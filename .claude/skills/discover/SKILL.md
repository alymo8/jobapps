---
name: discover
description: Find new job postings with career-ops' zero-token ATS scanner and write them as a CSV that /batch reads, deduplicated against applications.md, dlq.md, postings/ and earlier lists. Use when the user runs /discover or asks to scan for new postings.
argument-hint: [--since N] [--exclude <file.xlsx|file.csv|file.txt> ...] [--location KEYWORD ...] [--no-scan] [--career-ops PATH]
---

# /discover — new postings from the career-ops scanner

All paths are relative to `jobapps/`. This supplements the user's external target lists; it doesn't
replace them.

1. Run `python tools/discover.py $ARGUMENTS`. Unless the arguments already have `--location`, add
   `--location <discover_locations…>` (the list from `config.local.json` `discover_locations`;
   rows with an empty location are kept too) when that key is set, else no location filter: the
   scanner's own location filter lets most postings through, so `discover_locations` narrows them.
   A missing `config.local.json` means every key is absent (discover does not need the file). The
   career-ops folder comes from, in order, the `--career-ops` argument, the `CAREER_OPS_DIR`
   environment variable, then `config.local.json` `career_ops_dir`; if none is set, ask the user
   for the path and pass it. The scan takes a few minutes. Companies, title and location filters
   live in career-ops' `portals.yml`.
2. If it prints `no new postings`, say so and stop. If it exits non-zero, show its message
   (node missing, career-ops folder missing, scan failed) and stop.
3. Otherwise read the CSV it names and show the count and the first 15 rows
   (rank, company, title, location). Over 60 rows: say so, and suggest batching a slice
   (`--rows 1-40`) rather than the whole list, since every row costs a pre-screen and a score.
4. Suggest the next step: `/batch resume <csv>` or `/batch apply <csv>`; add `--exclude <this
   week's external list>` next time so the two don't overlap. Say that eligibility (config `targeting`
   `eligible_regions`) isn't checked yet (the `/batch` pre-screen does it) and that the score gate drops weak fits before
   resumes.
