# ADR 0007: Light LinkedIn runs: one tab at a time

- **Status:** accepted
- **Date:** 2026-10-19

## Context

`/outreach` and `/followup` often crashed Aly's laptop (16 GB RAM). Chrome was the cause: a
LinkedIn tab takes several hundred MB and keeps growing as pages are opened in it. `/batch` ran up
to 2 outreach subagents at once, each with its own LinkedIn tab next to the form tabs, and
`/followup` opened Messaging and a profile for each of up to 40 people in one tab that was never
reloaded. (Drafts left unsent in their own tabs for Aly to attach the resume were the third cause;
ADR 0006 already removed them: messages attach nothing.)

## Decision

- **One LinkedIn tab at a time.** `.claude/skills/linkedin-tab.md` is the shared procedure: one
  tab per run, pages by direct URL (never the feed), text reads over screenshots, closed at the end
  (left open only on a CAPTCHA or restriction warning, for Aly).
- **Recycle the tab every 8 page opens**: close it and open a fresh one, which frees what LinkedIn
  has piled up.
- **`/batch` does LinkedIn work serially.** Stage 2 fills forms only (2 at a time, `Application
  only`); a new stage 2b does the LinkedIn search and drafts one posting at a time; outreach-mode
  execute runs one subagent at a time.

## Consequences

Peak Chrome memory during a run is bounded by one LinkedIn tab (plus at most 2 form tabs in
`/batch`). Batch outreach runs take longer because LinkedIn work is serial, and recycling costs a
page load every 8 opens. 8 is a starting value for 16 GB; change it in `linkedin-tab.md` if runs
still feel heavy.
