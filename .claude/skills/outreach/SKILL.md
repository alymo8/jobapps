---
name: outreach
description: "Message people at a job posting's company on LinkedIn: the user's own 1st-degree connections there first, then recruiters / hiring managers near the posting location. Does not apply unless the user asks (`--apply`, which runs /apply first). Messages to the user's existing connections are approved by the user (names shown first); requests and messages to new people go out without approval. Use when the user runs /outreach."
argument-hint: <posting URL> | <posting dir> [--apply]
---

# /outreach — LinkedIn messages (apply only with --apply)

All paths are relative to `jobapps/`. Uses Chrome (load `claude-in-chrome` first); the user is logged in
to LinkedIn. Keep volume low (at most 3 people per posting): LinkedIn flags automated-looking
activity, and the account is the user's. All LinkedIn work happens in one tab, per
`.claude/skills/linkedin-tab.md` (direct URLs, recycled every 8 page opens, closed at the end).

## Apply or not

By default this skill only messages people on LinkedIn: it never opens the application form, never
calls `/apply` and never submits anything. It applies first only with `--apply`, or when the user's
message asks in plain words to apply as well (e.g. "outreach and apply"). When unsure whether the user
asked to apply, don't apply. When the run did not apply, the final report mentions that
`/apply <posting>` is available.

## Approval rule

| Person | Approval |
|--------|----------|
| **Existing connection**: 1st-degree when this run finds them (before any request from us) | **Required.** Show the user their **names** (plus title and why) and the exact message; send only after an explicit OK for that person and that text |
| **Everyone else**: 2nd/3rd-degree, out of network, people the user does not follow | **Not required.** Send the connection request / message, then report it |

A person stays in the class they had when first found: someone who accepts our request later is a
*new* connection, not an existing one (see `/followup`). Silence or an ambiguous reply never
approves an existing-connection message; an approval of one message does not cover another.

## Steps

0. **Pull the sources.** Follow `.claude/skills/pull-sources.md`, unless the skill that ran this one
   already pulled them in this run.
1. **Posting and resume.**
   - **Without `--apply`:** resolve the posting dir (`postings/<Company>-<id>/`, created with
     `posting.md` if new, as `/resume` does). If there is no compiled tailored resume in it, run
     `/resume` (build only; no form). The resume is the fact source for the messages and later
     follow-ups. Then check the posting's `applications.md` row:
     - A Notes cell with `approval pending` is checked first and handled like an `*-ready` row
       (next bullet), whatever the status.
     - `outreach-sent`, `outreach-only-sent`, `in-conversation`, `no-response` or `closed`: say so
       and stop unless the user says to continue (people were already messaged; `/followup` handles
       them). On a continued run, never message anyone already under `## Sent` in `outreach.md`.
     - `outreach-ready` or `outreach-only-ready` (an existing-connection message waiting on the user), or
       a Notes cell with `approval pending`: skip steps 2–3, reuse the shortlist and drafts in
       `outreach.md`, re-show the pending approval (step 4), and in step 5 send nothing to anyone
       already under `## Sent`.
   - **With `--apply`:** run the full `/apply` skill (both phases). If `applications.md` already
     shows this posting as `applied`, skip `/apply` and go to step 2. If the user decides not to submit,
     stop here. Exceptions, by the row's status before the run:
     - `outreach-only-ready`, `outreach-only-sent`, `in-conversation`, `no-response` or `closed`:
       run `/apply` only and skip steps 2–6 (people were already messaged; nobody is messaged
       twice; `/followup` handles them). Say so in the report.
     - `outreach-ready` or `outreach-sent` (applied and messaged): skip `/apply` (no reapply) and
       follow the no-`--apply` rules above: stop on `outreach-sent`, resume the pending approval on
       `outreach-ready`.
