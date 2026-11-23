#!/usr/bin/env python3
"""Regenerate editable student handout previews; never overwrites published files."""
import argparse
import hashlib
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import amos
import joel

HERE = Path(__file__).resolve().parent
PUBLISHED = HERE.parents[1] / 'handouts'
FONTS = {
    'Body': ('DejaVuSans.ttf', '57f73e11f51999432bf7ab22ce55b6f945d5eca1bf824404cfa9ec2e3718c84e'),
    'Bold': ('DejaVuSans-Bold.ttf', 'a4c5bc453ca281d90ea079e596da7ae0dfeb5777497c29ec254e76d97ff6f890'),
    'Serif': ('DejaVuSerif.ttf', '8cb29f7db250ebb2551a6ce2c1e0bfd5a0eb520e9e233370db0493e82e1f36f7'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--fonts', type=Path, default=Path('/usr/share/fonts/truetype/dejavu'))
    args = parser.parse_args()
    destination = args.out.resolve()
    if destination == PUBLISHED or PUBLISHED in destination.parents:
        parser.error('Choose a preview directory outside the published handouts folder.')
    for family, (name, expected) in FONTS.items():
        path = args.fonts / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            parser.error(f'{path}: missing or incompatible DejaVu 2.37 font; see the build guide.')
        pdfmetrics.registerFont(TTFont(family, str(path)))
    destination.mkdir(parents=True, exist_ok=True)
    for name in ('amos-quick-study', 'amos-deep-study', 'joel-quick-study', 'joel-deep-study'):
        if (destination / f'{name}.pdf').exists() or (destination / f'{name}.pdf').is_symlink():
            parser.error('Choose an empty preview directory; refusing to overwrite existing PDFs.')
    amos.build(destination)
    for name in ('joel-quick-study', 'joel-deep-study'):
        joel.build(HERE / f'{name}.json', destination / f'{name}.pdf')


if __name__ == '__main__':
    main()
