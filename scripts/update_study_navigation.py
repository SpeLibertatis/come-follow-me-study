"""Regenerate the shared, static Quick study / Go deeper / Print navigation."""
import argparse
from html import escape
from pathlib import Path
import re
from string import Template

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'scripts/templates/study-navigation.html'
NAVIGATION = re.compile(r'<nav class="study-path"[^>]*>.*?</nav>', re.DOTALL)
COMPANION_LINKS = {'quick': '#quick', 'deep': '#deep', 'print': '#downloads'}
DESTINATIONS = {
    'daniel.html': {'quick': '#daniel-1', 'deep': 'explore.html', 'print': '#student-print'},
    'lessons/hosea-joel.html': COMPANION_LINKS,
    'lessons/amos-obadiah-jonah.html': COMPANION_LINKS,
}


def render_navigation(source, fragment):
    """Replace only the marked nav, leaving page-specific content byte-for-byte."""
    matches = list(NAVIGATION.finditer(source))
    if len(matches) != 1:
        raise ValueError('expected exactly one <nav class="study-path"> slot')
    match = matches[0]
    return source[:match.start()] + fragment + source[match.end():]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the tracked HTML needs regenerating')
    args = parser.parse_args()
    template = Template(TEMPLATE.read_text(encoding='utf-8').removesuffix('\n'))
    changes = {}
    for route, links in DESTINATIONS.items():
        path = ROOT / route
        original = path.read_text(encoding='utf-8')
        fragment = template.substitute({key: escape(href, quote=True) for key, href in links.items()})
        try:
            generated = render_navigation(original, fragment)
        except ValueError as error:
            parser.exit(1, f'{route}: {error}.\n')
        if generated != original:
            changes[route] = generated
    if args.check and changes:
        parser.exit(1, f'Study navigation is stale: {", ".join(changes)}. Run python scripts/update_study_navigation.py.\n')
    for route, generated in changes.items():
        (ROOT / route).write_text(generated, encoding='utf-8')


if __name__ == '__main__':
    main()
