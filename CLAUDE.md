# Goodwill study materials site — notes.goodwillonlinetuition.com

Static site for Rainy Goodwill (Goodwill Tuition Centre, Ernakulam). Address him as "Sir".
Published by GitHub Pages from the `docs/` folder of `main`. Never edit `docs/` by hand: it is generated.

- `generator/data.py` – the catalogue: courses, chapter pages, and every PDF (Drive file id, title, description, date, tag).
- `generator/gen.py` – builds the site: `python3 -I generator/gen.py docs`
- `generator/style.css`, `generator/ex_cashflow.html` – page style and the Cash Flow worked example.
- `generator/state.json` – `checked_until`: UTC time of the last nightly check.

## Nightly update (scheduled task, 10:00 pm IST)

1. Read `generator/state.json`. List PDFs in each Drive course folder created after `checked_until`
   (Google Drive search: `'<folderId>' in ancestors and mimeType = 'application/pdf' and createdTime > '<checked_until>'`, excludeContentSnippets true; follow nextPageToken).
2. Skip a PDF when any of these is true:
   - its Drive id is already in `data.py`;
   - it is a duplicate of a PDF already listed (same title or same questions, e.g. a "(1)"/"(2)" or "Compressed" copy);
   - it is homework without answers, a "qp to solve"/"to solve" file, a scan (CamScanner), or a name like html_viewer / interactive_preview / combined_document;
   - you cannot tell what it covers from its name and its first page.
   Unsolved practice worksheets and original question papers may be added with tag "Unsolved" or "Question paper".
3. For each new PDF, read it with read_file_content (first page is enough) and add a tuple to the right chapter's `pdfs` list in `data.py`:
   `("<drive id>", "<title>", "<one-line description>", "<yyyy-mm-dd of modifiedTime>", "<tag or empty>")`
   - Titles name the textbook and question numbers the way students search: "T.S. Grewal Practical Questions 41, 43 and 45", "CBSE 2026 Board Question 23 – Diwan Ltd.", "Dr. Jayan – Illustration 5".
   - Never put a student's name in a title or description.
   - Descriptions say only what the PDF actually contains. Never invent question numbers.
   - If the chapter does not exist, add a new `ch(...)` block for it with an accurate intro and 4–6 correct "points students often miss". Accounting facts must be textbook-correct; if unsure, leave a point out.
   - If the course does not exist (see folders below), add it to COURSES.
4. Build: `python3 -I generator/gen.py docs`. It must finish without error.
5. Set `checked_until` in `state.json` to the time this run started (UTC, ISO format).
6. Commit and push to `main` with a message like "Nightly update: 3 PDFs added (Cash Flow, Share Capital)". If nothing was new, still update `state.json`, commit and push.
7. End with a short report: how many PDFs were added, to which pages, and which were skipped and why.

## Drive course folders (owner rainytp@goodwillonlinetuition.com)

| Course slug in data.py | Drive folder | Folder id |
|---|---|---|
| cbse-class-12-accountancy | CBSE Plus Two — Class 12 | 1U8J6vaLFoor2X0Bb-qIfBXoLAEgGK2Nk |
| cbse-class-11-accountancy | CBSE Plus One — Class 11 | 1MWob2O_EQpiPiFZnLFTjBPV9VNSQ9ErU |
| kerala-plus-two-accountancy | Plus Two — Kerala State | 1Q5iWgao-oom31o3VmJPbbeofxU578cg6 |
| (not yet on site) kerala-plus-one-accountancy | Plus One — Kerala State | 1YPzVQIplsB8Tn-MM4pHyOWXjS0jG2oBU |
| mgu-bcom-honours-financial-accounting | B.Com Honours (MGU) — 3rd Sem | 12zo3iLOqL5J_AFJbxvv4TnytJk3t8OD5 |
| mgu-bcom-5th-semester | B.Com Honours (MGU) — 5th Sem | 1eABXzjtVXaeF2gFv8O22cLz4kNxuc5ko |
| (not yet on site) mgu-bcom-6th-semester | B.Com Honours (MGU) — 6th Sem | find by title in Drive |
| mumbai-university-bcom-costing | B.Com (Mumbai University) — Costing | 16z4NhDbKOe4ndqwNAZ5TGg0AksDamhiz |
| amity-bba-financial-management | BBA | 1iYKVzmHjSLdLl3EbQjfv2onGaaaHiIlQ |
| (not yet on site) mba-finance | MBA | 111YCjYVXJ4jRHkvwByLU6ICK4hPkiAup |
| (not yet on site) skema-business-school | SKEMA Business School — Paris | 1FoT60aNDeRjCWLJ8Roc0SqqaHMxs2oSa |

## House rules
- Goodwill offers only a PAID demo class. Never write "free class", "free trial" or similar. "Free study materials" is fine.
- Do not promote the paid assessment class.
- Keep the site's look as it is; do not restyle pages.
