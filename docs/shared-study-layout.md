# Shared student study layout

The published lessons are plain HTML. A local Python script renders a few shared regions into them; the browser does not load any generator, template, or new JavaScript.

| Template | Pages | Owns |
| --- | --- | --- |
| `study-header.html` | Daniel, Joel, Amos | Site branding and links back to the archive; Daniel also links to Explore Further. |
| `study-navigation.html` | Daniel, Joel, Amos | Quick study, Go deeper, and Print shortcuts. |
| `study-footer.html` | Daniel, Joel, Amos | Attribution and privacy frame, preserving each lesson's existing copy. |
| `companion-quick.html`, `companion-deep.html`, `companion-print.html` | Joel, Amos | The opening tags and headings through the first `</h2>` for the quick, deeper, and print regions. |

Edit shared markup under `scripts/templates/` and existing page variations in `scripts/update_study_layout.py`. Then, from the repository root:

```sh
python scripts/update_study_layout.py
python tests/verify_routes.py
```

Commit the generated HTML when shared markup or its page settings change. CI checks that the committed HTML is current. Edit each lesson's story, art, scriptures, exercises, download links, and text after a section heading directly in the lesson page. Daniel keeps its distinct lesson body. Not-ready placeholders remain unregistered.

When applying the shared pieces to another published lesson, use the existing `site-header` and `study-path` classes as the first attribute on their tags, one `footer`, and the existing `quick`, `deep`, and `downloads` IDs as the first attribute on section openings if using the companion frame. Register the page in the layout script; it rejects missing or duplicate generated regions rather than inserting markup at an ambiguous position. Keep the markup through each generated heading in the template rather than editing it in the page.
