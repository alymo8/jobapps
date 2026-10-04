# /followup skill: design

- **Date:** 2026-10-04
- **Status:** approved

## Purpose

After `/outreach` (or `/batch outreach`) has contacted people on LinkedIn, Aly needs to re-engage
them: send the prepared follow-up once a connection is accepted, nudge people who went quiet,
answer people who replied, and replace contacts whose invitations sit unanswered. `/followup` does
this across all earlier postings in one pass, with every outgoing message approved by Aly first.

## Background (current state)

- `/outreach` writes `postings/<dir>/outreach.md`: a shortlist table, per-person drafts — (a) a
  connection note and (b) a follow-up message to send after acceptance — and a `## Sent` log.
  Older files use other labels and have no short notes: HingeHealth has an unlabelled
  "Connection note" plus a "Follow-up message" per person; Spellbook has an InMail Subject/Body plus a
  "Connection note (fallback)". In this spec a "Connection note" / "Connection note (fallback)"
  counts as (a), and a "Follow-up message" or InMail Body counts as (b).
  The log formats vary today: most bullets are
  `- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:` followed by the quoted text,
  some (BanyanSoftware, Knak, Sardine) have no `text sent:` field, and Censys has a prose preamble
  with the text quoted inline. `outreach/SKILL.md` step 6 lists the fields but not a format.
- Premium has lapsed, so most contacts were made by connection request with a note. A free account
  gets about 3 personalized invitations per month.
- The LinkedIn message composer is a cross-origin iframe: Claude cannot attach the resume PDF.
  Messages that need the resume are typed and left unsent in their own tab for Aly to attach and send.
- Aly sent some messages by hand, so some contacts are not in any `## Sent` log
  (e.g. Baseten, Cresta: drafts in `outreach.md`, no `## Sent` section, status `applied`).
- Some `outreach.md` files cover several postings (`Scotiabank-combined`, `ThomsonReuters-combined`);
  their `applications.md` rows point to the individual posting dirs. Scotiabank-combined names those
  dirs in its header; ThomsonReuters-combined names only the req ids (JREQ202780, 9090356).
- `applications.md` statuses today: `resume` → `ready` → `applied` → `outreach-ready` → `outreach-sent`.

## Scope

**In:**
- `.claude/skills/followup/SKILL.md` (new).
- `.claude/skills/outreach/SKILL.md`: step 6 gains a pointer to `/followup` and makes the
  `- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:` bullet (quoted text below it)
  the required `## Sent` format. Existing logs are not migrated; `/followup` step 1 (Collect) parses all variants.
- `applications.md`: status legend line gains `in-conversation`, `no-response` and `closed`.

**Out:**
- New Python tools; subagents; a `/batch followup` mode.
- Scheduling or recurring runs.
- Searching LinkedIn for people not already on a posting's shortlist.
- Email follow-ups.
- Updating the stale "has Premium (InMail)" line in `outreach/SKILL.md`.

## Design

### Invocation

`/followup [<posting dir | company> ...] [--dry-run]`

- No argument: every `postings/*/outreach.md` (any posting with a shortlist), so postings where
  Aly sent by hand are swept too. Postings with no `## Sent` entries and nothing found on LinkedIn
  are listed once as `no contacts` and dropped.
- `<company>` matches posting dirs whose name starts with it (case-insensitive), including
  `*-combined` dirs.
- `--dry-run`: steps 1–4 only. Writes only the batch dir (`manifest.md`, `review.md`,
  `questions.txt`): no `outreach.md`, `applications.md` or `profile.md` edits, nothing sent.
  Reconciled entries appear only in the manifest and review. It reports the questions.txt path
  in chat and does not open it.

### Flow

Runs inline in the main session: no subagents, one Chrome tab of its own (load `claude-in-chrome`
first; never touch other tabs).

#### 1. Collect

For each posting in scope, read the `## Sent` log and any existing `## Follow-up` section. Parse
every `## Sent` variant listed in Background (pipe bullets with or without `text sent:`, and prose
with inline quotes); a bullet that can't be parsed is listed in the review as `unparsed` with its
line, not guessed. Build one record per contacted person: posting dir, name, profile URL, channel, first-send date, the latest
follow-up state and date, and whether a nudge has been sent.

#### 2. LinkedIn sweep

- **Sent invitations** (My Network → Manage → Sent): which people are still pending, and since when.
- **People in scope:** every person in the posting's Shortlist table, plus anyone in its `## Sent` or
  `## Follow-up`. Shortlisted people with no logged send are checked on the Sent-invitations page
  and in Messaging, and become records only if a send is found (see Reconcile).
- **Messaging:** for each person in scope, open the thread (search by name). Record whether you
  are connected, the date of the last outbound message, the date of the last inbound message, and
  the full text of any inbound messages since the last outbound one.
