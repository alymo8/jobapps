# ADR 0006: Light LinkedIn runs: one tab, resume as a link

- **Status:** accepted
- **Date:** 2026-10-19

## Context

`/outreach` and `/followup` often crashed Aly's laptop (16 GB RAM). Chrome was the cause: a
LinkedIn tab takes several hundred MB and keeps growing as pages are opened in it. The skills
multiplied that: every message that carried the resume was typed and left unsent in its own tab
for Aly to attach the PDF (the composer's cross-origin iframe blocks `file_upload`); `/batch`
ran up to 2 outreach subagents, each with its own LinkedIn tab; and `/followup` opened Messaging and
a profile for each of up to 40 people in one tab that was never reloaded.

## Decision

- **Resume as a link.** Messages carry the tailored resume as a URL Aly makes (the posting's PDF
  uploaded, e.g. to Google Drive with "anyone with the link"), recorded as `Resume link: <url>` in
  the posting's `outreach.md`. Nothing is typed and left unsent in a tab any more; a message that
  needs the link waits for it.
- **One LinkedIn tab at a time.** `.claude/skills/linkedin-tab.md` is the shared procedure: one
  tab per run, pages by direct URL (never the feed), text reads over screenshots, closed at the end.
  `/batch` splits outreach prepare into the application part (2 at a time, no LinkedIn) and a
  LinkedIn stage 2b (1 at a time); outreach execute runs 1 at a time.
- **Recycle the tab every 8 page opens**: close it and open a fresh one, which frees what LinkedIn
  has piled up.

## Consequences

Peak Chrome memory during a run is bounded by one LinkedIn tab (plus at most 2 form tabs in
`/batch`). The resume becomes reachable by anyone with its link, and Aly uploads one PDF per
posting. Batch outreach runs take longer because LinkedIn work is serial. Older `outreach.md`
files may still log `typed, Aly to send`; `/followup` keeps reading it.
