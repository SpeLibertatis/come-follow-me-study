# Daniel visual exploration v1

Isolated, dependency-free prototype for issue #1. The owner approved this visual direction as the foundation for the [repository style standard](../../STYLE_GUIDE.md). Use that guide and the shared [design tokens](../../design/tokens.css) for new and substantially redesigned experiences. Existing production A/B pages have not been migrated. No deployment, hosting configuration, backend, or production entry points are changed.

## Preview

From the repository root run `python -m http.server 8080 --bind 127.0.0.1`, then open http://127.0.0.1:8080/prototypes/daniel-visual-v1/. Use localhost/loopback rather than file URLs for clipboard support. No build step. This is a local preview, not a deployment.

## Design and artwork

Three connected surfaces: cinematic copper/charcoal Babylon landing, ivory editorial reading with verse-oriented prompts, and dark teal evidence discovery. Georgia and system sans-serif avoid font downloads. The gateway SVG is original artwork authored for this prototype, approximately 4 KB, with an explicit intrinsic size and no external references. It is an imagined atmospheric scene, not an archaeological reconstruction. The hero is eager loaded because it is above the fold; no additional raster downloads, animation loops, or dependencies are needed.

The previous three-phone image was not attached to issue #1 or available in the repository. Comparison is therefore to the issue’s written direction: atmospheric Babylon, monumental type, ivory reading, charcoal/teal exploration. Relative to the baseline’s A/B choice cards, this proposal is a continuous editorial study journey with section navigation and evidence disclosure. Pixel-level resemblance to the unavailable mockup cannot be verified.

## Learning and rights review

Official sources checked November 7–8, 2026:

- [2026 lesson, November 9–15](https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026/46?lang=eng): the specified principle, Daniel 1/3/6, the uncertainty in Daniel 3:17–18, and Alma 14 comparison.
- [Daniel 1](https://www.churchofjesuschrist.org/study/scriptures/ot/dan/1?lang=eng), [Daniel 3](https://www.churchofjesuschrist.org/study/scriptures/ot/dan/3?lang=eng), [Daniel 6](https://www.churchofjesuschrist.org/study/scriptures/ot/dan/6?lang=eng), [Daniel 7](https://www.churchofjesuschrist.org/study/scriptures/ot/dan/7?lang=eng), and [Alma 14](https://www.churchofjesuschrist.org/study/scriptures/bofm/alma/14?lang=eng): chapter/verse references checked against the linked accounts. Food is described as vegetables in an explicitly original summary, not presented as the edition’s verbatim wording.
- [Church terms of use](https://www.churchofjesuschrist.org/learn/legal/terms-of-use/go?lang=eng): republication permission is restricted. No scripture paragraphs, Church artwork, or manual excerpts are reproduced. The requested short lesson principle is attributed and linked; all other study prose is original commentary or summary. Exact scripture reading takes place on the official linked site. No assumed license to reproduce the Church edition.

Discovery begins with a question and reveals command, response, then outcome. No scores, rewards, or obedience competitions. Essential reading emphasizes the friends’ commitment before the outcome—the “but if not” of Daniel 3:18. Particular rescues are never represented as guarantees. Deep study adds Daniel 7 and a sensitive, optional Alma 14 comparison. Chapter context is labeled narrative context, distinct from interpretation; no speculative historical dates are asserted.

## Privacy and security

Only self-hosted HTML, CSS, JS and SVG load. CSP denies connections, forms, objects and everything except explicit self-hosted script/style/image/font resources. No network APIs in application code, account, cookies, storage APIs, analytics, service worker, backend, third-party code, embeds, fonts, or user input HTML injection. Script uses textContent and DOM creation.

Reflection is a textarea in volatile page memory. pagehide clears it, including when leaving for a different page; reload starts empty. Study mode, scene progress and anchors also remain in memory / ordinary fragment history; no reflection enters URLs. Copy/share/download require clicks. Clipboard history, destination apps, downloaded files and backups are outside this page’s control. Unavailable clipboard selects text for manual copy. Unavailable/canceled native share reports status and points to copy/download. Download uses a local Blob and revokes its temporary URL. No reflection data is automatically transmitted.

GitHub Pages, if later approved as hosting, and network providers may log normal requests. Meta CSP cannot enforce frame-ancestors; a future host must supply a response header if anti-framing is required. No hosting settings were changed. External official links are explicit user actions, use no-referrer and noopener/noreferrer, and leave for a site with its own privacy policy.

## Review checks and screenshots

Run the local browser harness from the repository root with Node 18+ and Chrome installed:

```
npm install --prefix .test-tools --no-package-lock --no-audit --no-fund playwright@1.51.1
node prototypes/daniel-visual-v1/review/verify.cjs
```

Playwright is review tooling only, not a shipped runtime dependency. `CHROME_PATH` can override the Windows Chrome path. The harness serves only this prototype on loopback and checks the six flows, keyboard disclosure, back/forward, mode orientation, storage, first-party network requests, input-as-text, CSP enforcement, reduced motion, copy/share fallback branches, and exact text download. See [results](review/results.json), [desktop screenshot](review/desktop.png), [mobile screenshot](review/mobile.png).

Limitations: local timing is not a real-device/Lighthouse score. Native share branches use API mocks; an owner should review actual iOS/Android share sheets, screen-reader announcements, touch/zoom ergonomics and perceived artwork quality before approving. No claim of a complete accessibility audit. Study time estimates are editorial guidance, not timers.

## Versioning and rollback

Original prototype baseline: `3ca4d364117fd7e69909d85b620490cec488d383`. Four prototype checkpoints: shell/tokens; original artwork; interactions/content; security tests/review notes. PR #2 was subsequently merged on GitHub. The style-standard follow-up stays on `design/daniel-rich-visual-exploration` and uses a new draft PR against main. It adopts the owner-approved repository style standard. Production `index.html`, `adventure.html`, `journal.html`, `style.css`, `app.js`, and existing policies remain byte-for-byte unchanged by this work.

To abandon the style-standard follow-up before merge, close its draft PR; the already merged prototype remains. To undo the follow-up after an eventual approved merge, revert that merge or its documentation commit on an authorized branch. The original prototype can separately be reverted through PR #2's merge commit. Do not reset shared main history. This follow-up does not deploy anything or change hosting settings.
