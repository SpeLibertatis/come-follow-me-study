# Student quality smoke tests

The PR workflow uses Playwright WebKit on Linux with the iPhone 13 device
profile. It checks navigation, reflow, touch controls and PDF responses. This
is not a physical iPhone or Safari test, and it does not verify PDF rendering.
Chromium runs axe against the collection and published studies, including the
open Daniel game. Axe findings are initially report-only. The job summary
separates violations from inconclusive results; the short-lived JSON artifact
contains affected selectors. Failure to load a page or run the scanner still
fails the smoke job. A clean scan is not an accessibility certification.

Run locally from the repository root with Node, Python 3 and Playwright's
system dependencies installed:

```sh
npm ci --prefix tests/quality --ignore-scripts --no-audit --no-fund
cd tests/quality
./node_modules/.bin/playwright install chromium webkit
npm test
```

The separate weekly external-link workflow runs on the default branch, or by
manual dispatch. Review its Actions job summary before treating 403s, 429s or
timeouts as broken links. It checks external HTTP/S links in published HTML,
not PDF links or physical QR codes, and does not gate pull requests or releases.
