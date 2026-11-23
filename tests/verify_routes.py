"""Validate every canonical student route and the compatibility redirects."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE_SCRIPTS = {
    'index.html': {'legacy-links.js'},
    'lessons.html': {'legacy-links.js'},
    'daniel.html': {'study.js', 'game.js'},
    'explore.html': {'explore.js'},
}
REDIRECTS = {'adventure.html', 'journal.html'}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.feed(path.read_text(encoding='utf-8'))
        self.ids = [attrs['id'] for _, attrs in self.tags if 'id' in attrs]

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def read_routes(root):
    paths = sorted([*root.glob('*.html'), *(root / 'lessons').glob('*.html')])
    return {path.relative_to(root).as_posix(): Page(path) for path in paths}


def route_findings(root, routes):
    for route, page in routes.items():
        if len(page.ids) != len(set(page.ids)):
            yield (route, 'duplicate ID')
        for tag, attrs in page.tags:
            refs = [attrs[key] for key in ('href', 'src') if key in attrs]
            refs.extend(item.strip().split()[0] for item in attrs.get('srcset', '').split(',') if item.strip())
            for ref in refs:
                url = urlsplit(ref)
                if url.scheme or url.netloc:
                    if tag != 'a' or url.scheme != 'https':
                        yield (route, f'unexpected network/non-HTTPS reference {ref}')
                    elif attrs.get('target') != '_blank' or not {'noopener', 'noreferrer'} <= set(attrs.get('rel', '').split()):
                        yield (route, f'unsafe external link attributes {ref}')
                    continue
                target = (root / route).parent / unquote(url.path) if url.path else root / route
                target = target.resolve()
                if target.is_dir():
                    target /= 'index.html'
                if not target.is_relative_to(root) or not target.is_file():
                    yield (route, f'missing/outside local target {ref}')
                elif target.suffix == '.html' and url.fragment:
                    destination = routes.get(target.relative_to(root).as_posix()) or Page(target)
                    if unquote(url.fragment) not in destination.ids:
                        yield (route, f'bad internal fragment {ref}')


class Routes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes = read_routes(ROOT)

    def test_collection_alias_stays_identical(self):
        self.assertEqual((ROOT / 'index.html').read_bytes(), (ROOT / 'lessons.html').read_bytes())

    def test_internal_links_anchors_assets_and_outbound_attributes(self):
        self.assertEqual(list(route_findings(ROOT, self.routes)), [])

    def test_route_security_profiles(self):
        for route, page in self.routes.items():
            with self.subTest(route=route):
                csp = [a['content'] for t, a in page.tags
                       if t == 'meta' and a.get('http-equiv', '').lower() == 'content-security-policy']
                self.assertEqual(len(csp), 1)
                rules = {rule.split()[0]: rule.split()[1:] for rule in csp[0].split(';') if rule.strip()}
                for directive in ('default-src', 'form-action', 'base-uri', 'object-src'):
                    self.assertEqual(rules.get(directive), ["'none'"], directive)
                if route not in REDIRECTS:
                    self.assertEqual(rules.get('connect-src'), ["'none'"])
                metas = [a.get('content') for t, a in page.tags if t == 'meta' and a.get('name') == 'referrer']
                self.assertEqual(metas, ['no-referrer'])
                self.assertFalse(any(t in {'form', 'iframe', 'embed', 'object'} for t, _ in page.tags))
                self.assertFalse(any(k.startswith('on') for _, a in page.tags for k in a))
                scripts = [a.get('src') for t, a in page.tags if t == 'script']
                self.assertEqual(sorted(scripts), sorted(PAGE_SCRIPTS.get(route, ())))
                self.assertEqual(rules.get('script-src'), ["'self'"] if scripts else None)
                redirect = [a.get('content') for t, a in page.tags
                            if t == 'meta' and a.get('http-equiv', '').lower() == 'refresh']
                self.assertEqual(redirect, ['0; url=daniel.html'] if route in REDIRECTS else [])


if __name__ == '__main__':
    unittest.main()
