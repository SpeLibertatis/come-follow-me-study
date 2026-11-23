"""Verify the student PDFs expose their content and links in a structure tree."""
from pathlib import Path
from unittest import TestCase, main

from pypdf import PdfReader
from pypdf.generic import ContentStream

ROOT = Path(__file__).resolve().parents[1] / 'handouts'
PAGE_COUNTS = {'amos-deep-study': 3, 'amos-quick-study': 2, 'daniel-explore-further': 6,
               'daniel-student-handout': 2, 'joel-deep-study': 2, 'joel-quick-study': 2}


class StudentPdfStructure(TestCase):
    def test_published_handouts_have_real_roles_and_link_bindings(self):
        for name, page_count in PAGE_COUNTS.items():
            with self.subTest(name=name):
                reader = PdfReader(ROOT / f'{name}.pdf')
                self.assertEqual(len(reader.pages), page_count)
                self.assertEqual(reader.root_object.get('/Lang'), 'en-US')
                self.assertTrue(reader.root_object['/MarkInfo']['/Marked'].value)
                tree = reader.root_object['/StructTreeRoot']
                document = tree['/K']
                self.assertEqual(document['/S'], '/Document')
                roles = [str(entry.get_object()['/S']) for entry in document['/K']]
                self.assertEqual(roles.count('/H1'), 1)
                self.assertIn('/H2', roles)
                numbers = tree['/ParentTree']['/Nums']
                parents = dict(zip(numbers[::2], numbers[1::2]))
                for page in reader.pages:
                    self.assertEqual(page['/Tabs'], '/S')
                    mcids = []
                    current = None
                    for args, operation in ContentStream(page['/Contents'], reader).operations:
                        if operation == b'BDC':
                            self.assertIsNone(current)
                            current = args[1]['/MCID']
                            mcids.append(current)
                        elif operation == b'BMC':
                            self.assertIsNone(current)
                            self.assertEqual(args[0], '/Artifact')
                            current = 'artifact'
                        elif operation == b'EMC':
                            self.assertIsNotNone(current)
                            current = None
                        elif operation in (b'Tj', b'TJ', b'Do'):
                            self.assertIsNotNone(current, f'Unclassified page content: {args}')
                    self.assertIsNone(current)
                    page_parents = parents[page['/StructParents']]
                    self.assertEqual(mcids, list(range(len(page_parents))))
                    for i, ref in enumerate(page_parents):
                        kid = ref.get_object()['/K']
                        self.assertIn(i, kid if isinstance(kid, list) else [kid])
                    for ref in page.get('/Annots', []):
                        annot = ref.get_object()
                        self.assertEqual(annot['/Subtype'], '/Link')
                        self.assertTrue(annot['/Contents'].strip())
                        link = parents[annot['/StructParent']].get_object()
                        self.assertEqual(link['/S'], '/Link')
                        self.assertEqual(link['/K'][-1]['/Type'], '/OBJR')
                        self.assertEqual(link['/K'][-1].raw_get('/Obj'), ref)


if __name__ == '__main__':
    main()
