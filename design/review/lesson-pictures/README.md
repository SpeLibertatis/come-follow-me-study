# Lesson picture review

November 14, 2026. Scope: seven images on `lessons.html`, each connected to the official lesson's seminary-icon principle. Rebased onto the newly merged Joel companion (PR #13); its Ready status, guide note and brand navigation are preserved. Existing lesson destinations, ready/not-ready labels, shared tokens, restrictive CSP and first-party-only asset loading are preserved.

## Previews

- [Desktop, 1280px](lessons-1280.jpg)
- [Mobile, 390px](lessons-390.jpg)

Full compositions and source credits are visible. At narrow widths, text precedes each picture so lesson access remains first. Source and principle links open the Church website only when selected. See [image permissions and selection rationale](../../../assets/lessons/README.md) and [source manifest](../../../assets/lessons/sources.json).

## Validation

- `python tests/verify.py`: 4 tests passed.
- `python tests/verify_lessons.py` with local Chrome: 14 tests run, 13 passed, 1 optional game screenshot test skipped because `DANIEL_SCREENSHOT_DIR` was not set. Includes inherited game checks, lesson/back navigation, skip link, 320–1280px reflow and 200% text checks.
- `node --check study.js` and `node --check explore.js`: passed.
- Additional local browser inspection: all seven images decoded at 1280px, 390px and 320px; no horizontal overflow; all requests first-party; all original header and lesson links unchanged; CSP unchanged; Daniel link usable with every WebP request blocked.
- Desktop and full mobile screenshots inspected visually; all seven source images inspected before use.
- `git diff --check`: passed. Independent code review found no blockers.

Small renditions total 148,900 bytes; larger renditions total 544,968 bytes. Each image has a 320/640px responsive pair, explicit dimensions and asynchronous decoding. Six images are lazy-loaded. No production dependency or build step was added.

## Review and rollback

The feature branch is review-only; this change does not merge or publish the site. Revert the single feature commit (or its eventual squash merge) to restore the prior landing page. Image rights remain with their respective owners and permit this personal, noncommercial use; reassess permission before changing that use.
