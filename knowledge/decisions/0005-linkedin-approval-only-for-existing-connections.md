# ADR 0005: LinkedIn approval only for existing connections

- **Status:** accepted
- **Date:** 2026-10-19

## Context

`/outreach` and `/followup` waited for the user's OK on every person and every message. Most outreach
goes to strangers (recruiters, hiring managers) as connection requests, where the approval step
slowed runs without protecting much. The user's own 1st-degree connections at a company are the easiest
people to reach, but they are personal relationships: the user wants to know who is being messaged and
approve it first.

## Decision

- `/outreach` searches the user's 1st-degree connections at the company first and picks them before new
  people (still at most 3 per posting).
- Each contact has a class, fixed when first found: `existing connection` (1st-degree before any
  request from us) or `new` (everyone else, including people who later accept our request).
- Messages to existing connections need the user's explicit OK, with their names shown first. Connection
  requests, follow-ups after acceptance and nudges to `new` people go out without approval and are
  reported after.
- Replies to inbound messages still need approval, whatever the class: they answer real questions
  in the user's name.
- `/followup` re-messages people who accepted, and adds up to 2 new people per posting per run
  (Shortlist first, then a fresh LinkedIn search), at most 10 connection requests per run.
  Requests carry a note while the ~3/month note budget lasts, and go without one after.
- `/batch` subagents still send nothing; execute mode sends to `new` people without an approval mark.

## Consequences

Runs need the user only for existing connections and replies. Messages to strangers go out under the user's
name without review, so the drafting rules (resume-only facts, no filler) and the per-run caps carry
more weight. A CAPTCHA or restriction warning still stops the run.
