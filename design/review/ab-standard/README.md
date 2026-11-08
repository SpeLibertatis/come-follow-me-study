# A/B style migration review

The comparison and both Daniel study routes now use `design/tokens.css`: original Babylon artwork, ivory editorial reading, teal discovery, serif headings, and visible privacy information. Artwork is reused unchanged from the prototype; its documented origin remains in the prototype README.

Learning purpose: keep the same source readings and distinct routes while inviting observation before interpretation. Adventure remains sequential, now with fragment URLs, focus transfer and browser history. Journal stays freely navigable. Native disclosure introduces pressure, response and outcome in order. Expanded reading uses understated rules. Completion scoring is removed. Optional reflection remains in volatile memory with explicit exports and accessible failure messages.

## Review evidence

- [Comparison desktop](index-desktop.png) / [mobile](index-mobile.png)
- [Adventure desktop](adventure-desktop.png) / [mobile](adventure-mobile.png)
- [Journal desktop](journal-desktop.png) / [mobile](journal-mobile.png)
- [Browser check results](results.json)

Browser checks cover skip-link keyboard focus, Adventure focus and back/forward, ordered disclosure, 320px reflow, 200% text enlargement, first-party assets, failed/unavailable/canceled export APIs, explicit downloads, and reload clearing notes. The comparison desktop and Journal mobile screenshots were visually reviewed. Reduced motion is emulated; smooth scrolling only applies when reduced motion is not requested. CSP remains restrictive with no runtime dependencies added.

Native-device sharing, screen readers, and a full accessibility audit were not performed. Browser API mocks test fallbacks rather than device behavior. Publication remains subject to the security and privacy release gate.

## Reproduce

Install Playwright into ignored `.test-tools` as described in the prototype review, or set `PLAYWRIGHT_MODULE` to an existing installation. Set `CHROME_PATH` if Chrome is not at the Windows default. Run from the repository root:

```text
node design/review/ab-standard/verify.cjs
```

The script serves local files only, saves screenshots/results here, and closes its browser and server on completion.
