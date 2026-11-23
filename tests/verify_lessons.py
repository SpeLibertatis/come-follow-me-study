"""Lesson index and placeholder browser checks; no production dependencies."""
from browser_fixture import BrowserCase, expect
from pathlib import Path
import unittest

class Lessons(BrowserCase):
    def test_lesson_navigation(self):
        self.page.goto(self.url + 'lessons.html')
        expect(self.page).to_have_title('All lessons · 2026 — Scripture study')
        cards = self.page.locator('.lesson-list li').evaluate_all("""cards => cards.map(card => ({
            path: card.querySelector('h2 a').getAttribute('href'),
            status: card.querySelector('.status').textContent.trim()
        }))""")
        self.assertTrue(cards)
        paths = [card['path'] for card in cards]
        self.assertEqual(len(paths), len(set(paths)))
        for card in cards:
            path, status = card['path'], card['status']
            with self.subTest(path=path):
                self.assertIn(status, {'Ready to study', 'Not ready yet'})
                response = self.page.goto(self.url + path)
                self.assertEqual(response.status, 200)
                placeholder = self.page.get_by_role('heading', name='Not ready yet', exact=True)
                if status == 'Not ready yet':
                    expect(placeholder).to_be_visible()
                    expect(self.page.get_by_role('link', name='Read the official lesson')).to_have_attribute('rel', 'noopener noreferrer')
                    self.page.get_by_role('link', name='← Back to all lessons').click()
                    expect(self.page).to_have_title('All lessons · 2026 — Scripture study')
                else:
                    expect(placeholder).to_have_count(0)
        self.page.goto(self.url + 'lessons.html')
        self.page.get_by_role('link',name='Daniel 1–7',exact=True).click()
        expect(self.page.locator('#lions-den')).to_have_count(1)
        self.assertFalse(self.errors)
        self.assertTrue(all(u.startswith(self.url) for u in self.requests))

    def test_latest_study_works_from_both_collection_urls_without_javascript(self):
        page = self.browser.new_page(java_script_enabled=False, viewport={'width': 390, 'height': 844})
        try:
            for entry in ('index.html', 'lessons.html'):
                page.goto(self.url + entry)
                action = page.get_by_role('link', name='Open the latest study', exact=True)
                expect(action).to_be_visible()
                href = action.get_attribute('href')
                archive = page.locator('.lesson-list > li')
                expect(archive.first.locator('h2 a')).to_have_attribute('href', href)
                state_and_dates = archive.evaluate_all("""cards => cards.map(card => [
                    card.querySelector('.status').classList.contains('ready'), card.dataset.weekStart
                ])""")
                self.assertEqual(state_and_dates, sorted(state_and_dates, reverse=True))
                destination_card = page.locator(f'.lesson-list a[href="{href}"]').locator('xpath=ancestor::li')
                expect(destination_card.locator('.status')).to_have_text('Ready to study')
                action.click()
                expect(page).to_have_url(self.url + href)
                expect(page.get_by_role('navigation', name='Study options')).to_be_visible()
        finally:
            page.close()

    def test_joel_companion(self):
        self.page.goto(self.url+'lessons.html')
        self.page.get_by_role('link',name='Hosea 1–6; 10–14; Joel',exact=True).click()
        expect(self.page).to_have_title('Joel — I will pour out my spirit upon all flesh')
        self.page.get_by_role('link',name='Begin the quick path').click()
        expect(self.page.locator('#quick-title')).to_be_visible()
        self.assertEqual(self.page.locator('.quick-step').count(),4)
        self.assertEqual(self.page.locator('.deep-module').count(),4)
        self.assertEqual(self.page.locator('.phrase-discovery details').count(),3)
        self.assertEqual(self.page.locator('.practice-choices details').count(),3)
        for detail in self.page.locator('.phrase-discovery details, .practice-choices details').all():
            detail.locator('summary').click()
            self.assertTrue(detail.evaluate('(el)=>el.open'))
            detail.locator('summary').click()
        for disclosure in self.page.locator('.deep-module').all():
            disclosure.locator('summary').click()
            self.assertTrue(disclosure.evaluate('(el) => el.open'))
            disclosure.locator('summary').click()
        self.assertEqual(self.page.locator('form, input, textarea, iframe, script').count(),0)
        self.assertNotIn('Teacher source audit',self.page.content())
        for link in self.page.locator('#downloads a').all():
            response=self.page.request.get(link.get_attribute('href').replace('../',self.url))
            self.assertEqual(response.status,200)
            self.assertTrue(response.body().startswith(b'%PDF'))
        self.page.locator('header .site-brand').click()
        expect(self.page).to_have_title('All lessons · 2026 — Scripture study')
        self.assertTrue(all(u.startswith(self.url) for u in self.requests))

    def test_amos_companion(self):
        self.page.set_viewport_size({'width': 390, 'height': 844})
        for collection in ('index.html', 'lessons.html'):
            self.page.goto(self.url + collection)
            lesson = self.page.locator('.lesson-list li').filter(has_text='November 23–29, 2026')
            expect(lesson.locator('.status')).to_have_text('Ready to study')
            lesson.get_by_role('link', name='Amos; Obadiah; Jonah', exact=True).click()
            expect(self.page).to_have_url(self.url + 'lessons/amos-obadiah-jonah.html')

        expect(self.page.get_by_role('heading', name='A voice worth hearing.')).to_be_visible()
        expect(self.page.locator('.amos-hero .verse-label')).to_have_text(
            'THE LORD REVEALS TRUTH THROUGH HIS PROPHETS.')
        self.page.locator('.amos-hero img').evaluate('(img) => img.decode()')
        self.assertTrue(self.page.locator('.amos-hero img').evaluate(
            "(img) => img.currentSrc.endsWith('/assets/amos-hillside-small.webp')"))
        self.page.keyboard.press('Tab')
        expect(self.page.locator('.skip')).to_be_focused()
        self.page.keyboard.press('Enter')
        expect(self.page.locator('#main')).to_be_focused()
        self.page.get_by_role('link', name='Begin the quick path').click()
        expect(self.page).to_have_url(self.url + 'lessons/amos-obadiah-jonah.html#quick')
        expect(self.page.locator('#quick .quick-step')).to_have_count(3)
        self.page.get_by_role('link', name='Choose one small next step').click()
        expect(self.page).to_have_url(self.url + 'lessons/amos-obadiah-jonah.html#complete')
        expect(self.page.locator('#complete .practice-choices details')).to_have_count(3)
        self.page.get_by_role('link', name='Keep exploring').click()
        expect(self.page).to_have_url(self.url + 'lessons/amos-obadiah-jonah.html#deep')
        expect(self.page.locator('#deep .deep-module')).to_have_count(3)
        for disclosure in self.page.locator('.deep-module, .practice-choices details').all():
            summary = disclosure.locator(':scope > summary')
            summary.focus()
            summary.press('Enter')
            self.assertTrue(disclosure.evaluate('(el) => el.open'))
            summary.press('Space')
            self.assertFalse(disclosure.evaluate('(el) => el.open'))
        self.page.get_by_role('navigation', name='Study options').get_by_role('link', name='Print', exact=True).click()
        expect(self.page).to_have_url(self.url + 'lessons/amos-obadiah-jonah.html#downloads')
        for link in self.page.locator('#downloads a').all():
            response = self.page.request.get(link.get_attribute('href').replace('../', self.url))
            self.assertEqual(response.status, 200)
            self.assertTrue(response.body().startswith(b'%PDF'))
        expect(self.page.locator('form, input, textarea, iframe, script')).to_have_count(0)
        expect(self.page.locator('meta[name="referrer"]')).to_have_attribute('content', 'no-referrer')
        csp = self.page.locator('meta[http-equiv="Content-Security-Policy"]').get_attribute('content')
        self.assertIn("connect-src 'none'", csp)
        for link in self.page.locator('main a[target="_blank"]').all():
            expect(link).to_have_attribute('rel', 'noopener noreferrer')
            self.assertTrue(link.get_attribute('href').startswith('https://www.churchofjesuschrist.org/'))
        for link in self.page.locator('main a[href^="#"]').all():
            expect(self.page.locator(link.get_attribute('href'))).to_have_count(1)
        self.assertFalse(self.errors)
        self.assertTrue(all(u.startswith(self.url) for u in self.requests))

    def test_narrative_hero_labels_are_legible_in_print(self):
        self.page.emulate_media(media='print')
        for path in ('lessons/hosea-joel.html', 'lessons/amos-obadiah-jonah.html'):
            with self.subTest(path=path):
                self.page.goto(self.url + path)
                hero = self.page.locator('.joel-hero')
                expect(hero).to_have_css('background-color', 'rgb(255, 255, 255)')
                self.assertEqual(hero.evaluate("el => getComputedStyle(el, '::after').display"), 'none')
                for label in self.page.locator(
                    '.joel-hero .verse-label, .joel-hero .art-caption, '
                    '.scene-promise .scene-number, .scene-promise .scripture sup'
                ).all():
                    expect(label).to_have_css('color', 'rgb(0, 0, 0)')

    def test_home_and_legacy_routes(self):
        for path in ['', 'index.html', 'lessons.html']:
            self.page.goto(self.url+path)
            expect(self.page).to_have_title('All lessons · 2026 — Scripture study')
            self.assertEqual(self.page.locator('header').get_by_text('Daniel study').count(),0)
            self.assertEqual(self.page.locator('link[rel="icon"]').count(),1)
        for fragment in ['#lions-den','#daniel-3','#reflection']:
            self.page.goto(self.url+fragment)
            expect(self.page).to_have_url(self.url+'daniel.html'+fragment)
        self.page.goto(self.url+'daniel.html')
        self.page.locator('header .site-brand').click()
        expect(self.page).to_have_title('All lessons · 2026 — Scripture study')

    def test_design_screenshots(self):
        import os
        folder=Path(os.environ.get('DANIEL_SCREENSHOT_DIR','/tmp/cfm-design-screenshots'))
        folder.mkdir(parents=True,exist_ok=True)
        for width in [390,1280]:
            self.page.set_viewport_size({'width':width,'height':900})
            for name,path in [('collection','index.html'),('joel','lessons/hosea-joel.html')]:
                self.page.goto(self.url+path)
                for picture in self.page.locator('img').all():
                    picture.scroll_into_view_if_needed()
                    picture.evaluate('(img) => img.decode()')
                self.page.evaluate('window.scrollTo(0,0)')
                self.page.screenshot(path=str(folder/f'{name}-{width}.png'),full_page=True)
                self.page.screenshot(path=str(folder/f'{name}-opening-{width}.png'))
            self.page.goto(self.url+'lessons/hosea-joel.html#jesus')
            self.page.screenshot(path=str(folder/f'joel-discovery-{width}.png'))
            self.page.goto(self.url+'lessons/hosea-joel.html#complete')
            self.page.screenshot(path=str(folder/f'joel-complete-{width}.png'))
            self.page.locator('.practice-choices summary').first.click()
            self.page.screenshot(path=str(folder/f'joel-practice-{width}.png'))
            self.page.locator('#deep').scroll_into_view_if_needed()
            self.page.locator('.deep-module summary').first.click()
            self.page.screenshot(path=str(folder/f'joel-deep-{width}.png'))

    def test_lesson_reflow(self):
        paths=['','lessons.html']+['lessons/'+p.name for p in (Path(__file__).resolve().parents[1]/'lessons').glob('*.html')]
        for width,scale in [(320,1),(421,2),(480,2),(640,2),(1280,1)]:
            self.page.set_viewport_size({'width':width,'height':900})
            for path in paths:
                self.page.goto(self.url+path)
                if path in ('lessons/hosea-joel.html', 'lessons/amos-obadiah-jonah.html'):
                    self.page.locator('details').evaluate_all('(els)=>els.forEach(e=>e.open=true)')
                self.page.evaluate('(s)=>document.documentElement.style.fontSize = `${s*100}%`',scale)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(path,width,scale))
        self.page.goto(self.url+'lessons.html')
        self.page.keyboard.press('Tab')
        expect(self.page.locator('.skip')).to_be_focused()
        self.page.keyboard.press('Enter')
        expect(self.page.locator('#main')).to_be_focused()

if __name__=='__main__':
    unittest.main(defaultTest='Lessons')
