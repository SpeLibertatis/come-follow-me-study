"""Compose the shared masthead into static student pages; no browser runtime."""
from pathlib import Path, PurePosixPath
import re
from string import Template

TEMPLATE = Path(__file__).resolve().parent / 'templates/site-header.html'
HEADER = re.compile(r'<header class="site-header"[^>]*>.*?</header>', re.DOTALL)


def apply(source, route):
    prefix = '../' * (len(PurePosixPath(route).parts) - 1)
    header = Template(TEMPLATE.read_text(encoding='utf-8').rstrip('\n')).substitute(prefix=prefix)
    source, count = HEADER.subn(lambda _: header, source)
    if count != 1:
        raise ValueError(f'{route}: expected one site header, got {count}')
    stylesheet = f'<link rel="stylesheet" href="{prefix}site-header.css">'
    if stylesheet not in source:
        if '</head>' not in source:
            raise ValueError(f'{route}: missing head for site header stylesheet')
        source = source.replace('</head>', stylesheet + '</head>', 1)
    return source
