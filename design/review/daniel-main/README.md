# Daniel main experience review

The main `index.html` now uses Daniel visual v1 directly: its original artwork, hero composition, section-number rail, editorial reading, account picker, ordered evidence disclosure, and optional reflection. Essential and Deep Study are modes within this single page. The A/B chooser and alternate study implementations are removed; old Adventure and Journal URLs redirect to the main study, with a visible fallback link.

The archived prototype is unchanged. Main-page assets are first-party files at `assets/babylon.svg`, `style.css`, and `app.js`. Shared design tokens are loaded and mapped to the original layout. Small accessibility refinements enlarge controls and privacy information, use dark-surface focus rings, and allow narrow layouts to wrap at enlarged text sizes. No hosting configuration is changed.

## Evidence

[Desktop](desktop.png) · [Mobile](mobile.png) · [Desktop hero](desktop-hero.png) · [Mobile hero](mobile-hero.png) · [Results](results.json)

Browser checks pass for all three accounts with keyboard disclosure; section back/forward; mode switching; exact downloaded reflection text; successful/failed clipboard; successful/unavailable/canceled mocked sharing; clear/reload; no storage or external requests; CSP enforcement; reduced motion; 320/390/768/1440px reflow; 320px reflow at 200% text; both legacy redirects. Desktop and mobile hero screenshots were visually reviewed.

Native-device sharing and screen-reader behavior remain unverified. Mock APIs test application branches, not real device behavior. Publication remains subject to the security/privacy release gate.

## Reproduce

Install Playwright in ignored `.test-tools` as described by the prototype review, or set `PLAYWRIGHT_MODULE` to an existing installation. `CHROME_PATH` overrides the default Windows Chrome path. Run from the repository root:

```text
node design/review/daniel-main/verify.cjs
```

Artwork provenance: the original SVG was authored for Daniel visual v1, contains no external references, and depicts an imagined Babylonian gateway. See the prototype README for source and rights notes.
