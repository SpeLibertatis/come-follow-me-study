"""Apply reviewed PDF 1.7 structural tags without changing the print artwork.

The zero-based maps refer to nonempty BT/ET runs, not lines or pages. They are
specific to the reviewed source PDFs and guarded by SHA-256. See docs/student-pdf-tags.md.
"""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf._cmap import get_encoding
from pypdf.generic import (
    ArrayObject, BooleanObject, ContentStream, DictionaryObject, NameObject,
    NumberObject, TextStringObject,
)


# Per original page: heading run(s), links in annotation order, artifacts.
# Unspecified text runs are paragraphs in content-stream order.
PLANS = {
    'amos-deep-study': (
        'Amos, Obadiah and Jonah: Deeper student study',
        [({1: 1, 8: 2, 14: 2}, [(5, 'Official Come, Follow Me lesson: Amos, Obadiah and Jonah'), (9, 'Amos 5:14–15, 24'), (10, 'Ezekiel 33:7–11'), (15, 'Alma 7:11–13')], {19}),
         ({1: 2, 4: 3, 12: 3}, [(6, 'Follow the Prophet; He Knows the Way, by Elder Teh'), (7, 'Following Christ, section III, by President Oaks'), (9, '3 Nephi 11:29–30'), (13, 'Jonah 3 and 4, selected verses')], {0, 17, 18}),
         ({1: 2}, [(5, 'Official Come, Follow Me lesson: Amos, Obadiah and Jonah'), (8, 'Scripture Helps: Amos, Obadiah, Jonah'), (11, 'Follow the Prophet; He Knows the Way, by Elder Teh'), (14, 'Following Christ, October 2024, by President Oaks'), (17, 'Alma 7:11–13'), (20, 'Jonah 3 and 4')], {0, 23, 24})],
    ),
    'amos-quick-study': (
        'Amos, Obadiah and Jonah: Quick student study',
        [({1: 1, 9: 2, 14: 2}, [(6, 'Official Come, Follow Me lesson: Amos, Obadiah and Jonah'), (10, 'Amos 7:12–15'), (15, 'Amos 3:3–8')], {19}),
         ({1: 2, 4: 3, 15: 3}, [(5, '3 Nephi 11:29–30'), (8, 'Following Christ, by President Oaks')], {0, 20, 21})],
    ),
    'daniel-explore-further': (
        'Daniel: Explore Further',
        [({2: 1, 5: 2, 13: 2, 21: 2}, [(12, 'Official Come, Follow Me lesson: Daniel 1–7'), (20, 'Daniel 1'), (28, 'Daniel 3')], {1}),
         ({2: 2, 3: 3, 11: 3, 20: 3, 28: 3}, [(10, 'Daniel 6'), (19, 'Bible Dictionary: Daniel'), (27, 'Be Not Afraid, Only Believe, by Dieter F. Uchtdorf'), (36, 'Hebrews 11')], {0, 1}),
         ({2: 2, 4: 3, 13: 3, 20: 3, 22: 3}, [(12, "Video: Daniel: Choosing God's Kingdom Over Ours"), (24, 'Visit the online Daniel library')], {0, 1}),
         ({2: 2, 4: 3, 13: 3, 22: 3}, [(12, 'The Book of Daniel in Recent Research (Part 1)'), (21, 'Daniel 3: Intratextual Perspectives and Intertextual Tradition'), (30, 'Book of Daniel, by Tawny Holm')], {0, 1}),
         ({2: 2, 3: 3, 12: 3, 21: 3}, [(11, 'The Babylonian Background of the Motif of the Fiery Furnace in Daniel 3'), (20, "Holding On To Daniel's Court Tales"), (29, 'The Literary Structure of the Book of Daniel')], {0, 1}),
         ({2: 2, 4: 3, 5: 4, 7: 4, 9: 4, 11: 4, 13: 4, 15: 3, 18: 3}, [], {0, 1})],
    ),
    'daniel-student-handout': (
        'Daniel 1, 3 and 6: Faith under pressure',
        [({2: 1, 8: 2, 18: 2}, [(7, 'Open the Come, Follow Me study site')], {1}),
         ({3: 2, 12: 2, 16: 2, 18: 2}, [], {0, 1, 2})],
    ),
    'joel-deep-study': (
        'Hosea and Joel: Deeper student study',
        [({1: 1, 7: 2, 12: 2}, [(3, 'Official Come, Follow Me lesson: Hosea and Joel'), (8, 'Joel 2:12–13, 21–27, 30–32'), (13, 'Joseph Smith—History 1:41'), (14, 'Scripture Helps: Hosea and Joel'), (16, 'Living in the Fulness of Times, by President Gordon B. Hinckley')], {20}),
         ({1: 2, 4: 3, 9: 3}, [(5, 'Moroni 10:4–8, 17–18'), (10, 'Helaman 6:34–36'), (12, 'Revelation for the Church, Revelation for Our Lives, by President Russell M. Nelson')], {0, 18, 19})],
    ),
    'joel-quick-study': (
        'Hosea and Joel: Quick student study',
        [({1: 1, 7: 2, 12: 2}, [(3, 'Official Come, Follow Me lesson: Hosea and Joel'), (8, 'Joel 2:28–29'), (14, 'Acts 2:16–18, 32–33')], {18}),
         ({1: 2, 4: 3, 10: 3}, [(5, 'Promptings of the Spirit, by Elder Gary E. Stevenson')], {0, 17, 18})],
    ),
}
DIGESTS = {
    'amos-deep-study': 'b2ce75e98bfb56e8a2ef004f69dd0893dc7ab8e1cc3545cef9a76a676aa6436a',
    'amos-quick-study': 'd3b6dee11e3eeb39f392a970c71c5ad10663e48831e21cf7f136586d63961420',
    'daniel-explore-further': '18fdf70aa1156061938b999ead3769f2f9eb3dc576db7f0f43a69f10dad10fb8',
    'daniel-student-handout': '9a89669e5fe47e743ea24eebc3345b1b0879fe753de3ecb61ad11d2121b90bd2',
    'joel-deep-study': '5ad4ebf9478edb85cd1372bcab5f8653929f119b516c351cd5a0206ac0949171',
    'joel-quick-study': 'fb5b1eb22e7bd4a7c65ec8ad86fc8f5114a76f114edc36c0f7819ed1d978db4c',
}


