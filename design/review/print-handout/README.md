# Printable handout verification - 2026-11-08

- Two Letter pages rendered and visually inspected: no clipped text or split chapters; black-and-white text and vector QR, with writing space.
- QR decoded from rendered page 1 with zxing-cpp: https://spelibertatis.github.io/come-follow-me-study/ (no query parameters).
- Six checks pass: four existing privacy/structure tests and two new PDF/link tests.
- Local PDF URL returns bytes identical to the committed artifact; deterministic regeneration checked.
- Browser checked: download links visible on study and library, retaining established styling.
- Independent review found no actionable issues.
- No form fields or student data in the PDF; no new runtime dependencies or external assets.
- Changes prepared on feature/daniel-print-handout for review; no merge or deployment performed.

## Explore Further companion

- Separate six-page PDF includes all 14 library resources, their source/author/chapter metadata, introductions, questions, access notes and original source URLs. Advanced Research distinctions and source caveats are retained.
- All six pages rendered and inspected; page 3 QR decoded to the direct Explore Further URL.
- Seven tests pass, including matching every resource and link against the existing verified HTML library.
- Static local PDF links on both entry pages; no embedded content, tracking or personal notes.
- Independent review of all six companion pages and source changes found no substantive issues.
