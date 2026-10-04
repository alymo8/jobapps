---
name: followup
description: Follow up with the LinkedIn contacts from earlier /outreach runs - send the prepared follow-up after a connection is accepted, nudge people who went silent, draft answers to replies, and replace stale invitations from the posting's shortlist; every message is approved by Aly before sending. Use when the user runs /followup or asks to follow up or re-message people from previous outreach batches.
argument-hint: "[<posting dir | company> ...] [--dry-run]"
---

# /followup — re-engage earlier outreach contacts, human-in-the-loop

All paths are relative to `jobapps/`. Runs inline in this session (no subagents) in **one Chrome
tab of its own**: load `claude-in-chrome` first, create a new tab, never touch other tabs. Aly is
logged in to LinkedIn on a free account (no InMail; about 3 personalized invitations a month;
invitation notes ≤200 characters). **Nothing is sent to anyone without an explicit `ok` or `edit:`
from Aly in this run's `questions.txt`.**

## Arguments

- No argument: every `postings/*/outreach.md`.
- `<posting dir>` (with or without `postings/`): that dir. A dir with no `outreach.md` resolves to the
  `*-combined` dir whose header names it or its req id.
- `<company>`: dirs whose name starts with it (case-insensitive), `*-combined` included; matching
  dirs without `outreach.md` are ignored. Nothing matches → report `no outreach for <arg>`.
- `--dry-run`: steps 1–4 only. Writes only `batches/<id>-followup/`; no `outreach.md`,
  `applications.md` or `profile.md` edits; nothing sent, nothing clicked that sends, connects or
  withdraws. Report the questions.txt path in chat; do not open it.

## Dates

Business days = Mon–Fri after the date the rule counts from, up to and including today. Each rule
counts from one date: `silent` / `waiting` after a message → the last outbound message; `done` by
nudge → the nudge; `stale-pending` / pending `waiting` → the invitation. Compute, never estimate:

```
python -c "import datetime as d,sys; a=d.date.fromisoformat(sys.argv[1]); b=d.date.fromisoformat(sys.argv[2]); print(sum(1 for i in range(1,(b-a).days+1) if (a+d.timedelta(i)).weekday()<5))" <from YYYY-MM-DD> <today YYYY-MM-DD>
```

Calendar days = `(today - from).days`. Use the logged date when there is one for a send Claude
confirmed (`## Sent`, `nudge sent`, `reply sent`, `invite sent`). For a `typed, Aly to send`
message, use the outbound date shown in the LinkedIn thread (Aly may send it days later). When only LinkedIn's
relative label exists ("1 week ago", "Tuesday"), convert it to an absolute date and mark it `~` in
the manifest (e.g. `~2026-09-27`).

## 1. Collect

For each posting in scope read `outreach.md`:

- **`## Sent`**: parse every variant: the pipe bullet
  `- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:` + `>` quote; the same bullet
  without `text sent:` + an indented `>` quote; and the pipe bullet whose fifth field is the sent text in double quotes, after a prose line naming the channel (Censys). A
  bullet that fits none is listed in the review as `unparsed` with its line; never guess.
- **`## Follow-up`**: two kinds of bullet. Action bullets
  `- <Name> | <YYYY-MM-DD> | <state> | <action> | text:` are the record: derive state only from
  them. Approval bullets `- APPROVED <YYYY-MM-DD> | <Name> | <kind> | text:` with no later action
  bullet of the same person and kind are shown in the review as `approved, not executed (<date>)`
  and need a fresh approval.
- **Drafts**: (a) = connection note, also "Connection note" / "Connection note (fallback)";
  (b) = follow-up after acceptance, also "Follow-up message" / InMail Body. A "Short notes (200-char
  limit)" entry replaces (a) when sending.
- **Shortlist** table (the section whose heading starts with `## Shortlist`; `*-combined` files add a Role(s) column), in order.

One record per contacted person: posting dir, name, profile URL, channel, first-send date, last
action and date, nudge sent (yes/no). **Dedupe by profile URL** across postings: one LinkedIn
check per person; one state per posting. "Nudge sent" is computed across **all** `outreach.md`
files: any `nudge sent` action bullet for that profile URL counts, so a person gets one nudge
ever, not one per posting. A person nudged via another posting is classified from that nudge's
date (`done (no-response)` after ≥3 business days with no reply, else `waiting`), note
`nudged via <dir>`. Within one run a due nudge goes on the posting contacted first.

