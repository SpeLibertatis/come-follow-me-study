"""Static release checks for the weekly study, including the printed QR route."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ROUTE = "lessons/amos-obadiah-jonah.html"

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class Amos(unittest.TestCase):
    def test_qr_route_points_to_study(self):
        for entry in ("2026.html",):
            with self.subTest(entry=entry):
                self.assertIn(ROUTE, [a.get("href") for _, a in Page(ROOT / entry).tags])
        lesson = ROOT / ROUTE
        self.assertNotIn("Not ready yet", lesson.read_text())
        self.assertIn("the lord reveals truth through his prophets.", lesson.read_text().lower())
    def test_study_journey_and_downloads(self):
        lesson = ROOT / ROUTE
        tags = Page(lesson).tags
        ids = [attrs["id"] for _, attrs in tags if "id" in attrs]
        hrefs = [attrs["href"] for t, attrs in tags if t == "a" and "href" in attrs]
        for anchor in ("quick", "deep", "complete", "downloads"):
            with self.subTest(anchor=anchor):
                self.assertEqual(ids.count(anchor), 1)
                self.assertIn("#" + anchor, hrefs)
        pdfs = [h for h in hrefs if h.endswith(".pdf")]
        self.assertEqual(len(pdfs), 2)
        for pdf in pdfs:
            self.assertTrue((lesson.parent / pdf).read_bytes().startswith(b"%PDF"))
        self.assertFalse(any(t in {"form", "input", "textarea", "iframe", "script"} for t, _ in tags))
    def test_hillside_images_are_local(self):
        tags = Page(ROOT / ROUTE).tags
        artwork = [(t, a) for t, a in tags if any("amos-hillside" in a.get(k, "") for k in ("src", "srcset"))]
        self.assertEqual([t for t, _ in artwork], ["source", "img"])
        for tag, a in artwork:
            asset = a["srcset" if tag == "source" else "src"]
            self.assertTrue((ROOT / "lessons" / asset).is_file())
        self.assertTrue(artwork[1][1].get("alt"))

if __name__ == "__main__":
    unittest.main()
