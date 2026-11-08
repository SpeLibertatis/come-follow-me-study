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

class ExploreCompanion(unittest.TestCase):
    def test_complete_library_and_links(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        from build_handout import Tree, Node, plain
        source=Tree((ROOT/'explore.html').read_text(encoding='utf-8')).root
        pdf=PdfReader(ROOT/'handouts/daniel-explore-further.pdf')
        self.assertEqual(len(pdf.pages),6)
        text=plain(' '.join(page.extract_text() for page in pdf.pages))
        urls={a.get_object().get('/A',{}).get('/URI') for page in pdf.pages for a in page.get('/Annots',[])}
        count=0
        for shelf in ['official','commentary','scholarship']:
            for article in source.find(id=shelf).children:
                if not isinstance(article,Node) or article.tag!='article': continue
                count+=1
                for field in ['h3','byline','resource-meta','chapters-label','investigate','resource-question','access']:
                    node=article.find('h3') if field=='h3' else article.find(cls=field)
                    self.assertIn(plain(node.text()),text)
                self.assertIn(article.find('a').attrs['href'],urls)
        self.assertEqual(count,14)
        self.assertIn(URL+'explore.html',urls)
        self.assertIn('What remains uncertain',text)
        self.assertFalse(pdf.get_fields())
        for name in ['index.html','explore.html']:
            self.assertIn('href="handouts/daniel-explore-further.pdf"',(ROOT/name).read_text(encoding='utf-8'))

if __name__=='__main__': unittest.main()
