"""Run with Python plus pypdf (development only)."""
from pathlib import Path
import unittest
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
URL='https://spelibertatis.github.io/come-follow-me-study/'

class Handout(unittest.TestCase):
    def test_two_page_printable_lesson(self):
        pdf=PdfReader(ROOT/'handouts/daniel-student-handout.pdf')
        self.assertEqual(len(pdf.pages),2)
        text='\n'.join(p.extract_text() for p in pdf.pages)
        for phrase in ['Daniel 1:8, 12','Daniel 3:17-18','Daniel 6:10','But if not','as he did aforetime','One next step','spelibertatis.github.io/come-follow-me-study/']:
            self.assertIn(phrase,text)
        self.assertFalse(pdf.get_fields())
        links=[a.get_object().get('/A',{}).get('/URI') for p in pdf.pages for a in p.get('/Annots',[])]
        self.assertIn(URL,links)
        for p in pdf.pages:
            self.assertEqual(tuple(p.mediabox),(0,0,612,792))

    def test_both_pages_offer_local_pdf(self):
        for name in ['index.html','explore.html']:
            self.assertIn('href="handouts/daniel-student-handout.pdf"',(ROOT/name).read_text(encoding='utf-8'))

if __name__=='__main__': unittest.main()
