---
name: discover
description: Find new job postings with career-ops' zero-token ATS scanner and write them as a CSV that /batch reads, deduplicated against applications.md, dlq.md, postings/ and earlier lists. Use when the user runs /discover or asks to scan for new postings.
argument-hint: [--since N] [--exclude <file.xlsx|file.csv|file.txt> ...] [--location KEYWORD ...] [--no-scan] [--career-ops PATH]
---

# /discover — new postings from the career-ops scanner

All paths are relative to `jobapps/`. This supplements Aly's external target lists; it doesn't
replace them.

1. Run `python tools/discover.py $ARGUMENTS`. Unless the arguments already have `--location`, add
   `--location Canada Montreal Toronto Vancouver Ottawa Quebec Calgary Waterloo` (rows with
   an empty location are kept too): the scanner's own location filter lets most foreign postings
   through, and Aly is looking in Canada. The career-ops folder comes from `--career-ops` or
   the `CAREER_OPS_DIR` environment variable; if neither is set, ask Aly for the path (career-ops
   lives at `C:\Users\alymo\Desktop\Job Search\career-ops` on Aly's machine) and pass it. The scan
   takes a few minutes. Companies, title and location filters live in career-ops' `portals.yml`.
2. If it prints `no new postings`, say so and stop. If it exits non-zero, show its message
   (node missing, career-ops folder missing, scan failed) and stop.
3. Otherwise read the CSV it names and show the count and the first 15 rows
   (rank, company, title, location). Over 60 rows: say so, and suggest batching a slice
   (`--rows 1-40`) rather than the whole list, since every row costs a pre-screen and a score.
4. Suggest the next step: `/batch resume <csv>` or `/batch apply <csv>`; add `--exclude <this
   week's external list>` next time so the two don't overlap. Say that Canada eligibility isn't
   checked yet (the `/batch` pre-screen does it) and that the score gate drops weak fits before
   resumes.
