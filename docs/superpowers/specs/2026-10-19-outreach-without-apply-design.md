# Outreach without apply: design

- **Date:** 2026-10-19
- **Status:** draft

## Purpose

`/outreach` today always runs `/apply` first (form fill, approval, submit) and only then messages
people on LinkedIn; `/batch outreach` does the same over many postings. Aly wants the two separate:
`/outreach` messages people on LinkedIn only, and applies to the posting only when Aly asks for it
explicitly. Applying stays `/apply`'s job.

The same change brings the outreach wording in line with Aly's standing rules in
`sources/profile.md` (`## LinkedIn outreach`, 2026-10-16), which the skill text still contradicts:
never InMail, say Aly is *interested* (never that he applied), never say a resume is attached.

## Background (current state)

Verified 2026-10-19 on `main` at `ab9c676` (#17):

- `.claude/skills/outreach/SKILL.md` step 1 runs the full `/apply` skill; "Running as a batch
  subagent" runs `/apply` Phase 1; "Batch execute mode" submits the application first. Messages say
  "that Aly applied"; existing-connection messages are typed with the resume attached and left for
  Aly to send; InMail is offered "with Premium".
- `.claude/skills/followup/SKILL.md`: the nudge reminds the reader "that Aly applied"; an accepted
  connection's follow-up (b) is typed for Aly to attach the resume; status changes start only from
  `applied`, `outreach-ready`, `outreach-sent`, `in-conversation`, `no-response`, `closed`.
- `.claude/skills/batch/SKILL.md`: mode `outreach` builds resumes, scores, then runs the outreach
  batch subagent (form fill + drafts), one review sheet, then execute (submit + sends).
- `tools/read_postings.py:28`: `DONE = {"applied", "outreach-ready", "outreach-sent"}`; rows with a
  `DONE` status are skipped unless `--all`, whatever the batch mode.
- `applications.md` keeps one row per posting with a single Status cell, updated in place; legend:
  `resume` → `ready` → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` |
  `no-response` | `closed`. Today `outreach-*` implies applied.
- `sources/profile.md` `## LinkedIn outreach`: free message when LinkedIn allows one (1st degree, or
  Open Profile "Free message"), otherwise a connection request with the note; never InMail;
  "interested", never "applied"; no "resume attached"; send approved messages directly, don't leave
  drafts open.

## Scope

**In:**

- `.claude/skills/outreach/SKILL.md`: LinkedIn-only by default, `--apply` opt-in; profile rules
  folded in; batch subagent and batch execute modes follow the flag.
- `.claude/skills/batch/SKILL.md`: `/batch outreach` is LinkedIn-only; `/batch outreach --apply`
  is today's combined flow; statuses and `read_postings.py --for outreach` as below.
- `.claude/skills/followup/SKILL.md`: nudge wording, follow-up (b) sent directly with no
  attachment, status transitions accept the new statuses, legend safety-net line updated.
- `.claude/skills/apply/SKILL.md`: description no longer says "/outreach runs this first" (it does
  only with `--apply`); after a submit, a row that was `outreach-only-ready`/`outreach-only-sent`
  becomes `outreach-ready`/`outreach-sent` instead of `applied` (keeps the outreach state).
- `tools/read_postings.py`: `--for outreach` option; `tests/test_read_postings.py`: tests for it.
- `applications.md` legend line: written by the skills' safety net (it is gitignored, not edited
  in the repo).
- `CLAUDE.md`: architecture line and the `read_postings.py` command line.
- `knowledge/decisions/0006-outreach-separate-from-apply.md` (new) and its row in
  `knowledge/decisions/README.md`.

**Out:**

- The approval classes from ADR 0005 (existing connection vs new) are unchanged.
- The 3-per-posting cap, the invitation budget and the 10-requests-per-run cap are unchanged.
- `/apply`'s form-filling and submit flow, `/resume`, `/cover-letter`, `/discover`,
  `/job-shortlist`.
- Editing `sources/profile.md` or any Claude Doc (the rules are already there).
- Recovering the applied/not-applied fact once a row has moved to `in-conversation`,
  `no-response` or `closed` (see Decisions).
- Any real LinkedIn send or application submit during implementation or testing.

## Design

### `/outreach` arguments

`argument-hint: <posting URL> | <posting dir> [--apply]`. Without `--apply`, the run never opens the
application form, never calls `/apply` and never submits anything. With `--apply` (or when Aly's
message in plain words asks to apply as well, e.g. "outreach and apply"), step 1 runs today's
"Apply first" step unchanged. When unsure whether Aly asked to apply, don't apply, and mention in
the final report that `/apply <posting>` is available.

The description becomes: "Message people at a job posting's company on LinkedIn: Aly's own
1st-degree connections there first, then recruiters / hiring managers near the posting location.
Does not apply unless Aly asks (`--apply`, which runs /apply first). Messages to Aly's existing
connections are approved by Aly (names shown first); requests and messages to new people go out
without approval. Use when the user runs /outreach."

