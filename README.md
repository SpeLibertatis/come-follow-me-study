# Come, Follow Me: Supplemental Study Guides

A privacy-first, mobile-friendly scripture study companion for youth ages 13–15 and their teachers. The site pairs short reading paths with optional deeper study and printable handouts. It is an independent supplement, **not affiliated with or endorsed by The Church of Jesus Christ of Latter-day Saints**.

[Open the live lesson collection](https://spelibertatis.github.io/come-follow-me-study/lessons.html) · [Repository checks](https://github.com/SpeLibertatis/come-follow-me-study/actions)

## What students can do

| Start here | Experience |
| --- | --- |
| [All lessons](lessons.html) | The reusable QR destination. The homepage presents the same collection. Unpublished lessons link to the official manual. |
| [Daniel](daniel.html) | Read three stories, reflect privately, or try an optional word challenge. Keep a reflection only by explicitly copying, sharing, or downloading it. |
| [Daniel: Explore Further](explore.html) | Browse official sources, commentary, and scholarship. Optional theme filters leave the full library readable without JavaScript. |
| [Hosea and Joel](lessons/hosea-joel.html) | Follow the quick path or open deeper questions about the Lord pouring out His Spirit. |
| [Amos, Obadiah, and Jonah](lessons/amos-obadiah-jonah.html) | Follow the Amos-centered study and consider how the Lord reveals truth through His prophets. |

Student PDFs live in [handouts/](handouts/) and are linked from their lessons. The Daniel handouts can be regenerated using the scripts in [scripts/](scripts/); the Joel and Amos PDFs are checked-in student artifacts.

## How the site is built

- **Static by design.** GitHub Pages serves plain HTML, CSS, JavaScript, WebP illustrations, and PDFs. There is no app server, database, production package install, or runtime build.
- **Progressive enhancement.** The collection, Daniel, and Explore use small first-party scripts where useful. Joel, Amos, and the placeholder lessons do not require JavaScript. See the [design notes](DESIGN.md) and [style guide](STYLE_GUIDE.md).
- **Stable entry points.** Keep `lessons.html` and `index.html` in sync. Keep an existing week's URL when replacing a placeholder. `adventure.html`, `journal.html`, and recognized former Daniel hashes are retained for compatibility.
- **Separate content and art rights.** The [image source and reuse notes](assets/lessons/README.md) describe the Church Media Library assets. Do not assume those rights transfer to other projects.

## Student privacy and tradeoffs

The site does not request accounts, collect personal reflections, run analytics, or fetch third-party assets on page load. Daniel’s reflection remains in the page until a student explicitly copies, shares, or downloads it; clipboard history, files, and receiving apps can retain those copies. The hosting provider and network intermediaries may process routine access logs. External study links open sites with their own privacy practices. Read the [privacy notice](PRIVACY.md) and [security policy](SECURITY.md).

## Verify and update a lesson

1. Preview locally with `python -m http.server 4176 --bind 127.0.0.1`, then open `http://127.0.0.1:4176/lessons.html`. Python and browser dependencies are for development and CI only.
2. Edit the lesson at its existing route. For a newly published lesson, update its card in both collection files. Keep official references, alternate paths, and linked print editions aligned.
3. Run `python tests/verify.py`, `python tests/verify_routes.py`, and `python tests/verify_amos_release.py`. For the PDF suite, install the test dependencies listed in the [CI workflow](.github/workflows/verify-study.yml) and run `python tests/verify_handout.py`.
4. Use `npm ci --prefix tests --ignore-scripts` and `npm test --prefix tests` for the JavaScript interaction suite. With Python Playwright and a supported Chromium binary, set `CHROME_PATH` as needed and run `python tests/verify_game.py` and `python tests/verify_lessons.py`. Review the actual phone and print layouts too.
5. Verify the feature PR checks and review the content before merging. After GitHub Pages deploys, check the live collection, lesson, and student downloads.

The original Daniel visual prototype remains available as a [design archive](prototypes/daniel-visual-v1/README.md).
