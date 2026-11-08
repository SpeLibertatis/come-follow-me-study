# Come, Follow Me — Supplemental Study Guides

Privacy-first, unofficial supplemental scripture study experiences for youth. This project is **not affiliated with or endorsed by The Church of Jesus Christ of Latter-day Saints**.

## Deployment status
The existing Daniel edition is available on GitHub Pages. Changes on feature branches are not published until reviewed and merged; retain the security and privacy release checks below.

## Style standard

The approved [repository style standard](STYLE_GUIDE.md) preserves the Daniel prototype's cinematic artwork, ivory reading surfaces and teal discovery sections. The main entry point is an approximately 15-minute journey through Daniel 1, 3, and 6 for ages 13–15, ending in a shared reflection. Students can finish without writing or opening optional material. Each chapter has a deeper-study disclosure. [Explore Further](explore.html) is a separate curated library with six themes, three source categories and Advanced Research notes. The pages consume the shared [design tokens](design/tokens.css). Legacy Adventure and Journal URLs redirect to the study. The [original prototype](prototypes/daniel-visual-v1/README.md) remains archived. See [current verification](design/review/three-chapter/README.md) and [source checks](design/review/three-chapter/SOURCES.md). Styling changes do not authorize deployment.

Run offline checks with `python tests/verify.py`, `node --check study.js`, and `node --check explore.js`. Preview using `python -m http.server 4176 --bind 127.0.0.1`. There are no runtime dependencies or build step.

## Privacy design
- No accounts, forms that submit data, databases, analytics, advertising, cookies, or third-party scripts.
- No participant names, emails, religious reflections, or identifiers are collected.
- Reflections, if offered, remain in volatile browser memory and are cleared on reload. No localStorage, sessionStorage, IndexedDB, or service workers.
- All images, fonts, styles, and scripts are first-party and served from the site.
- Scripture resources open as external links; those destinations have their own privacy policies.
- GitHub Pages and network providers may process routine access logs and IP addresses independently of this application.

## Security release gate
Before publishing: inspect all HTML/JS and dependencies; remove external embeds and trackers; enforce restrictive CSP; test both versions on mobile; check accessibility and links; review image rights; verify no participant data leaves the browser; enable HTTPS and repository branch protection.

## Study experience
The A/B chooser has been replaced by the Daniel study edition. The original visual v1 prototype remains an archived reference. No remote analytics or identifying student feedback are collected.

## Printable student handout

[Download the two-page student PDF](handouts/daniel-student-handout.pdf). It contains the three essential scripture readings, context, questions, writing space, and a static QR code to the public study URL. Print on Letter paper, or choose Fit for A4; optional double-sided printing uses the long edge. No phone is needed to complete it. The PDF never includes browser reflections and loads only when selected.

To regenerate after changing lesson content, install the development-only `reportlab` package and run `python scripts/build_handout.py`. Install `pypdf` and run `python tests/verify_handout.py` to check the PDF and its page links. Recheck both rendered pages and decode the QR before publishing. These packages are not shipped to students.

[Explore Further print companion](handouts/daniel-explore-further.pdf) is a separate, optional six-page library: official sources (pages 1–2), video and theme guide with QR (page 3), scholarship (pages 4–5), and Advanced Research (page 6). Print only the pages you need. It includes all 14 resource introductions, questions, access notes, and readable clickable source links; full external articles and video still require access to their publishers. Regenerate with `python scripts/build_explore_handout.py`; the handout checks cover both PDFs.

## Hidden Daniel word challenge

Near the bottom of the study, tap the small lion and “A quiet lion is hiding here…” to open eight short word puzzles based on Daniel 1, 3, and 6. [Jump to the lion](https://spelibertatis.github.io/come-follow-me-study/#lions-den). Students may guess, reveal a letter, show an answer, or skip freely. The game is optional, with no timer, lost lives, scores, accounts, or saved progress. It never gates lesson completion.

Development-only interaction tests: install `jsdom@26.1.0` outside the site (`npm install --prefix /tmp/daniel-game-test --cache /tmp/daniel-npm-cache jsdom@26.1.0`), then run `NODE_PATH=/tmp/daniel-game-test/node_modules node --test tests/verify_game.cjs`. Also run `node --check game.js`. The optional Chromium browser suite is `python tests/verify_game.py`; it needs Python Playwright and a supported local Chromium installation. These test dependencies are never served to students.

The GitHub Actions verification workflow runs the same checks plus real Chromium interactions, narrow-screen layout, enlarged text, and screenshot capture. Run `npm ci --prefix tests` then `npm test --prefix tests` for the pinned DOM-test setup. Set `CHROME_PATH` if Chromium is installed elsewhere. No workflow has write permissions to the repository.
