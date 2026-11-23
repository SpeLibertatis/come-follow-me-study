# Student PDF structure

The six shipped handouts use reviewed PDF 1.7 structure trees. The tags identify the document language and title, headings, paragraphs, reading order, and descriptive link names that point back to the original link annotations. Repeated page furniture and decorative drawing operations are treated as artifacts. Links retain their destinations and hit areas. There is no PDF/UA certification or physical screen-reader-device test; the lesson HTML remains an alternative.

## Reproduce the tags for this batch

The retrofit is tied to the exact original layout. To rebuild these six PDFs from the originals, use Python 3 and `pypdf==6.21.4`:

```sh
originals="$(mktemp -d)"
tagged="$(mktemp -d)"
base=5025bbb8b97c8107a031da65f5c53218f09fbfca
for path in $(git ls-tree --name-only "$base" handouts/); do
  case "$path" in
    *.pdf) git show "$base:$path" > "$originals/${path##*/}" ;;
  esac
done
python scripts/tag_student_pdfs.py "$originals" "$tagged"
```

Each per-page map is keyed to the original file's SHA-256 and describes the meaningful text objects and matching annotations in reading order. Tagging refuses new layouts rather than guessing. If a handout is rebuilt with a changed layout, review the heading hierarchy, reading order, and each link before updating its map and digest. Use an authoring pipeline that exports a real structure tree for new material where practical.

## Verify before replacing handouts

- Run `python tests/verify_pdf_structure.py` from the repo root after putting the candidates in a review checkout. It checks structure roles, MCID and parent tree consistency, and the original link annotations' structure bindings.
- Inspect logical output with `pdfinfo -struct-text handouts/amos-quick-study.pdf` and each other PDF. Headings should occur in teaching order, and link labels should describe what they open.
- Compare page count, page boxes and every link rectangle and destination against the previously published edition. When changing only tags, `pdftotext -layout` text and same-version `pdftoppm -r 150` page renders should also match.
- For full accessibility validation, test the reading and tab order in a compatible PDF viewer with a screen reader. The structural test is not a substitute for a PDF/UA validator or assistive-technology testing.
