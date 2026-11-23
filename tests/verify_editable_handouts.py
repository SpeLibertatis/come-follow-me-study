"""Opt-in source parity check; requires pinned fonts and Poppler (see build guide)."""
import argparse
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / 'scripts/student_handouts/build.py'
HISTORICAL = '5025bbb8b97c8107a031da65f5c53218f09fbfca'
NAMES = ('amos-quick-study', 'amos-deep-study', 'joel-quick-study', 'joel-deep-study')


def verify(ok, message):
    if not ok:
        raise ValueError(message)


def links(page):
    return [(tuple(link['/Rect']), dict(link['/A']))
            for ref in page.get('/Annots', []) if (link := ref.get_object())]


def compare(pdf, reference, temporary):
    first, second = PdfReader(pdf), PdfReader(reference)
    verify(len(first.pages) == len(second.pages), f'{pdf.name}: page count differs')
    for index, (a, b) in enumerate(zip(first.pages, second.pages), 1):
        note = f'{pdf.name}, page {index}, vs {reference.parent.name}'
        verify(a.mediabox == b.mediabox and a.cropbox == b.cropbox, f'{note}: box differs')
        verify(a.extract_text() == b.extract_text(), f'{note}: extracted text differs')
        verify(links(a) == links(b), f'{note}: link targets or areas differ')
    for side, source in (('candidate', pdf), ('reference', reference)):
        subprocess.run(['pdftoppm', '-r', '150', source, temporary / side],
                       check=True, stderr=subprocess.PIPE)
    for number in range(1, len(first.pages) + 1):
        verify((temporary / f'candidate-{number}.ppm').read_bytes() ==
               (temporary / f'reference-{number}.ppm').read_bytes(),
               f'{pdf.name}, page {number}: pixels differ')
    return len(first.pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fonts', type=Path)
    args = parser.parse_args()
    build = [sys.executable, str(BUILDER)]
    if args.fonts:
        build += ['--fonts', str(args.fonts)]
    with TemporaryDirectory() as path:
        work = Path(path)
        previews, repeat = work / 'previews', work / 'repeat'
        for destination in (previews, repeat):
            subprocess.run(build + ['--out', str(destination)], check=True)
        for path in (previews, ROOT / 'handouts'):
            rejected = subprocess.run(build + ['--out', str(path)], capture_output=True)
            verify(rejected.returncode == 2, f'Unsafe output path accepted: {path}')
        originals = work / 'historical'
        originals.mkdir()
        for name in NAMES:
            file = f'{name}.pdf'
            candidate = previews / file
            verify(candidate.read_bytes() == (repeat / file).read_bytes(),
                   f'{file}: nonreproducible output bytes')
            original = originals / file
            original.write_bytes(subprocess.check_output(
                ['git', 'show', f'{HISTORICAL}:handouts/{file}'], cwd=ROOT))
            count = compare(candidate, original, work)
            compare(candidate, ROOT / 'handouts' / file, work)
            print(f'{file}: deterministic; {count} pages, text, links, boxes, and pixels match both releases')


if __name__ == '__main__':
    main()
