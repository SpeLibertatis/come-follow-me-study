"""Lesson index and placeholder browser checks; no production dependencies."""
from verify_game import WordChallenge, expect
from pathlib import Path
import unittest

class Lessons(WordChallenge):
    def test_lesson_navigation(self):
        self.page.get_by_role('link', name='All lessons', exact=True).click()
        expect(self.page).to_have_title('All lessons · 2026 — Scripture study')
        links=self.page.locator('.lesson-list h2 a').evaluate_all('(els) => els.map(e => e.getAttribute("href"))')
        self.assertEqual(len(links),7)
        for path in links[2:]:
            response=self.page.goto(self.url+path)
            self.assertEqual(response.status,200)
            expect(self.page.get_by_role('heading',name='Not ready yet',exact=True)).to_be_visible()
            expect(self.page.get_by_role('link',name='Read the official lesson')).to_have_attribute('rel','noopener noreferrer')
            self.page.get_by_role('link',name='← Back to all lessons').click()
            expect(self.page).to_have_title('All lessons · 2026 — Scripture study')
        self.page.get_by_role('link',name='Daniel 1–7',exact=True).click()
        expect(self.page.locator('#lions-den')).to_have_count(1)
        self.assertFalse(self.errors)
        self.assertTrue(all(u.startswith(self.url) for u in self.requests))

    def test_joel_companion(self):
        self.page.goto(self.url+'lessons.html')
        self.page.get_by_role('link',name='Hosea 1–6; 10–14; Joel',exact=True).click()
        expect(self.page).to_have_title('Joel — I will pour out my spirit upon all flesh')
        self.page.get_by_role('link',name='Begin the quick path').click()
        expect(self.page.locator('#quick-title')).to_be_visible()
        self.assertEqual(self.page.locator('.quick-step').count(),4)
        self.assertEqual(self.page.locator('.deep-module').count(),4)
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
                self.page.screenshot(path=str(folder/f'{name}-{width}.png'),full_page=True)
            self.page.locator('#deep').scroll_into_view_if_needed()
            self.page.locator('.deep-module summary').first.click()
            self.page.screenshot(path=str(folder/f'joel-deep-{width}.png'))

    def test_lesson_reflow(self):
        paths=['','lessons.html']+['lessons/'+p.name for p in (Path(__file__).resolve().parents[1]/'lessons').glob('*.html')]
        for width,scale in [(320,1),(421,2),(480,2),(640,2),(1280,1)]:
            self.page.set_viewport_size({'width':width,'height':900})
            for path in paths:
                self.page.goto(self.url+path)
                if 'hosea-joel' in path:
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
