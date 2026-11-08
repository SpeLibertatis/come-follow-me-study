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

## Browser and release checks outstanding
The development container blocks Chromium's required Unix sockets; the provided cloud browser cannot reach the container's local preview. `tests/verify_game.py` is ready but has not run successfully here. Actual mobile/text enlargement, native focus, screenshot, screen-reader, and first-party network behavior must be checked in a usable browser before calling verification complete. GitHub reports main unprotected, while the repository release instructions require branch protection; no protection setting has been changed.
