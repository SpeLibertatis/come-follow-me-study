"""Development-only browser checks: python tests/verify_game.py (requires playwright)."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import os
import unittest
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

class WordChallenge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/'
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(executable_path=os.environ.get('CHROME_PATH', '/usr/bin/chromium'), headless=True, args=['--no-sandbox'])
        expect.set_options(timeout=2000)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()

    def setUp(self):
        self.page = self.browser.new_page(viewport={'width': 1280, 'height': 900}, reduced_motion='reduce')
        self.errors, self.requests = [], []
        self.page.on('pageerror', lambda e: self.errors.append(str(e)))
        self.page.on('request', lambda r: self.requests.append(r.url))
        self.page.goto(self.url)
        self.game = self.page.locator('#daniel-word-challenge')

    def tearDown(self):
        self.page.close()

    def open_game(self):
        expect(self.game).to_have_count(1)
        self.game.locator('summary').click()
        expect(self.page.locator('#game-controls')).to_be_visible()

    def test_discovery_does_not_gate_study(self):
        self.page.locator('#finish').click()
        expect(self.page.locator('#finished')).to_be_visible()
        self.open_game()
        expect(self.page.locator('#game-progress')).to_have_text('Word 1 of 8')
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '6 letters: blank blank blank blank blank blank')

    def test_guess_repeat_and_complete(self):
        self.open_game()
        self.page.locator('[data-letter="D"]').click()
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '6 letters: D blank blank blank blank blank')
        self.page.keyboard.press('d')
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '6 letters: D blank blank blank blank blank')
        self.page.keyboard.press('z')
        expect(self.page.locator('#game-status')).to_contain_text('not in this word')
        self.page.keyboard.type('aniel')
        expect(self.page.locator('#game-status')).to_contain_text('You found DANIEL')
        expect(self.page.locator('#game-explanation')).to_be_visible()
        expect(self.page.locator('#game-hint')).to_be_disabled()

    def test_hint_reveal_and_next_reset(self):
        self.open_game()
        self.page.locator('#game-hint').click()
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '6 letters: D blank blank blank blank blank')
        self.page.locator('#game-reveal').click()
        expect(self.page.locator('#game-status')).to_contain_text('Answer: DANIEL')
        self.page.locator('#game-next').click()
        expect(self.page.locator('#game-progress')).to_have_text('Word 2 of 8')
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '5 letters: blank blank blank blank blank')
        expect(self.page.locator('#game-explanation')).to_be_hidden()
        expect(self.page.locator('#game-hint')).to_be_enabled()
        self.assertEqual(self.page.evaluate('document.activeElement.id'), 'game-clue')

    def test_multiword_and_last_puzzle_restart(self):
        self.open_game()
        for _ in range(2): self.page.locator('#game-next').click()
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '3 letters: blank blank blank; 4 letters: blank blank blank blank')
        self.page.locator('#game-reveal').click()
        expect(self.page.locator('#game-status')).to_contain_text('TEN DAYS')
        for _ in range(5): self.page.locator('#game-next').click()
        expect(self.page.locator('#game-progress')).to_have_text('Word 8 of 8')
        expect(self.page.locator('#game-next')).to_have_text('Start again')
        self.page.locator('#game-next').click()
        expect(self.page.locator('#game-progress')).to_have_text('Word 1 of 8')

    def test_keyboard_isolation_and_modifier_keys(self):
        self.open_game()
        self.page.locator('#thought').fill('A private reflection')
        self.page.locator('#thought').press('a')
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '6 letters: blank blank blank blank blank blank')
        self.game.locator('summary').focus()
        self.page.keyboard.press('Control+a')
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '6 letters: blank blank blank blank blank blank')
        self.game.locator('summary').click()
        self.page.keyboard.press('d')
        self.game.locator('summary').click()
        expect(self.page.locator('#game-word')).to_have_attribute('aria-label', '6 letters: blank blank blank blank blank blank')

    def test_no_network_or_persistence_and_reload_resets(self):
        self.open_game()
        initial = len(self.requests)
        self.page.locator('#game-reveal').click()
        self.page.locator('#game-next').click()
        self.assertEqual(len(self.requests), initial)
        self.assertTrue(all(u.startswith(self.url) for u in self.requests))
        self.assertEqual(self.page.evaluate('[localStorage.length, sessionStorage.length, document.cookie]'), [0, 0, ''])
        self.page.reload()
        self.open_game()
        expect(self.page.locator('#game-progress')).to_have_text('Word 1 of 8')
        self.assertEqual(self.errors, [])

    def test_mobile_reflow_targets_and_reduced_motion(self):
        self.page.set_viewport_size({'width': 320, 'height': 740})
        self.open_game()
        for _ in range(6): self.page.locator('#game-next').click()
        self.page.locator('#game-reveal').click()
        self.assertLessEqual(self.page.evaluate('document.documentElement.scrollWidth'), 320)
        for button in self.game.locator('button').all():
            box = button.bounding_box()
            self.assertGreaterEqual(box['height'], 44)
            self.assertGreaterEqual(box['width'], 44)
        self.assertEqual(self.page.evaluate('getComputedStyle(document.documentElement).scrollBehavior'), 'auto')

    def test_completion_keeps_keyboard_focus_in_game(self):
        self.open_game()
        self.page.locator('#game-reveal').click()
        self.assertEqual(self.page.evaluate('document.activeElement.id'), 'game-next')
        self.page.locator('#game-next').click()
        for _ in range(5): self.page.locator('#game-hint').click()
        self.assertEqual(self.page.evaluate('document.activeElement.id'), 'game-next')

    def test_enlarged_text_reflows_within_game(self):
        self.page.set_viewport_size({'width': 320, 'height': 740})
        self.open_game()
        self.page.evaluate("document.documentElement.style.fontSize = '200%'")
        for _ in range(6): self.page.locator('#game-next').click()
        self.page.locator('#game-reveal').click()
        self.assertTrue(self.game.evaluate('(el) => el.scrollWidth <= el.clientWidth'))
        for button in self.game.locator('button').all():
            box = button.bounding_box()
            self.assertGreaterEqual(box['height'], 44)
            self.assertGreaterEqual(box['width'], 44)

    def test_capture_review_screenshots(self):
        output = os.environ.get('DANIEL_SCREENSHOT_DIR')
        if not output:
            self.skipTest('Set DANIEL_SCREENSHOT_DIR to save review images')
        output = Path(output)
        output.mkdir(parents=True, exist_ok=True)
        self.open_game()
        self.page.locator('#lions-den').screenshot(path=str(output / 'desktop-game.png'))
        self.page.set_viewport_size({'width': 320, 'height': 740})
        self.page.locator('#lions-den').screenshot(path=str(output / 'mobile-game.png'))
        for _ in range(6): self.page.locator('#game-next').click()
        self.page.locator('#game-reveal').click()
        self.page.evaluate("document.documentElement.style.fontSize = '200%'")
        self.page.locator('#lions-den').screenshot(path=str(output / 'mobile-enlarged-game.png'))

    def test_script_unavailable_has_useful_fallback(self):
        self.page.route('**/game.js', lambda route: route.abort())
        self.page.reload()
        expect(self.game).to_have_count(1)
        self.game.locator('summary').click()
        expect(self.page.locator('#game-fallback')).to_be_visible()
        expect(self.page.locator('#game-controls')).to_be_hidden()
        self.page.locator('#finish').click()
        expect(self.page.locator('#finished')).to_be_visible()

if __name__ == '__main__':
    unittest.main()
