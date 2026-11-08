# Optional Daniel word challenge review

## Learning purpose and changes
A discreet, original line-art lion opens eight optional word puzzles from Daniel 1, 3, and 6. The existing lesson can be completed without opening the game. Unlimited guesses, letter hints, answer reveal, and skip/restart controls avoid pressure or scoring religious behavior. Uses the existing palette, type, native disclosure, and first-party assets.

## Automated checks
- `python tests/verify.py`: 4 passed, including game.js in the no-collection checks.
- `python tests/verify_handout.py`: 3 passed; handout files unchanged.
- `node --check study.js`, `node --check explore.js`, `node --check game.js`: passed.
- `NODE_PATH=/tmp/daniel-game-test/node_modules node --test tests/verify_game.cjs`: 9 passed. Covers all eight puzzles, misses/repeated guesses, hints, reveal, skip/restart, keyboard scope/modifiers/IME, page-exit/reload reset, missing-script fallback, and completion focus.
- `git diff --check`: passed.
- The static UI audit reports the existing 20 findings plus 3 new button-binding false positives. It only recognizes inline handlers, while CSP requires external listeners. All three new buttons have tested listeners in game.js. Existing textarea resizing is owned by study.css. The audit does not establish runtime accessibility.

## Review findings addressed
An independent review found two accessibility issues: disabling a focused hint/reveal control, and fixed alphabet columns/long word groups under 200% text enlargement. Completion now places focus on the next-word control; a regression test failed first and now passes. Alphabet columns respond to available width, and long letter groups may wrap. Browser regression cases are included.

## Browser and release verification
The real Chromium suite passed in [GitHub Actions run 42502211624](https://github.com/SpeLibertatis/come-follow-me-study/actions/runs/42502211624): 11 browser tests plus the 9 DOM, 4 repository, and 3 handout tests. This includes 320px reflow, 44px targets, 200% text within the game, reduced-motion behavior, native completion focus, keyboard isolation, missing-script fallback, reload, no storage, and no unexpected or third-party network requests. Screenshots were inspected after download from the workflow artifact.

- [Desktop game](desktop-game.png)
- [320px discovery viewport](mobile-discovery-viewport.png)
- [320px controls viewport](mobile-controls-viewport.png)
- [320px controls with 200% text](mobile-enlarged-controls-viewport.png)

Full-element captures of a tall section can place fixed navigation in misleading locations, so the mobile review uses actual viewport screenshots. The new game reflows at enlarged text; the existing study navigation is unchanged. No physical-device or screen-reader pass is claimed.

The owner enabled an active default-branch protection rule on November 8, 2026 that blocks deletion and force pushes. GitHub now reports main as protected. This change is released through the reviewed pull request.

## Reproducibility note
Action versions and direct development dependencies are pinned; npm transitive packages have a lockfile. The GitHub-hosted runner, system Chrome, Node version, and Python transitive dependencies can change between runs. This is a maintenance consideration, not a runtime dependency of the study.
