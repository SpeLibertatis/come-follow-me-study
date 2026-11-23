"""Validate every canonical student route and the compatibility redirects."""
from html.parser import HTMLParser
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import importlib.util
import subprocess
import sys
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

    def test_latest_study_is_current_in_both_static_aliases(self):
        subprocess.run([sys.executable, str(ROOT / 'scripts/update_collection.py'), '--check'], check=True, cwd=ROOT)

    def test_latest_study_follows_newest_ready_card_not_future_or_archive_position(self):
        spec = importlib.util.spec_from_file_location('update_collection', ROOT / 'scripts/update_collection.py')
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        fixture = (
            '<ol class="lesson-list">'
            '<li data-week-start="2030-02-03"><span class="status ready">Ready to study</span><a href="lessons/new.html">New</a></li>'
            '<li data-week-start="2030-02-10"><span class="status">Not ready yet</span><a href="lessons/future.html">Future</a></li>'
            '<li data-week-start="2030-01-27"><span class="status ready">Ready to study</span><a href="lessons/old.html">Old</a></li></ol>'
        )
        cards = generator.CollectionCards(fixture).cards
        latest = generator.latest_ready(cards)
        self.assertEqual(latest['route'], 'lessons/new.html')
        self.assertIn('href="lessons/new.html"', generator.feature(latest)[0])
        self.assertNotIn('This week', generator.feature(latest)[0])
        self.assertEqual([card['route'] for card in generator.CollectionCards(generator.order_archive(fixture, cards)).cards],
                         ['lessons/new.html', 'lessons/old.html', 'lessons/future.html'])
        promoted = fixture.replace('class="status"', 'class="status ready"')
        self.assertEqual(generator.latest_ready(generator.CollectionCards(promoted).cards)['route'],
                         'lessons/future.html')
        empty = fixture.replace('class="status ready"', 'class="status"')
        self.assertIsNone(generator.latest_ready(generator.CollectionCards(empty).cards))
        self.assertEqual(generator.render(ROOT)['2027.html'], (ROOT / '2027.html').read_text())

    def test_core_joel_and_amos_readings_are_available_inline(self):
        joel = (ROOT / 'lessons/hosea-joel.html').read_text(encoding='utf-8')
        amos = (ROOT / 'lessons/amos-obadiah-jonah.html').read_text(encoding='utf-8')
        self.assertIn('Acts 2:32–33 · King James Version', joel)
        self.assertIn('he hath shed forth this', joel)
        self.assertIn('Amos 7:12–15 · King James Version', amos)
        self.assertIn('prophesy unto my people Israel', amos)
        self.assertIn('3 Nephi 11:29–30 · Original paraphrase', amos)

    def test_static_study_layout_matches_shared_templates(self):
        subprocess.run(
            [sys.executable, str(ROOT / 'scripts/update_study_layout.py'), '--check'],
            check=True, cwd=ROOT,
        )

    def test_study_layout_detects_and_repairs_copy_drift(self):
        routes = ('daniel.html', 'lessons/hosea-joel.html', 'lessons/amos-obadiah-jonah.html')
        with TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            templates = tuple(path.relative_to(ROOT) for path in (ROOT / 'scripts/templates').glob('*.html'))
            for relative_path in (*routes, 'scripts/update_study_layout.py', *templates):
                target = fixture / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative_path, target)
            daniel = fixture / routes[0]
            original = daniel.read_text(encoding='utf-8')
            amos = fixture / routes[2]
            original_amos = amos.read_text(encoding='utf-8')
            amos.write_text(
                original_amos.replace('>All lessons</a>', '>Archive</a>')
                .replace('>THE QUICK PATH</p>', '>OPENING</p>')
                .replace('>Print &amp; keep</h2>', '>Download</h2>')
                .replace('Independent supplemental study.', 'An independent guide.'),
                encoding='utf-8',
            )
            daniel.write_text(original.replace('>Quick study</a>', '>Start here</a>'), encoding='utf-8')
            command = [sys.executable, str(fixture / 'scripts/update_study_layout.py')]
            stale = subprocess.run([*command, '--check'], capture_output=True, text=True)
            self.assertEqual(stale.returncode, 1)
            self.assertIn('Study layout is stale: daniel.html, lessons/amos-obadiah-jonah.html', stale.stderr)
            self.assertIn('>Start here</a>', daniel.read_text(encoding='utf-8'))
            subprocess.run(command, check=True)
            self.assertEqual(daniel.read_text(encoding='utf-8'), original)
            self.assertEqual(amos.read_text(encoding='utf-8'), original_amos)
            subprocess.run([*command, '--check'], check=True)

    def test_student_study_links_use_same_three_shortcut_labels(self):
        for route in ('daniel.html', 'lessons/hosea-joel.html', 'lessons/amos-obadiah-jonah.html'):
            html = (ROOT / route).read_text(encoding='utf-8')
            segment = html.partition('aria-label="Study options"')[2].partition('</nav>')[0]
            with self.subTest(route=route):
                for label in ('Quick study', 'Go deeper', 'Print'):
                    self.assertIn(f'>{label}</a>', segment)

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
