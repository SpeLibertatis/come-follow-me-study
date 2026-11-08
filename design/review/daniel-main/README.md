# Exact Daniel v1 replacement

The main page, study.css, study.js, and assets/babylon.svg are copied byte-for-byte from the user-selected local Daniel visual v1 reference. No typography, spacing, control, content, or layout overrides are applied. Adventure and Journal URLs redirect to this single experience.

Validation: full-page browser screenshots match the archived reference pixel-for-pixel at desktop (1440px) and mobile (390px). All four source files were also compared byte-for-byte with the specified local reference. The browser harness passes interaction, keyboard disclosure, modes, history, export fallbacks, exact download content, privacy/storage, CSP, reduced-motion, legacy redirects, and 320–1440px reflow checks. See results.json and desktop.png/mobile.png.

The original prototype's accessibility limitations remain; native-device sharing and screen readers have not been verified. No 200% text compliance claim is made for this exact reproduction.

Run `node design/review/daniel-main/verify.cjs` with PLAYWRIGHT_MODULE pointing to Playwright and optional CHROME_PATH. Artwork provenance and source review remain documented in the prototype README.