def name(value):
    return NameObject('/' + value)


def dictionary(**values):
    return DictionaryObject({name(key): value for key, value in values.items()})


def text_runs(operations):
    """Return inclusive paint ranges for complete text objects with glyphs."""
    begin = None
    painted = False
    runs = []
    for index, (_, operator) in enumerate(operations):
        if operator == b'BT':
            if begin is not None:
                raise ValueError('Nested text object')
            begin, painted = index, False
        elif operator in (b'Tj', b'TJ', b"'", b'"'):
            if begin is None:
                raise ValueError('Text paint outside text object')
            painted = True
        elif operator == b'ET':
            if begin is None:
                raise ValueError('Missing text object start')
            if painted:
                runs.append((begin, index + 1))
            begin = None
        elif operator in (b'BMC', b'BDC', b'EMC'):
            raise ValueError('Refusing to tag existing marked content')
    if begin is not None:
        raise ValueError('Unclosed text object')
    return runs


def visual_lines(operations):
    """Split a ReportLab text object only at rendered line boundaries."""
    start = 0
    painted = False
    for index, (_, operator) in enumerate(operations):
        if operator == b'Tj':
            painted = True
        elif operator == b'T*' and painted:
            yield operations[start:index + 1]
            start, painted = index + 1, False
    # Preserve closing ET and any other non-paint state.
    if start < len(operations):
        yield operations[start:]

def readable_text(operations, fonts):
    """Preserve spaces across visual wraps using each embedded ToUnicode map."""
    pieces = []
    font = None
    wrapped = False
    line_break = False
    for args, operator in operations:
        if operator == b'Tf':
            font = args[0]
        elif operator == b'T*':
            line_break = bool(pieces)
        elif operator == b'Tj':
            if line_break:
                pieces.append(' ')
                wrapped = True
                line_break = False
            encoding, cmap = fonts[font]
            body = args[0].original_bytes
            if isinstance(encoding, str):
                chars = body.decode(encoding)
            else:
                chars = ''.join(encoding[b] for b in body)
            pieces.append(''.join(cmap.get(c, c) for c in chars))
        elif operator in (b'TJ', b"'", b'"'):
            raise ValueError(f'Unexpected reviewed text operator: {operator!r}')
    return ''.join(pieces) if wrapped else None


def wrap(out, operations, tag=None, mcid=None, actual_text=None):
    if not operations:
        return
    if tag is None:
        out.append(([name('Artifact')], b'BMC'))
    else:
        props = dictionary(MCID=mcid)
        if actual_text is not None:
            props[name('ActualText')] = TextStringObject(actual_text)
        out.append(([name(tag), props], b'BDC'))
    out.extend(operations)
    out.append(([], b'EMC'))


