---
name: scan-jobs
description: Search the web for open job postings that match the targets in the user's profile (target roles, locations, target and priority companies) and write them as a CSV that /batch reads, deduplicated against applications.md, dlq.md, postings/ and earlier lists. Use when the user runs /scan-jobs or asks to find or scan for new postings.
argument-hint: [--exclude <file.xlsx|file.csv|file.txt|dlq.md> ...]
---

# /scan-jobs — find new postings

All paths are relative to the repo root. `<S>` is this session's scratchpad. This supplements the
user's external target lists; it doesn't replace them. It never applies and never messages anyone.

1. **Read the setup.** If `config.local.json` does not exist, say
   `config.local.json is missing: this repo is not set up yet (run /onboard, or see README "Setup").`
   and stop. If `sources/profile.md` is missing, run `.claude/skills/pull-sources.md` first. Read
   `sources/profile.md`, `sources/mega-resume.tex` (ranking factor 2 is requirements overlap with
   the resume) and `config.local.json` `targeting` (`eligible_regions`, `home_city`; a missing key
   is simply absent).
2. **Fill the gaps before searching.** Never search with any of these missing.
   - `Target roles` or `Locations` under `## Targeting` missing or `ASK`: ask the user, then save
     each answer through `.claude/skills/write-source.md` (one run per change): an `ASK` line is
     replaced; a missing `Locations` line is added at the end of `## Targeting`.
   - No `## Job search` section: ask for target companies and priority companies (`none` is a
     valid answer for either), then add the section in one `write-source.md` run, a "new section"
     edit with the text
     `\n## Job search\n- Target companies: <answer> (<first name>, <today>)\n- Priority companies: <answer> (<first name>, <today>)\n`.
   - `## Job search` exists but a line is `ASK`: ask, then replace each `ASK` line in its own
     `write-source.md` run, in sequence.
3. **Search.** Read `templates/weekly-search-prompt.md` and follow these sections, found by
   heading, with its placeholders filled at run time: `## Target roles, in priority order` from
   `Target roles`; `## Target companies` and `## Priority companies` (with `### How priority status
   works` and `### Known board-access notes (from past runs)`) from `## Job search`;
   `## Location scope` from `Locations` plus config `targeting` (`eligible_regions`, `home_city`);
   `## Ranking`; `## Scale` (no padding, duplicates or reposts across boards; report the true
   smaller count; at most 100); and the last paragraph of `## Before you start` (ask only when
   something is genuinely ambiguous; otherwise make the call and say so). Skip `## Task`,
   `## Output`, `## Publish the results to the shortlist artifact`, `## Respect my decisions`,
   `## Week-over-week comparison`, `## What to flag explicitly in the summary` and the first
   paragraph of `## Before you start`: they read or write the Excel file or the shortlist artifact.
   A posting with no verifiable posting URL is left out (dedupe is by URL). Keep a list of priority
   companies whose boards you could not read: they are `unreadable`, not "nothing found".
4. **Dedupe and write the CSV.** Write the postings, best first, to `<S>/scan-jobs/rows.json` as a
   JSON list of `{"company", "title", "location", "url"}` objects, one per posting, each with its
   posting URL. Run `python tools/discover.py --input <S>/scan-jobs/rows.json $ARGUMENTS` with no
   `--location` (the search already applied the location scope). It dedupes against
   `applications.md`, `dlq.md`, `postings/*/posting.md`, earlier `discovered/*.csv` and any
   `--exclude` files, and writes `discovered/<date>.csv`. If it prints `no new postings`, say so
   (with the `unreadable` list, if any) and stop. If it exits non-zero, show its message and stop.
5. **Report.** Read the CSV it names and show the count, its `skipped N rows` line if it printed
   one, and the first 15 rows (rank, company, title, location). List the `unreadable` priority
   companies so the user can check them by hand. Over 60 rows: say so, and suggest batching a
   slice (`--rows 1-40`) rather than the whole list, since every row costs a pre-screen and a
   score. Suggest the next step: `/batch resume <csv>` or `/batch apply <csv>`; add `--exclude
   <this week's external list>` next time so the two don't overlap. Say that eligibility (config
   `targeting` `eligible_regions`) is re-checked by the `/batch` pre-screen and that the score gate
   drops weak fits before resumes.
