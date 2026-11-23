# Daniel study design context

The maintained design specification is [STYLE_GUIDE.md](STYLE_GUIDE.md). The existing runtime tokens in `design/tokens.css` remain canonical; this document does not generate or duplicate them.

## Intent
An independent scripture-study experience for ages 13–15: three scenes of faith under pressure, with room for questions. Preserve the Babylon gateway illustration, ivory editorial reading, dark teal discovery, Georgia headings and Arial interface text.

## Journey and library
- `daniel.html`: Daniel 1 → 3 → 6 → synthesis/reflection; about 15 minutes, with no timer or participation score. Each chapter offers native optional deep-study disclosure.
- `explore.html`: a separate editorial exhibit. A quiet category rail and theme buttons lead to annotated resources, retaining accurate academic titles rather than replacing them with promotional copy.
- Shared styles belong in `study.css`; exhibit-specific composition in `explore.css`. Native links, buttons and details remain the shared interaction vocabulary.
- Library filter selection stays in memory only, never URL or persistent storage, because reading interests are not collected. Reset is the All resources button; empty categories remain labeled.
- Study-to-library links open another tab to retain the current study page and reflection. No external asset is loaded until a student navigates to a resource.

## Accessibility and restraint
Native keyboard behavior, visible focus, 44px minimum control height, natural document scrolling and 320px reflow. Honor reduced motion. No badges for religious behavior, quizzes that gate completion, autoplay or animated distractions. Full text remains available without JavaScript; export controls need JavaScript.

## Verification
See `design/review/three-chapter/README.md`. Preserve the existing style guide's token mapping and privacy contract when extending the collection.

## Optional word challenge
The lion-marked disclosure near the footer is a separately requested Easter egg, not part of completing the study. Eight clue-based word puzzles use native buttons and a polite status region. No timer, lost lives, score, religious-behavior reward, or persistence. The existing study keeps its quiet, ungated flow. `game.css` owns only this disclosure’s layout and consumes the same runtime tokens. `game.js` owns volatile game state; keyboard letter shortcuts apply only within the open disclosure.

## Year-end collection and Joel companion
- `index.html` and the root are the lesson collection and shared brand destination. `lessons.html` retains the same collection for compatibility. Bare legacy QR codes now intentionally land on the collection; known Daniel fragments forward to `daniel.html`.
- `lessons/hosea-joel.html` is a mobile-first Joel 2:28 companion, not a replacement for the official weekly lesson. It has a four-step quick path and four native optional deep modules.
- Joel uses canonical ivory/teal/gold tokens and Georgia/Arial typography. Its large, quiet promise-led opening replaces Babylon imagery; no new animation or game. `joel.css` supplies the narrative styles shared by Joel and Amos. `amos.css` overrides the Amos-specific artwork and hero treatment.
- No personal input, account, tracking, persistence, remote embeds or JavaScript. Responses stay in students’ own notebooks. Church sources are primary; optional Scripture Central commentary is labeled nonofficial.

## November 15 design reevaluation — candidate, pending user review
The user requested Daniel-level visual care rather than a basic Joel page. The collection is an editorial cover and chronological gallery, retaining all principle-led Church images and credits from PR #14 without cropping or alteration. Daniel remains first and obvious, but is not the global site identity.

Joel uses an original symbolic rain/fields SVG, a cinematic promise-led opening, narrow ivory reading, a dark-teal deeper-learning scene and muted finish. Signature imagery is Joel-specific, not Babylon reused. Original illustration and book/light favicon were authored as SVG in this change; neither reproduces Church branding. All color/type map to `design/tokens.css`. No motion, tracking or input was added.

Header owner: `site.css`, icon + independent study identity + All lessons. Page-specific study-path navigation stays separate. Collection owner: `collection.css` over existing `lessons.css`; Joel owner: `joel.css`.

Candidate template boundaries: shared identity, path selector, read/notice/try sections, optional resources, downloads and mobile behavior. These are proposed patterns, not an approved final template. Do not propagate the Joel redesign to Daniel or future lessons until the user approves the candidate.