2. **Find people** (LinkedIn people search in the run's LinkedIn tab, filtered to the company's
   current employees). Check each one still works there (current position).
   1. **the user's connections first**: the same search with the Connections filter set to `1st`. Every
      1st-degree connection at the company is a candidate, whatever their role (anyone inside can
      refer or forward); rank engineers / managers on the posting's team, then recruiters, then
      the rest.
   2. **Then new people**: recruiter / talent acquisition / technical recruiter at the company,
      preferring ones covering the posting's location or Canada/North America; and the likely
      hiring manager (the eng/AI manager or lead for the team the posting describes, in the
      posting's location, or the user's (Montreal) if the posting names several).
   - Write the shortlist (`## Shortlist` table in `postings/<dir>/outreach.md`): name, title,
     location, connection degree, **class** (`existing connection` / `new`), profile URL, and one
     line on why they fit. Up to 5 candidates, existing connections at the top.
   - Pick up to 3 to contact: existing connections first (up to 3), then fill the remaining slots
     with new people.
3. **Draft one message per picked person** (save all in `outreach.md`):
   - **Existing connection** → a direct message, 400–800 characters: friendly and personal (they
     know the user), role title and that the user is interested in the role, 1–2 concrete facts from the
     tailored resume that match the posting (from `sources/mega-resume.tex` only), and the ask: a
     referral, forwarding to the hiring team, or a short chat.
   - **New person** → (a) a connection note ≤ 200 characters (role, that the user is interested in the
     role, one fact), length checked in code by piping it on stdin into
     `python -c "import sys; print(len(sys.stdin.read().rstrip(chr(10))))"`; and (b) the follow-up
     message for after acceptance (or for a free message, step 5), 500–800 characters, same content
     rules as above, tailored to the reader: recruiter → fit + availability; hiring manager → the
     most relevant work.
   - Wording rules, every message:
     - Say the user is **interested** in the role. Never say he applied, even when he has.
     - Never say a resume is attached, and attach nothing.
     - No flattery filler, no claims beyond the resume.
4. **Approval gate, existing connections only.** Before anything is sent, show the user in chat:
   - A line naming them: `Your connections at <company> I'd message: <Name>, <Name>.`
   - For each: title, why, and the exact message text.
   - Then the new people (name, title, channel, the note), for information only: they are sent in
     step 5 without waiting for an answer.

   Wait for the user on the existing connections only: the user picks who and OKs or edits each text. If there
   are no existing connections at the company, say so in one line and go on.
5. **Send**, one person at a time, waiting 3–5 seconds between page opens (in the one tab, per
   `.claude/skills/linkedin-tab.md`). Never send to anyone
   already under `## Sent` in `outreach.md`.
   - Before the first send, check the user's plan (Premium or free), and for each new person read their
     message composer, both per "the user's plan and each person's message route" in
     `.claude/skills/linkedin-tab.md`.
   - **New person**, no approval needed: if their composer says "Free message" (Open Profile),
     send the follow-up (b) as that message. Otherwise send the
     connection request with note (a) right away and confirm it shows as pending. Notes are
     budgeted (below); past the budget send the request **without a note**, and (b) goes later
     through `/followup` once they accept. No InMail unless the user OKs that person and text in chat:
     if the composer shows InMail credits, send the connection request instead.
   - **Existing connection**: only after the OK, the approved text verbatim as a regular message,
     sent directly. No attachment.
   - A CAPTCHA, rate limit, "restricted activity" warning or failed send: stop and tell the user. No
     retries.
