# Repository style standard

Version 1.1 · Personal-study refinement · November 8, 2026

## Personal-study refinement

The current main experience serves ages 13–15 studying independently. Its primary job is a complete, approximately five-minute Daniel 3 study: Understand → Read → Notice → Try. The furnace remains the subject throughout. Completion never requires a written reflection, a quiz or opened commentary. Additional accounts and longer passages are optional after the finish point.

Keep the original gateway artwork and existing palette. Use expressive Georgia for the title and scripture, with Arial for instructions and controls. The main page now consumes the canonical `design/tokens.css` directly. The hero token is `clamp(3.75rem, 7vw, 6rem)`; the section-heading token is `clamp(2rem, 3.5vw, 2.75rem)`. Use a centered 700px reading measure instead of the wide section-number rail. On phones, start-study action and time estimate take priority over illustration scale. This refinement supersedes the larger typography, rail layout and Essential/Deep Study selector described in the v1 reference below; the prototype remains archived.

Use at least 14px for supporting privacy and source text, 16px for body/controls and 44px interactive targets. Exports sit behind “Keep my reflection”; Finish study remains available independently. Preserve progress in optional accounts during the current page session. No persistence, automatic sharing or gamification.

Daniel 3:17–18 is reproduced from the historic King James text (public domain in the US), with chapter/verse attribution and an official source link. The wording was checked against the linked text; no Church annotations or edition-specific footnotes are reproduced. Story summaries and interpretation remain explicitly distinguished from scripture.

The Daniel visual exploration is the visual foundation for new and substantially redesigned study experiences in this repository. This standard adopts its cinematic artwork, editorial reading surfaces, and deliberate discovery interactions. It does not authorize merging, deployment, or a wholesale restyling of the existing A/B pages.

Use this guide with [SECURITY.md](SECURITY.md) and [PRIVACY.md](PRIVACY.md). Privacy, accessibility, source accuracy, and clear learning are design requirements. The [Daniel prototype](prototypes/daniel-visual-v1/index.html) is the reference composition; its [screenshots](prototypes/daniel-visual-v1/review/) show the approved visual direction, not proof that every detail has passed an accessibility audit.

## Design character

Build a quiet, mature scripture study experience. Give each lesson a recognizable visual setting, one compelling question, and a clear route through reading, discovery, and optional reflection. Use large type, generous space, restrained borders, and a limited palette. Avoid an endless grid of interchangeable cards, ornamental dashboards, scores, streaks, or rewards for religious behavior.

Compose three complementary surfaces:

| Surface | Purpose | Treatment |
| --- | --- | --- |
| Cinematic opening | Establish place and the central question | Original atmospheric artwork, dark overlay, large ivory serif heading, one copper emphasis, one primary action |
| Editorial reading | Support careful attention to the source | Warm ivory, dark ink, narrow reading measure, verse references, understated rules and margin notes |
| Discovery | Invite observation before explanation | Charcoal/teal ground, warm text, copper selection marker, ordered disclosure and clear source links |
| Reflection | Offer an unhurried personal response | Muted ivory surface, visible label, open writing area, adjacent privacy explanation and explicit export controls |

The lesson’s artwork and question may change. Preserve the hierarchy and reading rhythm instead of copying Babylon into unrelated lessons.

## Color and reusable tokens

[design/tokens.css](design/tokens.css) is the canonical, dependency-free token source for new work. Import it with a local stylesheet link before page-specific CSS. Its `--cfm-` names avoid collisions with existing pages. The file declares variables only; it does not style elements or change pages that do not load it.