- **Reconcile:** if a thread or a pending invitation shows a send to a shortlisted person with no
  `## Sent` entry (sent by hand), record it in the manifest as `(reconciled <date>)` with the text
  visible on LinkedIn. In a normal run step 7 also writes it to `## Sent`; `--dry-run` does not.
- A profile that now shows a different current employer: state `done`, note `left company`.
- A CAPTCHA, a rate-limit or a "restricted activity" warning: stop the sweep and tell Aly. No retries.

#### 3. Classify

Business days (Mon–Fri) are counted from the last outbound message to today, not counting the send
day. Exactly one state per person, checked in this order:

| # | State | Rule | Drafted next action |
|---|-------|------|---------------------|
| 1 | `done` | Left the company, or the conversation was closed by either side (declined, "not hiring", told to apply elsewhere), or nudged already and still no reply after ≥3 business days since the nudge, or a stale invitation whose replacement was already handled (its `## Follow-up` shows `replacement sent` or `none left`) and that is still not accepted and has no inbound message | None. The log's state field records `done (no-response)`, `done (closed)` or `done (left company)`; its action is `none` |
| 2 | `replied` | An inbound message newer than the last outbound one | A one-line summary of their reply, their text verbatim, and a drafted response |
| 3 | `accepted` | Connected, and follow-up (b) (or an equivalent message) not yet sent | The posting's existing (b) draft, re-checked against the resume; the resume is attached by Aly. With no (b) (or equivalent, see Background) for that person, a new follow-up drafted from the posting's existing draft and tailored resume, marked new in questions.txt |
| 4 | `silent` | Outbound message (b), an InMail or a direct message was sent, no reply, ≥3 business days, no nudge yet | One nudge, ≤300 characters |
| 5 | `stale-pending` | Invitation still pending ≥10 calendar days after sending | Leave the invitation. Propose the next unused person from that posting's shortlist. The note is that person's entry in the posting's "Short notes (200-char limit)" section if there is one, else a new ≤200-character note condensed from their (a) note or its equivalent (see Background), or from their only draft when they have neither (length measured in code), shown in questions.txt as a new message needing approval |
| 6 | `waiting` | Anything else (under the thresholds) | None. Listed for information |

**Nudge content:** the role title, a reminder that Aly applied and messaged earlier, and one
question about whether the role is still open and whether they'd be open to a short chat or to
pointing Aly to the right person. No new claims, no guilt-tripping phrasing.

**Reply content:**
- Answer only from the posting's tailored resume and `profile.md`.
- If the reply asks for something neither covers (salary when `profile.md` has no rule, specific
  availability, references), that becomes a question in `questions.txt` instead of a guess.
- If the reply asks to schedule something, propose that Aly suggests times. Don't invent any.

**stale-pending replacements:** the free-account invite budget (about 3 a month) is shown in the
review. No more than one replacement per posting per run. Postings with no unused shortlisted
person get `none left` instead. Step 7 logs the stale person with action `replacement sent` (once
the replacement goes out) or `none left`, so no later run proposes another replacement for them;
from then on they are `done (no-response)` unless they accept (then `accepted`) or reply.

#### 4. Review sheet

Create `batches/<YYYY-MM-DD-HHMM>-followup/`:

- `manifest.md`: table `# | Posting | Person | State | Days | Last out | Last in | Proposed action | Result`, where
  Days is the count step 3 used for that state (e.g. `3 bd` business days, `10 cd` calendar days).
- `review.md`: every proposed message **in full, verbatim**, grouped by state in the order
  replied, accepted, silent, stale-pending. For `replied`, the person's reply text verbatim above
  the draft. Then `waiting` and `done` as short tables. At the top: counts per state and the
  invite budget.
- `questions.txt`: what Aly fills in, in the `/batch` convention. One numbered item per proposed
  message: the message verbatim, then an `Answer:` line (`ok` / `edit: <text>` / `skip`). Only an
  explicit `ok` or `edit:` approves; a blank `Answer:` counts as `skip`. Unlike `/batch`, there are no
  suggested answers and no "leave blank to accept" line. Next,
  any reply questions from step 3. Open it with `Invoke-Item` (not in `--dry-run`).

Post a 5-line summary in chat (counts per state) and wait. Nothing is approved by silence, and an
approval of one message does not cover another. `--dry-run` ends here.

#### 5. Record approvals

Read `questions.txt`. For each `ok`/`edit`, append the final text under the person's entry in the
posting's `## Follow-up` section, marked `APPROVED <date>`. Save reusable answers to `profile.md`, as
`/batch` does. Anything unclear → ask before recording.

#### 6. Execute (approved items only, verbatim)

- **Nudge or reply, no attachment needed:** send it in the thread, then confirm it appears there.
- **(b) message, or any message whose approved text says the resume is attached:** type it in the
  thread and leave it unsent in its own tab. List the tabs for Aly, who attaches the PDF and sends.
  Log it as `typed, Aly to send`.
