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
        for path in links[1:]:
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

    def test_lesson_reflow(self):
        paths=['','lessons.html']+['lessons/'+p.name for p in (Path(__file__).resolve().parents[1]/'lessons').glob('*.html')]
        for width,scale in [(320,1),(421,2),(480,2),(640,2),(1280,1)]:
            self.page.set_viewport_size({'width':width,'height':900})
            for path in paths:
                self.page.goto(self.url+path)
                self.page.evaluate('(s)=>document.documentElement.style.fontSize = `${s*100}%`',scale)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(path,width,scale))
        self.page.goto(self.url+'lessons.html')
        self.page.keyboard.press('Tab')
        expect(self.page.locator('.skip')).to_be_focused()
        self.page.keyboard.press('Enter')
        expect(self.page.locator('#main')).to_be_focused()

if __name__=='__main__':
    unittest.main(defaultTest='Lessons')
