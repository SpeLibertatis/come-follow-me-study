"""Regenerate the static study page components without changing lesson bodies."""
import argparse
from html import escape
from pathlib import Path
import re
from string import Template

from shared_header import apply as apply_header

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / 'scripts/templates'
DANIEL = 'daniel.html'
JOEL = 'lessons/hosea-joel.html'
AMOS = 'lessons/amos-obadiah-jonah.html'

COMPANION_LINKS = {'quick': '#quick', 'deep': '#deep', 'print': '#downloads'}
DESTINATIONS = {
    DANIEL: {'quick': '#daniel-1', 'deep': 'explore.html', 'print': '#student-print'},
    JOEL: COMPANION_LINKS,
    AMOS: COMPANION_LINKS,
}

FOOTERS = {
    DANIEL: {
        'brand': '<p class="brand">COME, FOLLOW ME <span>AN INDEPENDENT STUDY EXPLORATION</span></p>',
        'credit': 'Independent and supplemental.',
        'privacy': ('No accounts, analytics or automatic reflection storage. External links open another site '
                    'with its own privacy policy. Hosting providers, including GitHub Pages, may log requests.'),
        'extra': '<p>Original imagined artwork · <a href="PRIVACY.md">Privacy</a></p>',
    },
    JOEL: {
        'credit': 'Unofficial supplemental study.',
        'privacy': ('No accounts, tracking, or saved study activity. GitHub Pages and network providers may process '
                    'routine access logs. Official lesson links open the Church website, which has its own privacy practices.'),
    },
    AMOS: {
        'credit': 'Independent supplemental study.',
        'privacy': ('No accounts, tracking, forms, or saved study activity. Your responses stay in your own notebook. '
                    'GitHub Pages and network providers may process routine access logs. Source links leave this site '
                    'and follow the destination’s privacy practices.'),
    },
}

COMPANIONS = {
    JOEL: {
        'heading': 'A promise in a<br><em>broken landscape.</em>',
        'inner_open': '<div class="deep-inner">',
        'section_label': ' aria-labelledby="downloads-title"',
        'eyebrow': 'TAKE THE STUDY WITH YOU',
        'heading_id': ' id="downloads-title"',
    },
    AMOS: {
        'heading': '“Go away.”<br><em>“The Lord sent me.”</em>',
        'inner_open': '',
        'section_label': '',
        'eyebrow': 'STUDENT DOWNLOADS',
        'heading_id': '',
    },
}

SLOTS = {
    'study-navigation': r'<nav class="study-path"[^>]*>.*?</nav>',
    'study-footer': r'<footer>.*?</footer>',
    **{f'companion-{name}': rf'<section id="{anchor}"[^>]*>(?:(?!</?section\b).)*?</h2>'
       for name, anchor in (('quick', 'quick'), ('deep', 'deep'), ('print', 'downloads'))},
}


def render_component(source, name, values):
    """Replace one owned region and preserve all surrounding page content."""
    matches = list(re.finditer(SLOTS[name], source, re.DOTALL))
    if len(matches) != 1:
        raise ValueError(f'expected exactly one {name} slot')
    template = Template((TEMPLATES / f'{name}.html').read_text(encoding='utf-8').removesuffix('\n'))
    match = matches[0]
    return source[:match.start()] + template.substitute(values) + source[match.end():]


def render(source, route):
    components = {
        'study-navigation': {key: escape(href, quote=True) for key, href in DESTINATIONS[route].items()},
        'study-footer': {'brand': '', 'extra': '', **FOOTERS[route]},
    }
    if route in COMPANIONS:
        components.update({f'companion-{section}': COMPANIONS[route] for section in ('quick', 'deep', 'print')})
    for name, values in components.items():
        source = render_component(source, name, values)
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the tracked HTML needs regenerating')
    args = parser.parse_args()
    changes = {}
    collection = {'index.html', 'lessons.html', '2026.html', '2027.html'}
    redirects = {'adventure.html', 'journal.html'}
    paths = sorted([*ROOT.glob('*.html'), *(ROOT / 'lessons').glob('*.html')])
    for path in paths:
        route = path.relative_to(ROOT).as_posix()
        if route in collection | redirects:
            continue
        original = path.read_text(encoding='utf-8')
        try:
            generated = apply_header(original, route)
            if route in DESTINATIONS:
                generated = render(generated, route)
        except ValueError as error:
            parser.exit(1, f'{route}: {error}.\n')
        if generated != original:
            changes[route] = generated
    if args.check and changes:
        parser.exit(1, f'Study layout is stale: {", ".join(changes)}. Run python scripts/update_study_layout.py.\n')
    for route, generated in changes.items():
        (ROOT / route).write_text(generated, encoding='utf-8')


if __name__ == '__main__':
    main()