- **stale-pending replacement:** send the connection request with the approved note (≤200
  characters, the free-account limit, measured in code), then confirm it appears as pending.
- Any send that fails or hits a warning: stop and tell Aly. No retries.

#### 7. Log

- In each posting's `outreach.md`, add or extend `## Follow-up`, one bullet per action:
  `- <Name> | <date> | <state> | <action: nudge sent / reply sent / typed, Aly to send / invite sent / replacement sent / none left / none> | text:`
  followed by the quoted text, if any.
- In `applications.md` (`/followup` is its only writer in this run), update the row(s) for each
  posting. A plain posting dir maps to the row whose Posting dir is that dir. A `*-combined` dir
  maps to every row whose Posting dir, after `postings/`, starts with the same company prefix (e.g. `ThomsonReuters-`)
  and whose dir name or req id appears in the combined file's header.
  - Status changes only when the current Status is `applied`, `outreach-ready`, `outreach-sent`,
    `in-conversation`, `no-response` or `closed` (the application is submitted), so a late reply
    still moves a row: checked in this order: to `closed` when every contacted person is `done` and at
    least one is `done (closed)`; to `no-response` when every contacted person is `done` with no
    reply; to `in-conversation` when any person at the posting is in `replied`, or has replied
    before in a conversation that is not closed; otherwise unchanged.
  - Rows with an unsubmitted Status (`resume`, `ready`, `blocked`, `held`, `skipped`) keep it, so an
    unsubmitted application stays visible. The follow-up outcome goes into Notes only.
  - Every touched row gets a short note with the run's batch id.
- If the legend line in `applications.md` lacks the new statuses (it is updated once at
  implementation, per Scope; this is only a safety net), update it to: `resume` → `ready` (form filled, awaiting OK) →
  `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`, keeping the
  existing parenthetical.
- Fill the manifest's Result column. Report in chat: sent, typed for Aly, skipped, and the tabs left open.

### Guardrails

- Never send anything not marked `APPROVED` in this run.
- At most one nudge per person, ever. The `## Follow-up` log is the record.
- No people beyond the posting's existing shortlist.
- Every factual claim comes from the posting's tailored resume (`.tex`/`.pdf` in the posting dir)
  or `profile.md`.
- Stop on CAPTCHA, rate-limit or restriction warnings.
- The first real send happens only in a later, non-dry run after Aly's approval, and is confirmed
  in the LinkedIn thread (a post-ship check, not part of done).

## Decisions

Confirmed by Aly on 2026-10-04:

1. Handles four situations: accepted → send (b); silent → nudge; replied → draft a response;
   invitation pending too long → act.
2. Timing: a nudge after 3 business days of silence, at most 1 nudge per person; a pending
   invitation is acted on after 10 days.
3. A stale pending invitation is left in place, and the next unused shortlisted person is proposed.
4. One inline pass with one review sheet, not a `/batch` mode with subagents.
5. Nudges, replies and replacement invitations are sent by Claude after approval. Messages that
   need the resume are typed and left unsent for Aly to attach the PDF.
6. New `applications.md` statuses: `in-conversation`, `no-response` and `closed` (everyone done,
   and at least one person declined or closed the conversation).
7. The 3-day threshold counts business days.
8. Reply questions that the resume or `profile.md` can't answer go to `questions.txt` and are never guessed.

## Success criteria

1. **Dry run on real data:** `/followup --dry-run` over the current postings (Artefact, 11x, GitLab,
   Guidepoint, Knak, Block, Baseten and any others with sends).
   - Every person in a `## Sent` log, plus any found by reconciliation, appears in `manifest.md`
     with exactly one state.
   - Each person gets the state the step 3 table gives for the run date, and the manifest shows
     the business-day or calendar-day count used.
   - Nothing is sent. SHA-256 hashes of `applications.md`, `profile.md` and every
     `postings/*/outreach.md`, taken before and after the run, are identical (several are
     already modified in the working tree, so `git status` can't show this). The only new files
     are under `batches/<id>-followup/`.
2. **Classifier table check:** the verifier works these synthetic cases out by hand against the step 3
   rules and records them in the verification notes; the skill does not produce them (logged sends
   are dated 2026-10-04; hand-sent contacts found by reconciliation, e.g. Baseten's Lou (September)
   and Crystal (pending before 2026-10-04), may reach other states in the criterion-1 run and are
   checked against the step 3 table with their LinkedIn dates): Thu (b) message sent → Tue check = 3
   business days → `silent`; Fri send → Mon check = 1 → `waiting`; invite pending 10 days →
   `stale-pending`; nudged + 3 business days → `done`; inbound newer than outbound → `replied`, even
   if a nudge was due.
3. **Consistency:** `followup/SKILL.md` follows the other skills' structure (frontmatter `name`,
   `description` triggering on `/followup`, `argument-hint`; numbered steps). The `outreach` and
   `applications.md` edits match this spec.
