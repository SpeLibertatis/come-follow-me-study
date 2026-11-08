# Daniel study design context

The maintained design specification is [STYLE_GUIDE.md](STYLE_GUIDE.md). The existing runtime tokens in `design/tokens.css` remain canonical; this document does not generate or duplicate them.

## Intent
An independent scripture-study experience for ages 13–15: three scenes of faith under pressure, with room for questions. Preserve the Babylon gateway illustration, ivory editorial reading, dark teal discovery, Georgia headings and Arial interface text.

## Journey and library
- `index.html`: Daniel 1 → 3 → 6 → synthesis/reflection; about 15 minutes, with no timer or participation score. Each chapter offers native optional deep-study disclosure.
- `explore.html`: a separate editorial exhibit. A quiet category rail and theme buttons lead to annotated resources, retaining accurate academic titles rather than replacing them with promotional copy.
- Shared styles belong in `study.css`; exhibit-specific composition in `explore.css`. Native links, buttons and details remain the shared interaction vocabulary.
- Library filter selection stays in memory only, never URL or persistent storage, because reading interests are not collected. Reset is the All resources button; empty categories remain labeled.
- Study-to-library links open another tab to retain the current study page and reflection. No external asset is loaded until a student navigates to a resource.

## Accessibility and restraint
Native keyboard behavior, visible focus, 44px minimum control height, natural document scrolling and 320px reflow. Honor reduced motion. No badges for religious behavior, quizzes that gate completion, autoplay or animated distractions. Full text remains available without JavaScript; export controls need JavaScript.

## Verification
See `design/review/three-chapter/README.md`. Preserve the existing style guide's token mapping and privacy contract when extending the collection.
