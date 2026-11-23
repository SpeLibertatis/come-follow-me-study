"""Student collection, legacy routes and curriculum boundaries."""
from pathlib import Path
import json
from shutil import copytree
import sys
from tempfile import TemporaryDirectory
import unittest

from verify_routes import Page

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from update_collection import render


class Collection(unittest.TestCase):
    def test_landing_uses_only_feature_art_and_separate_archives(self):
        landing = (ROOT / 'index.html').read_text()
        self.assertEqual(landing, (ROOT / 'lessons.html').read_text())
        self.assertIn('id="studies"', landing)
        self.assertIn('href="2026.html"', landing)
        self.assertIn('href="2027.html"', landing)
        self.assertIn('Start the study', landing)
        self.assertNotIn('assets/lessons/', landing)
        self.assertNotIn('Design preview', landing)
        self.assertNotIn('This week', landing)
        self.assertIn('src="legacy-links.js"', landing)
        tags = Page(ROOT / 'index.html').tags
        mobile_sources = {
            a['src'] for t, a in tags if t in {'img', 'script'} and 'src' in a
        } | {
            a['href'] for t, a in tags if t == 'link' and a.get('rel') in {'stylesheet', 'icon'}
        }
        self.assertLess(len(landing.encode()) + sum((ROOT / url).stat().st_size for url in mobile_sources),
                        120 * 1024)

    def test_archive_boundary_and_official_links(self):
        old = (ROOT / '2026.html').read_text()
        new = (ROOT / '2027.html').read_text()
        self.assertEqual(old.count('Church Media Library</span>'), 7)
        self.assertIn('data-curriculum-year="2026"', old)
        self.assertNotIn('Matthew 1; Luke 1', old)
        self.assertIn('data-curriculum-year="2027"', new)
        self.assertIn('data-week-start="2026-12-28"', new)
        self.assertIn('Matthew 1; Luke 1', new)
        self.assertIn('come-follow-me-for-home-and-church-new-testament-2027/01?lang=eng', new)
        with (ROOT / 'scripts/collection-2027.json').open() as handle:
            published = [week for week in json.load(handle)['weeks'] if week['status'] == 'ready']
        self.assertEqual(new.count('Open student study'), len(published))
        for week in published:
            self.assertIn(f'href="{week["study_path"]}"', new)

    def test_cross_year_ready_feature_and_landing_limits(self):
        with TemporaryDirectory() as folder:
            fixture = Path(folder)
            copytree(ROOT / 'scripts/templates/collection', fixture / 'scripts/templates/collection')
            (fixture / '2026.html').write_bytes((ROOT / '2026.html').read_bytes())
            data = json.loads((ROOT / 'scripts/collection-2027.json').read_text())
            data['weeks'][0].update(status='ready', study_path='lessons/matthew-luke.html')
            for i, day in enumerate((4, 11, 18, 25, 26, 27), 2):
                data['weeks'].append(dict(week_start=f'2027-01-{day:02}', date_label=f'Jan {day}, 2027',
                                          title=f'Official {day}', theme='Test', manual_part=f'{i:02}',
                                          status='official-only'))
            (fixture / 'scripts/collection-2027.json').write_text(json.dumps(data))
            pages = render(fixture)
            self.assertEqual(pages['index.html'].count('class="entry"'), 2)
            self.assertEqual(pages['index.html'].count('class="calendar-date"'), 4)
            self.assertIn('Latest study · Dec 28, 2026–Jan 3, 2027', pages['index.html'])
            self.assertIn('class="cta" href="lessons/matthew-luke.html"', pages['index.html'])
            self.assertNotIn('This week', pages['index.html'])
            self.assertIn('href="lessons/matthew-luke.html"', pages['2027.html'])
            self.assertNotIn('href="lessons/matthew-luke.html"', pages['2026.html'])
            self.assertEqual(pages['2027.html'].count('data-curriculum-year="2027"'), 7)


if __name__ == '__main__':
    unittest.main()
