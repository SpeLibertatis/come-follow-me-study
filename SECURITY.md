# Security and privacy policy

## Threat model
Audience includes minors. Primary risks: accidental collection of sensitive religious reflections; third-party trackers and remote assets; script injection; supply-chain compromise; malicious repository changes; external-link phishing; misleading claims of anonymity.

## Required controls
1. Static HTML/CSS/JavaScript only. No server endpoints or form submission.
2. Do not store user input in cookies, localStorage, sessionStorage, IndexedDB, URLs, or logs.
3. Never use eval, Function, innerHTML with user content, dynamic remote code, or untrusted HTML.
4. No analytics, pixels, CDNs, external fonts, embedded videos, or third-party scripts.
5. Self-host licensed imagery; avoid external image requests.
6. Set a restrictive Content Security Policy (prefer separate first-party JS/CSS, no inline script): default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; frame-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests. Note GitHub Pages does not provide arbitrary custom HTTP security headers; meta CSP cannot enforce frame-ancestors.
7. External links use rel="noopener noreferrer" and open only verified domains.
8. Use GitHub branch protection, least-privilege access, 2FA, dependency pinning if dependencies are introduced, and review changes before merging.
9. Test network requests in browser developer tools: only first-party assets on initial load.
10. Avoid collecting identifiable feedback in the A/B test.

## Privacy limitations
A public GitHub Pages site may still produce provider/network access logs (including IP addresses). Links to Church resources leave this site. Do not claim complete anonymity or zero provider data processing.

## Reporting
Please report security concerns privately to the repository owner rather than posting student information in public issues.