| Token | Value | Use |
| --- | --- | --- |
| `--cfm-color-ink` | `#242923` | Main text on light surfaces |
| `--cfm-color-paper` | `#f4f0e7` | Editorial background |
| `--cfm-color-reflection` | `#e9e5da` | Reflection section |
| `--cfm-color-field` | `#f6f3ec` | Writing surface |
| `--cfm-color-teal` | `#163e3e` | Primary actions and selected study mode |
| `--cfm-color-discovery` | `#142e30` | Discovery background |
| `--cfm-color-on-dark` | `#f3eee3` | Primary discovery text |
| `--cfm-color-muted-on-dark` | `#d2d9d2` | Supporting discovery text |
| `--cfm-color-gold` | `#dbb383` | Accent and selected indicator on dark surfaces |
| `--cfm-color-fire` | `#efbc88` | Hero emphasis on a dark overlay |
| `--cfm-color-line` | `#c9c4b8` | Decorative light-surface rules |
| `--cfm-color-line-on-dark` | `#607574` | Decorative dark-surface rules |
| `--cfm-color-focus` | `#b56d27` | Focus ring on light surfaces |
| `--cfm-color-focus-on-dark` | `#efbc88` | Focus ring on dark surfaces |

Gold and copper are accents on dark surfaces, not small text colors on ivory. Decorative rules are not sufficient boundaries for form fields or sole indicators of state. Use the stronger control-border token for light-surface inputs. Verify contrast in the actual composition: at least 4.5:1 for normal text, 3:1 for large text and meaningful control indicators. Artwork overlays must preserve readable contrast at every crop. Selected states need a second cue, such as an underline, border, radio mark, or text label.

## Typography

Use self-hosted system font stacks: Georgia, Times New Roman, serif for expressive headings and reading; Arial, Helvetica, sans-serif for navigation, labels, controls and supporting information. No remote font requests. Any future bundled font requires a recorded redistribution license and performance review.

| Role | Starting point | Guidance |
| --- | --- | --- |
| Hero | `--cfm-type-hero`, about 76–136 px | Normal-weight serif, tight leading; adapt size and line breaks to the actual title |
| Section heading | `--cfm-type-heading`, about 42–66 px | Serif, 1.08 leading, restrained negative tracking |
| Discovery heading | `--cfm-type-subheading`, 34 px | Serif, comfortable separation from its source label |
| Reading / introduction | `--cfm-type-reading`, 20 px | Serif, 1.65 leading, approximately 45–70 characters per line |
| Body / controls | `--cfm-type-body`, 16 px | Sans-serif, 1.65 body leading |
| Metadata | `--cfm-type-meta`, 12 px | Short labels only; never the size for required learning or privacy instructions |

Use rem-based sizes and fluid headings. The prototype’s smaller decorative labels are not a mandate to make controls or privacy text tiny. Content must remain usable at 200% text zoom and reflow at a 320 CSS-pixel viewport. Avoid fixed-height text containers and line breaks that truncate longer lesson titles. All-caps tracking belongs to short eyebrows and section markers, not paragraphs.

## Layout and responsive behavior

Use the shared spacing scale: 4, 8, 12, 16, 24, 32, 48, 64 and 96 px, expressed in rem. Prefer 48 px section spacing on small screens and 96 px on wide screens. Use fluid side gutters from 24 to 96 px and a reading width of approximately 700 px. Adjust for legibility rather than treating these as rigid dimensions.

On wide screens, pair a quiet section-number rail with the main reading column; the Daniel reference uses a 1:3 grid. Below approximately 700 px, stack the rail above the content. Let controls wrap and keep their labels complete. A sticky section navigation may provide orientation, but must not cover focused controls or anchor targets. Use a scroll offset that accounts for its actual height.

The hero may be expansive, but the first question and action must remain discoverable. Crop artwork intentionally for narrow screens; keep faces, symbols and text from competing. Do not put essential content solely inside an image. Do not force every lesson into identical viewport-height panels.

## Artwork

Create original, self-hosted assets with a lesson-specific composition and a documented origin. SVG is preferred for architectural, symbolic and atmospheric illustration; optimized raster images are appropriate when they materially improve the scene. Do not copy Church or third-party artwork without a verified license. Label imagined scenes when they could be mistaken for historical reconstructions.

