# Three-chapter study and library review

November 8, 2026. Feature branch starts at f0ff962 (`improve/personal-study`). Target is `main`; no deployment or merge is authorized.

## Delivered behavior
- A static Daniel 1, 3, 6 sequence, approximately four minutes each, followed by three minutes of synthesis and optional reflection. No time enforcement, scores or input required.
- Optional deep-study disclosures in each chapter; all text available without JavaScript.
- Separate Explore Further exhibit: 14 resources, three source categories, six themes, optional Advanced Research, access labels and secure explicit links.
- Original artwork and shared tokens retained. No new dependencies, network calls, embeds, collection or persistence.
- Reflections remain in memory. Library links open another tab to preserve the current study. Theme selection resets on reload.

## Verification
- `python tests/verify.py`: four tests pass. Written/run first against old code: missing chapter IDs/library files failed as expected, then passed after implementation. Checks static/no-JS content, complete source records, themes, unique IDs and anchor targets, secured external links, absence of external embedded assets and collection APIs.
- `node --check study.js`, `node --check explore.js`: pass.
- `git diff --check`: pass.
- Real browser: study and library checked at actual 320, 390, 768 and 1440 CSS-pixel widths, no horizontal overflow. An early viewport attempt affected the other tab; those readings were discarded and the study was retested in the active tab.
- Keyboard Enter opens chapter deep-study and Advanced Research disclosures and activates theme buttons. Focus moves to completion heading. Empty reflection can finish. Empty copy action provides guidance. Chapter disclosure and opening library in a new tab preserve reflection; reload clears it.
- All six themes exercised. Counts: Babylon 9, pressure 8, furnace 6, lions 7, literary 10, history 10; reset/reload restores 14. Furnace filter correctly reports no matching video in category B. No console warnings/errors seen in tested library flow.
- Static privacy inspection: restrictive CSP including `connect-src 'none'`, no external `src`, no embeddings, no tracking/storage APIs; external `href` links secured. Browser resource-timing enumeration was unavailable in the supported read-only browser scope, so a full network trace is **not** claimed.
- Independent fresh-context code reviewer found no actionable findings; its scope excluded browser and live-source verification.

## Audit interpretation and limits
`audit_project.py . --mode strict` produces actionless-button findings in `premium-audit.json`: it does not follow the separate JavaScript event listeners (including existing reflection handlers), and also scans the archived prototype. These are retained as static false positives, not suppressed or called a clean audit. Live theme buttons and empty-copy control were exercised. Existing share/download branches remain unchanged and were not retested on physical devices.

No screen-reader, physical touch-device, full 200% zoom, forced-colors, offline browser or reduced-motion runtime matrix was run. Reduced-motion and forced-colors CSS are present. No-JS behavior was checked structurally, not by disabling JavaScript in the browser. Time estimates are editorial estimates, not youth usability-study measurements.

## Sources and release review
See [SOURCES.md](SOURCES.md) and [link-checks.json](link-checks.json). Every outbound resource was checked, but four publisher destinations block automated access. Their DOI redirects and matching metadata are verified; full access remains restricted or explicitly unverified. The video introduction was checked against the entire auto-generated YouTube transcript. No transcript or article copies are redistributed.

Review article access in a normal browser before publication. The current draft does not claim every publisher page is freely accessible. Screenshots alongside this report show the phone study and desktop/mobile library.
