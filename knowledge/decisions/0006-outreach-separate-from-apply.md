# ADR 0006: Outreach separate from apply

- **Status:** superseded by [0015](0015-manual-applying-and-outreach.md)
- **Date:** 2026-10-19

## Context

`/outreach` always ran `/apply` first, so messaging people at a company meant submitting an
application too, and `/batch outreach` skipped every posting already applied to. The user's LinkedIn
wording rules lived only in the `## LinkedIn outreach` section of `sources/profile.md`, not in the
skills: say "interested", never "applied"; attach nothing; never InMail; send a free message when
LinkedIn offers one.

## Decision

- `/outreach` and `/batch outreach` are LinkedIn-only by default. They apply first only with
  `--apply` or when the user asks in plain words; when unsure, they do not apply.
- The tailored resume is still built (`/resume`, no form), because the messages quote it.
- New statuses `outreach-only-ready` and `outreach-only-sent` mark postings messaged without an
  application. Reusing `outreach-*` was rejected: the in-place Status cell would lose whether the user
  applied, and `/batch apply` would skip the posting forever.
- `tools/read_postings.py --for outreach` uses an outreach skip set, so postings applied to but
  never messaged are picked; the default skip set still picks `outreach-only-*` postings for
  `/batch apply`.
- The profile wording and route rules are folded into the skills: messages say "interested", never
  "applied"; nothing is attached and no message says a resume is attached; never InMail; a free
  message when LinkedIn offers one (Open Profile), else a connection request; approved messages to
  existing connections are sent directly. ADR 0005's approval classes and all caps are unchanged.

## Consequences

A posting can be messaged without an application, and `applications.md` shows which ones were.
Once a row reaches `in-conversation`, `no-response` or `closed`, the status no longer records
whether the user applied; the never-reapply rule and `/apply`'s per-application submit OK still guard
against a duplicate application. Follow-ups carry no attachment, so they rely on the message text
and the user's LinkedIn profile.
