# Personal study implementation plan

> Execute inline using executing-plans. The user approved the personal-study proposal in chat and requested implementation.

**Goal:** A complete five-minute Daniel 3 study for ages 13–15, with optional deeper reading.
**Architecture:** Retain the static HTML/CSS/JavaScript site, original SVG and private in-memory reflection. Use existing shared tokens; preserve legacy fragment links.
**Tech stack:** Native HTML, CSS and JavaScript; no shipped dependencies.
**Spec:** The accepted chat proposal: Understand → Read → Notice → Try, furnace first, optional exports, clear finish, approachable language.

## Global constraints
- No accounts, trackers, persistence, remote assets or automatic reflection transmission.
- Preserve the original Babylon artwork and mature tone. No scores or streaks.
- Scripture quotation must be attributed and verified; distinguish commentary.
- Keep extra accounts and deeper readings after completion; finishing must not require text or disclosures.

## Tasks
1. Rewrite index.html and study.js for the continuous furnace study, hint, optional reflection exports, completion and post-study exploration. Keep #landing, #reading, #discovery and #reflection working.
2. Refine study.css through design/tokens.css: shorter hero, readable UI type, centered reading measure, 44px controls, responsive layout, visible focus and reduced motion. Update STYLE_GUIDE.md, the existing canonical design document.
3. Verify browser flow, empty completion, reflection preservation while exploring, progressive reveals, keyboard focus, reload clearing, source links, 320/390/1440 reflow and screenshots. Review changes and package a reviewable branch.

## Review focus
- Finishing with an empty reflection must succeed.
- Switching accounts must not overwrite reflection or lose discovered steps.
- Anchor links and focused controls must clear sticky navigation.
- Export controls must stay explicit and show usable empty/error feedback.
- No student text in URLs, requests, logs or persistent storage.

## Validation record
- Baseline: existing site defaults to Daniel 1 and has no finish action; no package-managed test suite. Archived visual-match script targets the superseded v1 composition.
