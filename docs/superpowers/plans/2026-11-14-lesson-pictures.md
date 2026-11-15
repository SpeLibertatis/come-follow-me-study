# Lesson picture implementation plan

**Goal:** Add engaging pictures for ages 13–15 to the seven existing lesson landing-page entries, selected from the principle marked with the seminary icon.

**Architecture:** Static figures in the existing ordered list; local responsive WebP assets; existing design tokens and navigation. Keep images complete and include a source credit and explanatory caption. Preserve the site’s personal, noncommercial, unofficial status and first-party-only requests.

**Design:** Keep the ivory/teal palette, Georgia headings, Arial body, 50rem page measure and chronological rows. Use a 13rem picture column beside text on desktop and stack pictures below text on small screens. An image for each marked principle makes the whole calendar useful; a single hero would not cover the user's requested lesson-specific principles. A new card grid would unnecessarily change the established navigation layout.

**Files:** `lessons.html` and `lessons.css` own the presentation; `assets/lessons/` owns optimized images, source manifest and permission notes. Existing lesson and study pages remain the link destinations.

- [x] Inspect current content, shared styles, privacy constraints and the seven official marked headings.
- [x] Check image-specific download permissions, download official media, inspect all seven scenes, and resize without cropping.
- [x] Add figures, marked principles, captions, source links, responsive styling, intrinsic dimensions, alt text and lazy loading.
- [x] Run repository checks, real-browser reflow/navigation/privacy checks, image-failure checks and desktop/mobile visual review.
- [x] Review the complete diff, commit on a feature branch and open a PR without merging.

**Review focus:** Accurate principle-to-image mapping; full composition visible; all seven lesson destinations unchanged; no external asset requests; readable captions at 320px and enlarged text; usable navigation if images fail. Existing browser checks cover navigation/reflow; an additional one-off preview verifies loaded image dimensions, failure fallback, responsive selection and network requests.