## 2. LinkedIn sweep

If more than 40 people have records, ask Aly to confirm or narrow first. Wait 3–5 seconds
between page opens (browser wait action).

1. **Sent invitations** (My Network → Manage → Sent), one pass: who is pending and since when.
   Record the total count in the manifest header (`Sent invitations at start: N`).
2. **Messaging**, for each person with a record (search by name): connected or not, date of the
   last outbound and last inbound message, and the full text of inbound messages since the last
   outbound one.
3. **Profile**, for each person with a record: if the top Experience entry is no longer the
   posting's company → `done (left company)`.
4. **Reconcile** shortlisted people with no logged send, from the Sent-invitations page and the
   Messaging conversation list (no per-name search): a send found → a record marked
   `(reconciled <date>)` with the visible text. Step 7 writes it to `## Sent` (not in `--dry-run`).
5. Invitation neither pending nor accepted and no thread → `done (no-response)`, note
   `invite withdrawn/expired`.

A CAPTCHA, a rate limit or a "restricted activity" warning: stop, tell Aly, no retries. At the end
record `Sent invitations at end: N` in the manifest header.

## 3. Classify

Exactly one state per person, checked in this order:

| # | State | Rule | Drafted next action |
|---|-------|------|---------------------|
| 1 | `done` | Left the company; or the conversation was closed by either side (declined, "not hiring", told to apply elsewhere); or nudged and no reply ≥3 business days after the nudge; or a stale invitation whose `## Follow-up` shows `replacement sent` or `none left`, still not accepted and with no inbound message; or withdrawn/expired | None. State recorded as `done (no-response)`, `done (closed)` or `done (left company)` |
| 2 | `replied` | An inbound message newer than the last outbound one | One-line summary, their text verbatim, a drafted response |
| 3 | `accepted` | Connected, and no outbound message after acceptance other than the invitation note | The person's (b), re-checked against the resume; Aly attaches the resume. No (b) → a new follow-up from the posting's drafts and tailored resume, marked `new`. A previous `typed, Aly to send` → note `typed <date>, not sent` |
| 4 | `silent` | A (b), InMail or direct message sent, no reply, ≥3 business days since the last outbound message, no nudge yet | One nudge, ≤300 characters |
| 5 | `stale-pending` | Invitation pending ≥10 calendar days | Leave the invitation. Propose the next unused shortlisted person (below) |
| 6 | `waiting` | Anything else | None |

**Nudge:** the role title, a reminder that Aly applied and messaged earlier, and one question:
is the role still open, and would they be open to a short chat or to pointing Aly to the right
person. No new claims, no guilt-tripping.

**Reply:** answer only from the posting's tailored resume and `profile.md`,
in the language of the reply (English or French). Anything neither covers (salary with no `profile.md` rule, specific
availability, references) becomes a question in `questions.txt`, not a guess. A request to
schedule → ask Aly for times; never invent any.

**Replacement (stale-pending):** at most one per posting per run. The next person in Shortlist
order who has no `## Sent`, `## Follow-up` or reconciled send, is not marked skipped / may have
left / not at the company, and was not found `done (left company)`. The note: their "Short notes
(200-char limit)" entry, else a new note ≤200 characters condensed from their (a) (or their only
draft), length checked by piping the note on stdin into
`python -c "import sys; print(len(sys.stdin.read().rstrip(chr(10))))"` (heredoc in Bash), marked `new`. Nobody left →
`none left`.

**Invite budget:** count connection requests dated this calendar month across all `outreach.md`
(`## Sent` channel containing `connection request`, plus `## Follow-up` action `invite sent`).
Remaining = max(0, 3 − count). Proposals beyond it are still listed, flagged `over budget`.

## 4. Review sheet

Create `batches/<YYYY-MM-DD-HHMM>-followup/`:

- `manifest.md`: header lines (run date, args, dry run yes/no, invite budget, Sent invitations at
  start/end), then the table `# | Posting | Person | State | Days | Last out | Last in | Proposed action | Result`.
  Days: `N bd` (business days) for `silent`, `waiting` after a message and `done` by nudge; `N cd`
  (calendar days) for `stale-pending` and pending `waiting`; `-` otherwise.