def tag_pdf(source, destination):
    key = source.stem
    if sha256(source.read_bytes()).hexdigest() != DIGESTS[key]:
        raise ValueError(f'{source.name}: source differs from the reviewed layout')
    title, plan = PLANS[key]
    reader = PdfReader(source)
    writer = PdfWriter(clone_from=reader)
    writer.pdf_header = '%PDF-1.7'
    if len(writer.pages) != len(plan):
        raise ValueError('Page count differs from reviewed structure')
    catalog = writer.root_object
    catalog[name('Lang')] = TextStringObject('en-US')
    catalog[name('MarkInfo')] = dictionary(Marked=BooleanObject(True))
    catalog[name('ViewerPreferences')] = dictionary(DisplayDocTitle=BooleanObject(True))
    writer.add_metadata({'/Title': title})
    structure = dictionary(Type=name('StructTreeRoot'))
    structure_ref = writer._add_object(structure)
    document = dictionary(Type=name('StructElem'), S=name('Document'),
                          P=structure_ref, K=ArrayObject())
    document_ref = writer._add_object(document)
    catalog[name('StructTreeRoot')] = structure_ref
    structure[name('K')] = document_ref

    def element(parent, role, page_ref, kids, alt=None, actual_text=None):
        el = dictionary(Type=name('StructElem'), S=name(role), P=parent,
                        Pg=page_ref, K=kids)
        if alt is not None:
            el[name('Alt')] = TextStringObject(alt)
        if actual_text is not None:
            el[name('ActualText')] = TextStringObject(actual_text)
        ref = writer._add_object(el)
        parent.get_object()['/K'].append(ref)
        return ref

    parents = {}
    next_parent = len(plan)
    for page_num, (page, (headings, links, artifacts)) in enumerate(zip(writer.pages, plan, strict=True)):
        stream = ContentStream(page['/Contents'], writer)
        operations = stream.operations
        runs = text_runs(operations)
        fonts = {k: get_encoding(v.get_object()) for k, v in page['/Resources']['/Font'].items()}
        if any(i >= len(runs) for i in set(headings) | {i for i, _ in links} | artifacts):
            raise ValueError('Invalid reviewed text run index')
        annotations = page.get('/Annots', [])
        link_refs = {i: (ref, label) for (i, label), ref in zip(links, annotations, strict=True)}
        page[name('Tabs')] = name('S')
        page[name('StructParents')] = NumberObject(page_num)
        page_parents = parents[page_num] = ArrayObject()
        tagged = []
        cursor = 0
        original_document_kids = len(document['/K'])
        for index, (start, end) in enumerate(runs):
            wrap(tagged, operations[cursor:start])
            cursor = end
            if index in artifacts:
                wrap(tagged, operations[start:end])
                continue
            lines = list(visual_lines(operations[start:end]))
            tail = []
            if len(lines) > 1 and not any(op == b'Tj' for _, op in lines[-1]):
                tail = lines.pop()
            mcids = [NumberObject(len(page_parents) + i) for i in range(len(lines))]
            actual_text = readable_text(operations[start:end], fonts) if len(lines) > 1 else None
            if index in link_refs:
                annot_ref, label = link_refs[index]
                annot = annot_ref.get_object()
                if annot['/Subtype'] != '/Link' or annot['/A']['/S'] != '/URI':
                    raise ValueError('Expected a URI link annotation')
                annot[name('StructParent')] = NumberObject(next_parent)
                annot[name('Contents')] = TextStringObject(label)
                obj = dictionary(Type=name('OBJR'), Obj=annot_ref, Pg=page.indirect_reference)
                paragraph = element(document_ref, 'P', page.indirect_reference, ArrayObject())
                role = 'Link'
                link = element(paragraph, role, page.indirect_reference, ArrayObject([*mcids, obj]), label, actual_text)
                parents[next_parent] = link
                next_parent += 1
                ref = link
            else:
                role = 'H' + str(headings[index]) if index in headings else 'P'
                ref = element(document_ref, role, page.indirect_reference, mcids[0] if len(mcids) == 1 else ArrayObject(mcids), actual_text=actual_text)
            page_parents.extend([ref] * len(mcids))
            for line, mcid in zip(lines, mcids, strict=True):
                wrap(tagged, line, role, mcid)
            tagged.extend(tail)
        if page_num == 0 and key.startswith('daniel-'):
            # The source paints its footer before the first header. Read it last.
            footer = document['/K'].pop(original_document_kids)
            document['/K'].append(footer)
        wrap(tagged, operations[cursor:])
        stream.operations = tagged
        page.replace_contents(stream)

    nums = ArrayObject()
    for p, entry in sorted(parents.items()):
        nums.extend((NumberObject(p), entry))
    structure[name('ParentTree')] = writer._add_object(dictionary(Nums=nums))
    structure[name('ParentTreeNextKey')] = NumberObject(next_parent)
    with destination.open('xb') as fp:
        writer.write(fp)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='directory of reviewed, untagged source PDFs')
    parser.add_argument('destination', type=Path, help='fresh directory for generated tagged copies')
    parser.add_argument('names', nargs='*', choices=sorted(PLANS), help='one or more stems; omit for all')
    args = parser.parse_args()
    args.destination.mkdir(parents=True, exist_ok=True)
    for stem in args.names or PLANS:
        tag_pdf(args.source / f'{stem}.pdf', args.destination / f'{stem}.pdf')