### `/outreach` steps (without `--apply`)

0. Pull the sources (unchanged).
1. **Posting and resume.** Resolve the posting dir (`postings/<Company>-<id>/`, created with
   `posting.md` if new, as `/resume` does). If there is no compiled tailored resume in it, run
   `/resume` (build only; no form). The resume is the fact source for the messages and later
   follow-ups. If `applications.md` shows the posting as `outreach-sent`, `outreach-only-sent`,
   `in-conversation`, `no-response` or `closed`, say so and stop unless Aly says to continue
   (people were already messaged; `/followup` handles them).
2. Find people (unchanged from #17).
3. Draft (wording rules below).
4. Approval gate, existing connections only (unchanged from #17).
5. Send (route rules below).
6. Log (unchanged `## Sent` format). Status in `applications.md`, per "Statuses" below.

With `--apply`, step 1 is today's "Apply first" (run full `/apply`; if already `applied` skip it;
if Aly decides not to submit, stop); steps 2–6 are the same.

### Wording rules (all messages, both modes, and `/followup`)

- Say Aly is **interested** in the role. Never say he applied, even when he has.
- Never say a resume is attached, and attach nothing.
- 1–2 concrete facts from the posting's tailored resume (from `sources/mega-resume.tex` only), no
  flattery filler, no claims beyond the resume (unchanged).
- Drop the InMail subject line and the "With Premium InMail credits…" sentence.

### Route rules (step 5)

- **Existing connection** (after Aly's OK): a regular message with the approved text verbatim, sent
  directly. No attachment, so the "typed, leave unsent for Aly to attach" path is removed.
- **New person**: if the profile's Message button offers a free message (Open Profile "Free
  message"), send the follow-up (b) as that message; otherwise send the connection request with
  note (a), as today. Never InMail: if LinkedIn would only offer InMail, send the connection
  request instead.
- The `## Sent` channel list becomes `message (existing connection)`, `free message (open profile)`,
  `connection request with note`, `connection request (no note)`. Existing logs with `InMail` or
  `typed, Aly to send` stay valid for `/followup` to parse.
- The "Invitation and InMail budget" section becomes "Invitation budget"; the InMail-credit
  sentence goes.

### Statuses

Two new values in `applications.md`:

| Status | Meaning |
|--------|---------|
| `outreach-only-ready` | Not applied; an existing-connection message waits on Aly's OK |
| `outreach-only-sent` | Not applied; outreach sent |

- `/outreach` without `--apply` sets `outreach-only-ready` / `outreach-only-sent` when the row is
  absent or in `resume`, `ready`, `blocked`, `held`, `skipped` or `outreach-only-*`; when the row is
  already `applied` (or `outreach-ready`), it sets `outreach-ready` / `outreach-sent` (applied +
  messaged, today's meaning).
- `/apply` after a confirmed submit: `outreach-only-ready` → `outreach-ready`,
  `outreach-only-sent` → `outreach-sent`; anything else → `applied` (today).
- `/followup` status transitions start from the current list plus `outreach-only-ready` and
  `outreach-only-sent`. Moving to `in-conversation` / `no-response` / `closed` drops the
  applied/not-applied distinction (accepted, see Decisions).
- Legend line (all three skills' safety net, replacing the current one):
  ``Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`; not applied: `outreach-only-ready` → `outreach-only-sent`.``
  `/outreach` and `/apply` update the legend when they write a new-status row and the legend lacks
  `outreach-only`.

### `tools/read_postings.py --for outreach`

- New option `--for outreach` (any other value, or none, keeps today's behaviour).
- Default skip set stays `DONE = {"applied", "outreach-ready", "outreach-sent"}`, so
  `outreach-only-*` rows are **not** skipped by `/batch apply` / `/batch resume`.
- With `--for outreach`, the skip set is `{"outreach-ready", "outreach-sent", "outreach-only-ready",
  "outreach-only-sent", "in-conversation", "no-response", "closed"}`: postings already applied but
  never messaged are picked; postings already messaged are not. `--all` still keeps everything.
- Docstring and usage text mention the option.

### `/batch outreach`

- `argument-hint` gains `[--apply]` (meaningful only in `outreach` mode; ignored with a one-line
  note in other modes).
- Step 0.2 calls `read_postings.py ... --for outreach` in `outreach` mode without `--apply`;
  with `--apply`, today's call (no `--for`).
- Without `--apply`: the Workday-history check in 0.5 is skipped; resume (stage 1) and scoring
  (1a.5) run as today; stage 2's subagent prompt says `Mode: outreach only (no application)`; the
  review sheet and `questions.txt` have no application, form-question or submit parts for these
  postings (only LinkedIn, part 5, plus any decisions); stage 5 sends only; the orchestrator sets
  rows to `outreach-only-*` (or `outreach-*` when the row was `applied`), per "Statuses". The
  "Mark these <n> as applied?" shortlist prompt is not asked (nothing was submitted).
- With `--apply`: exactly today's flow, with the prompt saying `Mode: outreach + apply`.
- The confirm message (0.5) states which mode runs.

### `/outreach` batch sections

- "Running as a batch subagent": the prompt's mode line decides. `outreach only` → skip `/apply`
  entirely and run steps 2–3 (send nothing, as today); `outreach + apply` → today's text.
- "Batch execute mode": the application part runs only in `outreach + apply` mode; the send rules
  follow "Route rules".

### `/followup`

- Nudge: "the role title, a reminder that Aly is interested in it and messaged earlier, and one
  question" (replaces "Aly applied").
- `accepted` row: (b) is sent directly (no attachment), re-checked against the resume; the
  `typed <date>, not sent` note for older logs stays.
- Send rules: the "type it, Aly attaches the resume" bullet goes; every approved or no-approval
  text is sent directly. Never InMail.
- Status rules per "Statuses".

### ADR 0006

`knowledge/decisions/0006-outreach-separate-from-apply.md`, status accepted, date 2026-10-19:
context (outreach was tied to apply; profile wording rules not in the skills); decision (outreach
LinkedIn-only unless `--apply` or a plain request; tailored resume still built; `outreach-only-*`
statuses; `read_postings.py --for outreach`; wording and route rules); consequences (a posting can
be messaged without an application; the applied fact is lost once a row reaches
`in-conversation`/`no-response`/`closed`; follow-ups carry no attachment). Row added to
`knowledge/decisions/README.md` in the existing format.

### `CLAUDE.md`

- Architecture: `/discover` → `/resume` → `/apply`; `/outreach` (LinkedIn only; `--apply` to apply
  first) → `/followup`.
- Build, run, check: the `read_postings.py` line gains `[--for outreach]`.

## Decisions

- **LinkedIn-only by default; apply only on `--apply` or a plain request** (Aly, 2026-10-19).
  When unsure, don't apply.
- **Still build the tailored resume** without applying (Aly, 2026-10-19): drafts and follow-ups
  quote it. Rejected: drafting from the mega resume only.
- **New `outreach-only-ready` / `outreach-only-sent` statuses** (Aly, 2026-10-19). Rejected: reusing
  `outreach-*` (in-place status would lose whether Aly applied, and `/batch apply` would skip the
  posting forever).
- **Fold the profile.md LinkedIn rules into the skills** (Aly, 2026-10-19): interested-not-applied,
  no attachment, never InMail, free message when offered.
- **`/batch outreach` picks applied-but-not-messaged postings** (`--for outreach`): my call; outreach
  for a posting applied to earlier is the main reason to run outreach alone.
- **Applied fact lost after `in-conversation`/`no-response`/`closed`**: my call; a conversation
  means Aly is dealing with the posting by hand, and `/apply`'s never-reapply check by company +
  title (auto-memory) still applies. Rejected: an extra column (breaks every parser of the table).
- **Existing-connection messages sent directly after approval** (no typed-for-Aly tab): follows the
  profile rule "send approved messages directly", now possible because nothing is attached.

## Success criteria

1. `python -m unittest discover -s tests -v` passes, with new tests in `tests/test_read_postings.py`:
   with an `applications.md` fixture holding one row per status (`applied`, `outreach-ready`,
   `outreach-sent`, `outreach-only-ready`, `outreach-only-sent`, `in-conversation`, `ready`), default
   mode picks exactly `outreach-only-ready`, `outreach-only-sent`, `in-conversation`, `ready`;
   `--for outreach` picks exactly `applied`, `ready`; `--for outreach --all` picks all seven.
2. `python -m py_compile tools/*.py` succeeds; CI is green on the PR.
3. `rg -n -i "applied|InMail|attach" .claude/skills/outreach .claude/skills/followup` shows no
   instruction to say Aly applied, to use InMail or to attach a resume in a message; the only hits
   are the status names, `--apply`, the "never say he applied / never InMail / attach nothing"
   rules, and parsing of old log channels.
4. Read-through of `.claude/skills/outreach/SKILL.md` for both paths: without `--apply` no step
   reaches `/apply`, the form or a submit; with `--apply` the steps equal today's apply-then-message
   order. Same check for `/batch outreach` with and without `--apply` (prepare prompt mode line,
   review-sheet parts, execute stage, status written).
5. `rg -n "outreach-only" .claude/skills tools CLAUDE.md` shows the statuses in `outreach`, `apply`,
   `batch`, `followup` and `read_postings.py`, and the legend line is identical in every skill that
   writes it.
6. `rg -n "/outreach runs this first" .claude/skills` returns nothing; `knowledge/decisions/0006-*`
   exists and is listed in the decisions README.