Provide intrinsic image dimensions, useful alt text for meaningful images, and empty alt text for purely decorative images. Keep external references and scripts out of SVGs. Load the above-the-fold hero eagerly; lazy-load appropriate below-the-fold imagery. Use responsive raster sizes when needed. The Daniel SVG is about 3.3 KB; preserve that economy where practical rather than adopting a large image library or animation framework.

## Components and interaction

- **Masthead:** compact study identity and lesson/chapter orientation. An independent, supplemental identity must be clear; do not imitate an official Church product.
- **Primary action:** one obvious next step per section. Use a solid teal action on ivory, or ivory on the dark hero. Prefer direct verb labels. Keep secondary actions visually quieter and links recognizable.
- **Study length:** labeled native radios in a fieldset, with time estimates in text. Switching between Essential and Deep Study must preserve the current section and reflection. Keep the optional expanded reading clearly identified.
- **Section navigation:** semantic links with useful fragment URLs, visible current-location state, keyboard focus, and native back/forward behavior. Reflection content never belongs in a URL.
- **Reading:** show accurate chapter and verse ranges beside official-source links. Separate scripture quotation, original summary, narrative context and interpretation through explicit labels, not just color or typography. Link to exact text instead of reproducing text whose rights or accuracy are uncertain.
- **Discovery:** begin with an observation question and source. Reveal evidence before explanation. Where appropriate, disclose command, response and outcome in order using native details/summary. Preserve useful progress when switching accounts. No timed pressure, points, celebratory rewards or guaranteed-miracle framing.
- **Reflection:** optional, visibly labeled textarea, with nearby plain-language privacy information. Keep text only in volatile memory; clear on reload/page exit. Use `autocomplete="off"` and `spellcheck="false"` as additional browser hints. Copy, native share and plain-text download require explicit actions; explain clipboard, destination-app and device-file privacy. Report unavailable, canceled and failed actions with accessible status text and a usable fallback.

Use native buttons, links, radios, details and textareas before inventing widget roles. Aim for at least 44 × 44 CSS-pixel touch targets for interactive controls. Preserve a visible focus ring, using the appropriate light/dark token, and a logical keyboard order. Announce action results with a status region. Never use color alone for meaning.

## Motion, privacy and learning fidelity

Motion should communicate orientation or a deliberate state change. No autoplay loops, parallax, flashing effects, or motion required to understand content. Honor `prefers-reduced-motion: reduce`, including turning smooth scrolling off. A still illustration is an acceptable default.

Keep experiences static and dependency-free unless a documented need justifies an exception. Retain restrictive CSP, first-party assets, no analytics or automatic reflection transmission, and the controls in the security/privacy policies. Explain that external official links leave the site and that hosting providers may log ordinary requests. Styling must never hide these notices or turn export into automatic saving.

Write in a mature, invitational voice. Questions should invite discovery rather than test personal worthiness. Distinguish narrative outcomes from universal promises. Make room for uncertainty, grief, and the Daniel 3:18 principle that faith is not conditional on rescue. Verify sources and rights for each new lesson; the Daniel review is not blanket permission for future material.

## Applying and reviewing the standard

New study pages and substantial redesigns should use these tokens and patterns. The main study now uses the Daniel visual v1 composition directly; the former A/B URLs redirect to that experience. The prototype remains a reference implementation; later refinements for contrast, readable labels and touch targets take precedence over copying its CSS verbatim.

For visual changes, include mobile and desktop screenshots plus a short explanation of the learning purpose. Check keyboard navigation, focus, 320 px reflow, zoom, reduced motion, source labels, asset loading and privacy/export fallbacks as relevant to the change. Validate actual contrast over artwork. Record native-device and screen-reader checks honestly; mocked browser APIs are not device evidence. Do not repeat unrelated checks for documentation-only changes.

Update this guide and shared tokens together when changing the standard, and explain the change in the PR. Keep commits reversible. Owner approval of a visual direction does not by itself authorize merging or deployment.