- `review.md`: counts per state and the invite budget at the top; then every proposed message
  **in full, verbatim**, grouped replied → accepted → silent → stale-pending (for `replied`, their
  reply verbatim above the draft; flags `new`, `over budget`, `typed <date>, not sent`,
  `approved, not executed`); then `waiting` and `done` as short tables; `unparsed` lines; and a
  final `## No contacts` section for postings in scope with no contact found.
- `questions.txt`: plain text, numbered. One item per proposed message: who, which posting, the
  message verbatim, then `Answer:` (`ok` / `edit: <text>` / `skip`). Then reply questions from
  step 3. Header line: "Only `ok` or `edit:` approves; a blank `Answer:` counts as `skip`." No
  suggested answers. Open it with `Invoke-Item` (not in `--dry-run`).

Post a 5-line summary in chat (counts per state, budget, no-contact postings) and wait. Nothing is
approved by silence; an approval of one message does not cover another. `--dry-run` ends here.

## 5. Record approvals

When Aly says questions.txt is done, re-read it. For each `ok`/`edit:`, append an approval bullet
to that posting's `## Follow-up` (create the section at the end of `outreach.md` if missing):
`- APPROVED <date> | <Name> | <nudge / reply / follow-up (b) / replacement invite> | text:` + the
final text quoted. Save reusable answers to `profile.md` (as a rule when the answer carries
"always" or a condition). Anything unclear → ask before recording.

## 6. Execute

Approved items only, text verbatim, one at a time:

- **Nudge or reply** (no attachment): send in the thread; confirm it appears there.
- **Follow-up (b)**, or any approved text that says the resume is attached: type it in the thread
  and leave it **unsent** in its own tab; list those tabs for Aly, who attaches the PDF and sends.
- **Replacement invite**: re-check the note is ≤200 characters in code; send the connection
  request with it; confirm it shows as pending.
- After each confirmed send (or each message typed for Aly), write its action bullet immediately
  to that posting's `## Follow-up` (format in step 7), before the next item. A run that stops
  midway then never loses the record of a nudge already sent.
- A send that fails or hits a warning: stop and tell Aly. No retries.

## 7. Log

- **`outreach.md`**, `## Follow-up`, one action bullet per person handled (sends and typed
  messages were already logged in step 6; add the rest):
  `- <Name> | <date> | <state> | <action> | text:` + the quoted text if any. Actions:
  `nudge sent`, `reply sent`, `typed, Aly to send`, `invite sent` (the replacement person),
  `replacement sent` / `none left` (the stale person), `none`.
  - A replacement person also gets a standard `## Sent` bullet
    (`- <Name> | <profile URL> | connection request with note | <date> | text sent:` + quote).
  - A reconciled send gets a `## Sent` bullet in the same format, with `(reconciled <date>)`
    after the channel.
- **`applications.md`** (only writer this run). Rows: a plain dir → the row with that Posting dir;
  a `*-combined` dir → every row whose Posting dir, after `postings/`, starts with the same company
  prefix and whose dir name or req id is in the combined file's header.
  - Status changes only from `applied`, `outreach-ready`, `outreach-sent`, `in-conversation`,
    `no-response` or `closed`, checked in order: every contacted person `done` and at least one
    `done (closed)` → `closed`; every contacted person `done` with no reply → `no-response`; any
    person `replied`, or replied earlier in a conversation that is not closed → `in-conversation`;
    otherwise unchanged (a reconciled send or an acceptance only adds a Notes entry).
  - Unsubmitted rows (`resume`, `ready`, `blocked`, `held`, `skipped`) keep their status; the
    outcome goes in Notes only.
  - Every touched row gets a short note with the batch id.
  - Safety net: if the legend line lacks `in-conversation`, update it to
    ``Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`.``
- **Manifest** Result column filled. Chat report: sent, typed for Aly (with tab list), skipped,
  stopped-on-warning.

## Guardrails

- Never send anything not approved (`ok` / `edit:`) in this run.
- At most one nudge per person, ever; the `## Follow-up` action bullets are the record.
- No people beyond the posting's Shortlist table.
- Every factual claim from the posting's tailored resume or `profile.md`.
- Stop on CAPTCHA, rate-limit or restriction warnings, and on any failed send.
