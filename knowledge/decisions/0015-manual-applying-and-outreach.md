# ADR 0015: Manual applying and outreach: Claude prepares, the user submits and sends

- **Status:** accepted
- **Date:** 2026-11-21

## Context
`/apply` filled forms in the user's signed-in Chrome and submitted on an OK; one form was
submitted by a stray Enter before that rule existed (2026-10-04). `/outreach`, `/followup` and
`/batch` sent LinkedIn requests and messages to new people without approval (ADR 0005). Automated
LinkedIn activity risks the user's account, a send cannot be taken back, and an agent that reads
untrusted pages (postings, inbound messages) while it can click Send or Submit is exposed to
instructions planted in them. This user (a student looking for internships) wants no automated
submits or sends.

## Decision
- `/apply` and its Workday playbook are removed, with `/batch apply` mode and `/outreach --apply`.
  The user applies by hand with the tailored PDF (and `/cover-letter` when a form takes one).
- `/outreach`, `/followup` and `/batch`'s LinkedIn stage read LinkedIn and draft. Claude never
  clicks Connect, Message, Send, Follow or InMail and never types into a composer or a note: each
  posting gets a send sheet (`## To send` in `outreach.md`, or a batch `questions.txt`), the user
  sends by hand and says what was sent, and only that is logged under `## Sent` / `## Follow-up`.
- The user also checks each new person's route (a free Open Profile message or a connection
  request) when sending, so Claude no longer opens message composers.
- `applied` is recorded when the user says so: `/job-shortlist` "Record applied" now also updates
  `applications.md`, and `/batch` records `applied` from its `questions.txt`.
- The statuses and their legend are unchanged; `*-ready` now means drafts waiting for the user.

## Consequences
Supersedes ADR 0001 (Workday sign-in), ADR 0005 (approval only for existing connections), ADR 0006
(outreach separate from apply) and ADR 0008 (Claude reads the composer). The user does more clicks
per posting, and logs depend on the user saying what was sent; `/followup`'s reconcile step still
finds sends that were never logged. LinkedIn is still read by an agent, so the one-tab, low-volume
rules (ADR 0007) and the stop on any warning stay.
