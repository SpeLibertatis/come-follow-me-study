"""Offline content and privacy contract checks; run with python tests/verify.py."""
from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, name):
        super().__init__()
        self.tags = []
        self.feed((ROOT / name).read_text(encoding='utf-8'))
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class Contracts(unittest.TestCase):
    def test_complete_journey_without_library(self):
        page = Page('index.html')
        ids = {a['id'] for _, a in page.tags if 'id' in a}
        self.assertTrue({'daniel-1', 'daniel-3', 'daniel-6', 'reflection', 'finished'} <= ids)
        text = (ROOT / 'index.html').read_text(encoding='utf-8')
        self.assertIn('15-minute', text)
        self.assertEqual(text.count('class="deep-study"'), 3)
        self.assertNotIn('data-scene=', text)

    def test_external_links_and_assets(self):
        for name in ['index.html', 'explore.html']:
            page = Page(name)
            ids = [a['id'] for _, a in page.tags if 'id' in a]
            self.assertEqual(len(ids), len(set(ids)), name)
            for tag, attrs in page.tags:
                self.assertNotIn(tag, ['iframe', 'video', 'audio', 'embed', 'object'])
                if 'src' in attrs:
                    self.assertFalse(attrs['src'].startswith(('https:', 'http:', '//')))
                if tag == 'a':
                    href = attrs.get('href', '')
                    if href.startswith('https:'):
                        self.assertEqual(attrs.get('target'), '_blank')
                        self.assertTrue({'noopener', 'noreferrer'} <= set(attrs.get('rel', '').split()))
                    elif href.startswith('#'):
                        self.assertIn(href[1:], ids, (name, href))
                self.assertFalse(any(k.startswith('on') for k in attrs))

    def test_library_records(self):
        page = Page('explore.html')
        records = [a for t, a in page.tags if t == 'article' and 'data-themes' in a]
        self.assertGreaterEqual(len(records), 12)
        themes = {a['data-theme'] for _, a in page.tags if 'data-theme' in a}
        self.assertEqual(themes, {'all', 'babylon', 'pressure', 'furnace', 'lions', 'literary', 'history'})
        text = (ROOT / 'explore.html').read_text(encoding='utf-8')
        for doi in ['1476993X07084791', '10226486.2005.11745749', '9780199340378.013.152', '25610183', 'jets36-4-02', '4nI5UzicHWw']:
            self.assertIn(doi, text)
        self.assertEqual(text.count('class="investigate"'), len(records))
        self.assertEqual(text.count('class="resource-question"'), len(records))
        self.assertEqual(text.count('class="access"'), len(records))

    def test_no_collection(self):
        for name in ['study.js', 'explore.js', 'game.js']:
            text = (ROOT / name).read_text(encoding='utf-8')
            for forbidden in ['localStorage', 'sessionStorage', 'indexedDB', 'sendBeacon', 'fetch(', 'XMLHttpRequest', 'document.cookie', 'innerHTML']:
                self.assertNotIn(forbidden, text, name)

if __name__ == '__main__':
    unittest.main()
