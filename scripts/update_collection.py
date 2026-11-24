"""Refresh the static latest-study link and order the dated archive cards."""
import argparse
import json
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from string import Template
import re

from shared_header import apply as apply_header

ROUTE = re.compile(r'(?:lessons/)?[a-z0-9-]+\.html\Z')


class CollectionCards(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.html = html
        self.line_offsets = [0, *(match.end() for match in re.finditer(r'\n', html))]
        self.cards = []
        self.card = None
        self.capture = False
        self.feed(html)
        if not self.cards:
            raise ValueError('No dated archive cards found')

    def source_offset(self):
        line, column = self.getpos()
        return self.line_offsets[line - 1] + column

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == 'li' and 'data-week-start' in attrs:
            self.card = {
                'start': self.source_offset(),
                'date': date.fromisoformat(attrs['data-week-start']),
                'ready': False,
                'route': None,
                'title': '',
                'meta': attrs,
                'official': None,
            }
        if self.card is None:
            return
        if tag == 'span' and {'status', 'ready'} <= set(attrs.get('class', '').split()):
            self.card['ready'] = True
        if tag == 'a' and self.card['route'] is None:
            self.card['route'] = attrs.get('href')
            self.capture = True
        elif tag == 'a' and self.card['official'] is None:
            href = attrs.get('href', '')
            if href.startswith('https://www.churchofjesuschrist.org/study/manual/'):
                self.card['official'] = href

    def handle_endtag(self, tag):
        if tag == 'a':
            self.capture = False
        if tag == 'li' and self.card is not None:
            if not ROUTE.fullmatch(self.card['route'] or '') or not self.card['title'].strip():
                raise ValueError('Each dated archive card needs a local study title link')
            self.card['end'] = self.html.index('>', self.source_offset()) + 1
            self.cards.append(self.card)
            self.card = None

    def handle_data(self, text):
        if self.capture and self.card is not None:
            self.card['title'] += text


def order_archive(html, cards):
    # Swap whole cards in place, preserving the surrounding markup and spacing.
    ordered = sorted(cards, key=lambda card: (card['ready'], card['date']), reverse=True)
    parts = []
    previous_end = 0
    for slot, card in zip(cards, ordered):
        parts.append(html[previous_end:slot['start']])
        parts.append(html[card['start']:card['end']])
        previous_end = slot['end']
    return ''.join(parts) + html[previous_end:]


def short(card, name):
    return escape(card['meta'].get(f'data-{name}', ''), quote=True)


def text_title(card):
    return short(card, 'short-title') or escape(card['title'].strip())


def latest_ready(cards):
    return max((card for card in cards if card['ready']), key=lambda card: card['date'], default=None)


def feature(card):
    if not card:
        return ('<section class="dark"><div class="feature-copy"><h1>Come, Follow Me study</h1>'
                '<p>Browse the official readings and study archives.</p></div></section>', '')
    title = short(card, 'feature-title') or text_title(card)
    accent = short(card, 'feature-accent')
    stamp = short(card, 'short-date') or card['date'].isoformat()
    eyebrow = short(card, 'feature-date') or f"{stamp}, {card['date'].year}"
    duration = short(card, 'feature-duration')
    art, wide = short(card, 'feature-art'), short(card, 'feature-art-wide')
    picture = ''
    if art:
        wide_source = f'<source media="(min-width: 54rem)" srcset="{wide}">' if wide else ''
        picture = (f'<figure class="feature-art"><picture>{wide_source}<img src="{art}" '
                   f'width="900" height="600" alt="{short(card, "feature-alt")}" '
                   'fetchpriority="high"></picture></figure>')
    display_title = f'{title} <em>{accent}</em>' if accent else title
    time = f' <span class="duration">{duration}</span>' if duration else ''
    hook = short(card, 'hook')
    hook_html = f'<p class="feature-hook">{hook}</p>' if hook else ''
    credit = short(card, 'feature-credit')
    html = f"""
<section class="dark"><div class="feature{'' if art else ' no-art'}">
{picture}
<div class="feature-copy">
<p class="eyebrow">Latest study · {eyebrow}</p>
<h1>{display_title}</h1>
<p class="feature-meta">{text_title(card)}</p>
{hook_html}
<div class="actions"><a class="cta" href="{card['route']}">Start the study{time}</a><a class="quiet-link" href="#studies">Browse all lessons <span aria-hidden="true">↓</span></a></div>
</div></div></section>"""
    return html.strip(), f'<p>{credit}</p>' if credit else ''


def recent_entry(card):
    title = text_title(card)
    stamp = short(card, 'ready-date') or short(card, 'short-date') or card['date'].isoformat()
    hook = short(card, 'hook')
    hook_html = f'<p>{hook}</p>' if hook else ''
    return (f'<article class="entry"><p class="entry-meta">{stamp} · READY TO STUDY</p>'
            f'<h3>{title}</h3>{hook_html}<a class="entry-link" href="{card["route"]}" '
            f'aria-label="Open student study: {title}">Open student study <span aria-hidden="true">→</span></a></article>')


def official_entry(card):
    if not card['official']:
        raise ValueError(f'Missing official lesson URL: {card["route"]}')
    title = text_title(card)
    stamp = short(card, 'short-date') or card['date'].isoformat()
    return (f'<li><div><span class="calendar-date">{stamp}</span><p>{title}</p></div>'
            f'<a class="quiet-link" href="{escape(card["official"], quote=True)}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="Read official lesson: {title}">Read official lesson <span aria-hidden="true">↗</span></a></li>')


def read_2027(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if data['curriculum_year'] != 2027 or not data['weeks']:
        raise ValueError('The 2027 archive requires 2027 curriculum records')
    cards = []
    for week in data['weeks']:
        start = date.fromisoformat(week['week_start'])
        state = week['status']
        route = week.get('study_path')
        if state not in {'official-only', 'ready'} or not re.fullmatch(r'\d{2}', week['manual_part']):
            raise ValueError('A week needs an explicit publication state and official lesson number')
        if (state == 'ready' and not ROUTE.fullmatch(route or '')) or (state == 'official-only' and route):
            raise ValueError('Only a ready week can declare a local student study route')
        official = ('https://www.churchofjesuschrist.org/study/manual/'
                    f'come-follow-me-for-home-and-church-new-testament-2027/{week["manual_part"]}?lang=eng')
        meta = {f'data-{key.replace("_", "-")}': value for key, value in week.items()}
        meta.setdefault('data-feature-date', week['date_label'])
        meta.setdefault('data-ready-date', week['date_label'])
        meta.setdefault('data-short-date', week['date_label'])
        cards.append({'date': start, 'ready': state == 'ready', 'route': route,
                      'title': week['title'], 'theme': week['theme'], 'meta': meta,
                      'official': official})
    return cards


def archive_2027(cards, template, start):
    has_ready = any(card['ready'] for card in cards)
    archive_intro = ('Open a published student study or go to the Church’s official readings. '
                     if has_ready else 'No student companion is published here for 2027. ')
    archive_intro += f'The Church’s published schedule begins {start}.'
    ordered = sorted(cards, key=lambda card: (card['ready'], card['date']), reverse=True)
    sections = []
    for card in ordered:
        day = card['date'].isoformat()
        title = text_title(card)
        theme = escape(card['theme'])
        label = ('Read the first official lesson' if card['date'] == min(x['date'] for x in cards)
                 else 'Read official lesson')
        study = (f'<a class="entry-link" href="{card["route"]}">Open student study '
                 '<span aria-hidden="true">→</span></a> ' if card['ready'] else '')
        sections.append(
            f'<section class="body-section" aria-labelledby="week-{day}" data-curriculum-year="2027" '
            f'data-week-start="{day}"><p class="eyebrow">{short(card, "feature-date")}</p>'
            f'<h2 class="section-title" id="week-{day}">{title}</h2><p>{theme}</p>{study}'
            f'<a class="quiet-link" href="{escape(card["official"], quote=True)}" '
            'target="_blank" rel="noopener noreferrer">'
            f'{label} <span aria-hidden="true">↗</span></a></section>')
    return template.substitute(archive_intro=archive_intro, weeks='\n'.join(sections))


def render(root):
    archive = (root / '2026.html').read_text(encoding='utf-8')
    cards = CollectionCards(archive).cards
    if any(card['meta'].get('data-curriculum-year') != '2026' for card in cards):
        raise ValueError('The 2026 archive may contain only 2026 curriculum records')
    if len({card['date'] for card in cards}) != len(cards):
        raise ValueError('Archive card dates must be unique')
    next_cards = read_2027(root / 'scripts/collection-2027.json')
    all_cards = cards + next_cards
    if len({card['date'] for card in all_cards}) != len(all_cards):
        raise ValueError('Archive card dates must be unique across curriculum years')
    newest = latest_ready(all_cards)
    recent = sorted((card for card in all_cards if card['ready'] and card is not newest),
                    key=lambda card: card['date'], reverse=True)[:2]
    coming = sorted((card for card in all_cards if not card['ready']
                     and (newest is None or card['date'] > newest['date'])), key=lambda card: card['date'])[:4]
    templates = root / 'scripts/templates/collection'
    first = min(card['date'] for card in next_cards)
    next_start = f'{first:%B} {first.day}, {first.year}'
    new_year = archive_2027(next_cards, Template((templates / '2027.html').read_text(encoding='utf-8')), next_start)
    hero, credit = feature(newest)
    home = Template((templates / 'landing.html').read_text(encoding='utf-8')).substitute(
        feature=hero, credit=credit, next_start=escape(next_start),
        recent=''.join(recent_entry(card) for card in recent) or '<p>No additional student studies are published yet.</p>',
        coming='<ul class="calendar">' + ''.join(official_entry(card) for card in coming) + '</ul>'
        if coming else '<p>No upcoming official readings are listed here.</p>')
    pages = {'index.html': home, 'lessons.html': home,
             '2026.html': order_archive(archive, cards), '2027.html': new_year}
    return {route: apply_header(source, route) for route, source in pages.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the tracked HTML needs regenerating')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    outputs = render(root)
    mismatches = {root / name: value for name, value in outputs.items()
                  if not (root / name).is_file() or (root / name).read_text(encoding='utf-8') != value}
    if args.check and mismatches:
        parser.exit(1, 'Collection is stale. Run python scripts/update_collection.py.\n')
    for path, value in mismatches.items():
        path.write_text(value, encoding='utf-8')


if __name__ == '__main__':
    main()
