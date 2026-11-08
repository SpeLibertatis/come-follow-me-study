# Come, Follow Me — Supplemental Study Guides

Privacy-first, unofficial supplemental scripture study experiences for youth. This project is **not affiliated with or endorsed by The Church of Jesus Christ of Latter-day Saints**.

## Deployment status
The student websites are **not deployed**. Publication is blocked pending security and privacy review.

## Style standard

The approved [repository style standard](STYLE_GUIDE.md) establishes the Daniel prototype's cinematic artwork, ivory editorial reading, and teal discovery surfaces as the direction for new and substantially redesigned experiences. Use the shared [design tokens](design/tokens.css) and consult the [reference prototype and review screenshots](prototypes/daniel-visual-v1/README.md). Existing A/B pages require a separately scoped migration; adopting the standard does not merge or deploy changes.

## Privacy design
- No accounts, forms that submit data, databases, analytics, advertising, cookies, or third-party scripts.
- No participant names, emails, religious reflections, or identifiers are collected.
- Reflections, if offered, remain in volatile browser memory and are cleared on reload. No localStorage, sessionStorage, IndexedDB, or service workers.
- All images, fonts, styles, and scripts are first-party and served from the site.
- Scripture resources open as external links; those destinations have their own privacy policies.
- GitHub Pages and network providers may process routine access logs and IP addresses independently of this application.

## Security release gate
Before publishing: inspect all HTML/JS and dependencies; remove external embeds and trackers; enforce restrictive CSP; test both versions on mobile; check accessibility and links; review image rights; verify no participant data leaves the browser; enable HTTPS and repository branch protection.

## A/B testing
Use anonymous, optional, in-person feedback without identifying students or recording individual religious responses. No remote analytics.
