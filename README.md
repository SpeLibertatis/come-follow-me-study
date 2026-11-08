# Come, Follow Me — Supplemental Study Guides

Privacy-first, unofficial supplemental scripture study experiences for youth. This project is **not affiliated with or endorsed by The Church of Jesus Christ of Latter-day Saints**.

## Deployment status
The existing Daniel edition is available on GitHub Pages. Changes on feature branches are not published until reviewed and merged; retain the security and privacy release checks below.

## Style standard

The approved [repository style standard](STYLE_GUIDE.md) preserves the Daniel prototype's cinematic artwork, ivory reading surfaces and teal discovery sections. The main entry point is an approximately five-minute personal study for ages 13–15: Understand → Read → Notice → Try. Students stay with Daniel 3 throughout, can finish without writing, and can choose extra accounts and deeper readings afterward. The page consumes the shared [design tokens](design/tokens.css). Legacy Adventure and Journal URLs redirect to it. The [original prototype](prototypes/daniel-visual-v1/README.md) remains an archived reference. See the [personal-study verification](design/review/personal-study/README.md). Styling changes do not authorize deployment.

## Privacy design
- No accounts, forms that submit data, databases, analytics, advertising, cookies, or third-party scripts.
- No participant names, emails, religious reflections, or identifiers are collected.
- Reflections, if offered, remain in volatile browser memory and are cleared on reload. No localStorage, sessionStorage, IndexedDB, or service workers.
- All images, fonts, styles, and scripts are first-party and served from the site.
- Scripture resources open as external links; those destinations have their own privacy policies.
- GitHub Pages and network providers may process routine access logs and IP addresses independently of this application.

## Security release gate
Before publishing: inspect all HTML/JS and dependencies; remove external embeds and trackers; enforce restrictive CSP; test both versions on mobile; check accessibility and links; review image rights; verify no participant data leaves the browser; enable HTTPS and repository branch protection.

## Study experience
The A/B chooser has been replaced by the Daniel study edition. The original visual v1 prototype remains an archived reference. No remote analytics or identifying student feedback are collected.