6. **Log** each send in `postings/<dir>/outreach.md` under `## Sent`, one bullet per send in exactly
   this format (the `/followup` skill parses it):
   `- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:` followed by the text sent as a
   `>` quote on the next line(s). Channel is one of `message (existing connection)`,
   `free message (open profile)`, `connection request with note`, `connection request (no note)`.
   (Older logs may carry `InMail` or `typed, the user to send`; `/followup` still parses them, but new
   logs never use them.)

   **Status** in `applications.md`, using the row's status before the run:
   - Row absent or `resume`, `ready`, `blocked`, `held`, `skipped`, `outreach-only-ready` or
     `outreach-only-sent`: set `outreach-only-sent` (or `outreach-only-ready` if an
     existing-connection message is waiting on the user). When the row was `ready` (a form filled,
     awaiting OK), add `form filled <date>, not submitted` to the Notes cell.
   - Row `applied` or `outreach-ready` (or applied by this run's `--apply`): set `outreach-sent`
     (or `outreach-ready` if an existing-connection message is waiting on the user).
   - Continued run on an already-messaged row (the user said to continue on `outreach-sent`,
     `outreach-only-sent`, `in-conversation`, `no-response` or `closed`): this overrides the two
     rules above. Keep the status and add `outreach again <date>` to the Notes cell, or
     `outreach again <date>, approval pending` while an existing-connection message waits on the user;
     drop the `, approval pending` part once it is resolved.
   - When writing the row, if the legend line in `applications.md` lacks `outreach-only`, rewrite
     the legend line to:
     ``Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`; not applied: `outreach-only-ready` → `outreach-only-sent`.``

   Close the LinkedIn tab. End with a chat report: who was messaged (by name, existing connections marked), requests and
   free messages sent, and, if the run did not apply, that `/apply <posting>` is available. Later
   follow-ups are handled by `/followup`.

## Invitation budget

With Premium (checked per `.claude/skills/linkedin-tab.md`) notes are unlimited: every request
carries its note. A free account gets about 3 personalized invitations (with a note) per month
(seen 2026-10-04); the rest of this section applies to a free account only. Requests without a
note are not capped that way, but LinkedIn limits them weekly, so on either plan send at most
10 connection requests per run across all postings. Count notes already sent this calendar month
across all `outreach.md` (`## Sent` channel `connection request with note`, plus `## Follow-up`
action `invite sent` with a note). Give the notes left to the most relevant new people (hiring
manager before recruiter); the rest go without a note.

## Running as a batch subagent

When the prompt says you are a batch subagent (orchestrated by the `batch` skill): skip step 0 (the
orchestrator has already pulled the sources). The prompt's mode line decides the rest:

- `Mode: outreach only (no application)`: skip `/apply` entirely (never open the form) and run
  steps 2–3 in your own tab.
- `Mode: outreach + apply`: run `/apply` Phase 1 under its batch rules, then steps 2–3 in your own
  tab. When the prompt also carries the line `Application only`, run `/apply` Phase 1 only and skip
  steps 2–3; with the line `LinkedIn only`, skip `/apply` and run steps 2–3 only.

Steps 2–3 use one LinkedIn tab of your own per `.claude/skills/linkedin-tab.md`, closed at the end;
`Application only` never opens LinkedIn.

In both modes **send nothing, submit nothing, connect with no one** (parallel subagents must not act
on the user's account at once). End with: posting dir, `ASK` count, blockers, the `outreach.md` path, and
the names of any existing connections found.

## Batch execute mode

Run on `postings/<dir>/`:

- **Application:** only with `Mode: outreach + apply` and `APPROVED <date>: submit` in
  `application.md`, and the posting not yet `applied`: the submit (`/apply` batch execute mode).
  When the execute prompt carries the line `Application only`, run the submit only and skip step 5
  entirely.
- **Messages** (both modes, unless `Application only`): step 5 for each **new** person in the shortlist's picks not marked skipped
  (no approval mark needed) and for each **existing connection** marked `APPROVED <date>`, with the
  text **verbatim**, in one LinkedIn tab per `.claude/skills/linkedin-tab.md`, closed at the end.
  Never send to anyone already listed under `## Sent` in `outreach.md`.

Then log to `outreach.md` only (the orchestrator owns `applications.md`; never write it in batch).
Never message an existing connection without an approval mark. Anything needing the user (budget
exhausted, CAPTCHA) → stop and reply `NEEDS USER: ...`.
