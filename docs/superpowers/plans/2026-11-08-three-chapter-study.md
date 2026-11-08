# Daniel three-chapter study implementation plan

> Execute inline with superpowers:executing-plans. User authorized implementation and a PR against main on feature/daniel-three-chapter-study.

**Goal:** A cohesive 15-minute Daniel 1, 3, and 6 study plus optional deep study and Explore Further library for ages 13–15.

**Architecture:** Static HTML provides all essential reading without JavaScript. Existing tokens, original artwork, native disclosures and volatile reflection controls remain canonical. A separate static library has an in-memory theme filter; no tracking or external assets.

**Tech stack:** HTML, CSS, dependency-free JavaScript; Python standard-library structural checks and browser verification.

**Spec:** User's Explore Further brief and branch/scope clarification, captured below.

## Constraints and design
- Branch from improve/personal-study; open PR to main, no merge or deploy.
- Three four-minute chapters plus three-minute synthesis/reflection; no timers or completion gating.
- Each chapter: context, KJV text, observation question, optional hint/interpretation, outcome and application; deep study is a native disclosure.
- Library is a separate exhibit with three authority categories, six theme filters, detailed source records and optional Advanced Research notes. A separate page preserves the essential journey's independence better than an inline long bibliography. Links from study open a new tab so the current reflection is not lost.
- Scripture and authoritative Church teachings remain primary. Independent commentary and scholarship are labeled; distinguish narrative, historical evidence, proposals, Church teachings, uncertainty.
- Verify metadata/content/access; document failed checks honestly. Do not infer video content from title alone.
- No external embeds, remote imagery, fonts, scripts, storage, reading history, engagement collection or automatic requests. External links require action and noopener noreferrer.
- Keep the existing ivory/teal palette, Georgia headings, Arial controls and Babylon gateway artwork. Use an editorial exhibit of annotated resources, not an interchangeable card grid.

## Review focus
No JavaScript; keyboard disclosures/filter; narrow layout with long titles; empty reflection completion; no automatic third-party requests or retained reflection/filter history.

## Tasks
- [x] 1. Add and run structural/security tests; replace five-minute study with the three-chapter sequence while retaining explicit reflection exports. Test chapter links, source attribution, all essential content present without JS, finish independent of library.
- [x] 2. Verify each resource; implement explore.html, explore.css and explore.js. Every record has author, publisher/type, chapters, introduction, question, access and secured external link. Test six themes and all records, no-results feedback, no persistence.
- [x] 3. Browser checks for both pages at 320/390/768/1440 widths, keyboard, filter/reset, disclosures, reflection preservation/clearing, empty exports and privacy. Capture screenshots, run strict UI audit and syntax/whitespace checks.
- [x] 4. Independent review, resolve findings, update source-verification and README/privacy/style documentation, commit and push this branch; open draft PR against main with honest verification limits.

## Execution ledger
- Baseline f0ff962; clean worktree, study.js syntax passes. Local Git clone hit a Windows shell error; copied the clean repository into this task's work directory, preserved history and remote, then created the requested branch. Original checkout unchanged.

- Implementation and independent review complete; four offline tests and both JS syntax checks pass. Browser, source-access limits, and static-audit false positives recorded in design/review/three-chapter/README.md. Preparing the authorized draft PR; no deployment.
