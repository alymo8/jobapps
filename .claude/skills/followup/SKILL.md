---
name: followup
description: Follow up with the LinkedIn contacts from earlier /outreach runs - re-message people who accepted the connection request, nudge people who went silent, draft answers to replies, and find, add and message new people at the company. Messages to the user's existing connections and replies are approved by the user (names shown first); requests and messages to new connections go out without approval. Use when the user runs /followup or asks to follow up or re-message people from previous outreach batches.
argument-hint: "[<posting dir | company> ...] [--dry-run]"
---

# /followup — re-engage earlier outreach contacts and add new ones

All paths are relative to `jobapps/`. Runs inline in this session (no subagents) in **one LinkedIn
tab of its own**, per `.claude/skills/linkedin-tab.md`: load `claude-in-chrome` first, open pages
by direct URL, recycle the tab every 8 page opens, never touch other tabs, close it at the end. The user is
logged in to LinkedIn; check whether the user's plan is Premium or free before the first send, per
"The user's plan and each person's message route" in `.claude/skills/linkedin-tab.md` (free: about 3
personalized invitations a month; Premium: unlimited notes). Invitation notes stay ≤200 characters.

## Approval rule

Each person has a **class**, fixed when they were first found (step 1):

- **Existing connection**: the user's 1st-degree connection before any request from us. Every message
  to them needs an explicit `ok` or `edit:` from the user in this run's `questions.txt`, and the chat
  summary names them.
- **New**: everyone else, including people who have since accepted our request. Connection
  requests, the follow-up (b) after acceptance, and nudges go out **without approval** and are
  reported after.
- **Replies** to an inbound message always need approval, whatever the class: they answer real
  questions (availability, salary, scheduling) in the user's name.

## Arguments

- No argument: every `postings/*/outreach.md`.
- `<posting dir>` (with or without `postings/`): that dir. A dir with no `outreach.md` resolves to the
  `*-combined` dir whose header names it or its req id.
- `<company>`: dirs whose name starts with it (case-insensitive), `*-combined` included; matching
  dirs without `outreach.md` are ignored. Nothing matches → report `no outreach for <arg>`.
- `--dry-run`: steps 0–4 only (step 3b searches but sends nothing). Writes only `sources/` (the pull) and `batches/<id>-followup/`; no
  `outreach.md` or `applications.md` edits and no Profile doc writes; nothing sent, nothing clicked that sends, connects or
  withdraws. Report the questions.txt path in chat; do not open it.

## Dates

Business days = Mon–Fri after the date the rule counts from, up to and including today. Each rule
counts from one date: `silent` / `waiting` after a message → the last outbound message; `done` by
nudge → the nudge; `stale-pending` / pending `waiting` → the invitation. Compute, never estimate:

```
python -c "import datetime as d,sys; a=d.date.fromisoformat(sys.argv[1]); b=d.date.fromisoformat(sys.argv[2]); print(sum(1 for i in range(1,(b-a).days+1) if (a+d.timedelta(i)).weekday()<5))" <from YYYY-MM-DD> <today YYYY-MM-DD>
```

Calendar days = `(today - from).days`. Use the logged date when there is one for a send Claude
confirmed (`## Sent`, `nudge sent`, `reply sent`, `invite sent`). For a `typed, <word> to send` (any single word)
message, use the outbound date shown in the LinkedIn thread (the user may send it days later). When only LinkedIn's
relative label exists ("1 week ago", "Tuesday"), convert it to an absolute date and mark it `~` in
the manifest (e.g. `~2026-09-27`).

## 0. Pull the sources

Follow `.claude/skills/pull-sources.md`.

## 1. Collect

For each posting in scope read `outreach.md`:

- **`## Sent`**: parse every variant: the pipe bullet
  `- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:` + `>` quote; the same bullet
  without `text sent:` + an indented `>` quote; and the pipe bullet whose fifth field is the sent text in double quotes, after a prose line naming the channel (a company). A
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

One record per contacted person: posting dir, name, profile URL, **class**, channel, first-send
date, last action and date, nudge sent (yes/no). Class: `existing connection` when the Shortlist's
class column says so, or the `## Sent` channel is `message (existing connection)`; in older files
with no class column, a Shortlist degree of `1st` together with a `message` channel (not a
connection request); otherwise `new`. **Dedupe by profile URL** across postings: one LinkedIn
check per person; one state per posting. "Nudge sent" is computed across **all** `outreach.md`
files: any `nudge sent` action bullet for that profile URL counts, so a person gets one nudge
ever, not one per posting. A person nudged via another posting is classified from that nudge's
date (`done (no-response)` after ≥3 business days with no reply, else `waiting`), note
`nudged via <dir>`. Within one run a due nudge goes on the posting contacted first.

## 2. LinkedIn sweep

If more than 40 people have records, ask the user to confirm or narrow first. Wait 3–5 seconds
between page opens (browser wait action), and count page opens for the tab recycling in
`.claude/skills/linkedin-tab.md`.

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

A CAPTCHA, a rate limit or a "restricted activity" warning: stop, tell the user, no retries. At the end
record `Sent invitations at end: N` in the manifest header.

## 3. Classify

Exactly one state per person, checked in this order:

| # | State | Rule | Drafted next action |
|---|-------|------|---------------------|
| 1 | `done` | Left the company; or the conversation was closed by either side (declined, "not hiring", told to apply elsewhere); or nudged and no reply ≥3 business days after the nudge; or a stale invitation whose `## Follow-up` shows `replacement sent` or `none left`, still not accepted and with no inbound message; or withdrawn/expired | None. State recorded as `done (no-response)`, `done (closed)` or `done (left company)` |
| 2 | `replied` | An inbound message newer than the last outbound one | One-line summary, their text verbatim, a drafted response |
| 3 | `accepted` | Connected after our request, and no outbound message after acceptance other than the invitation note | Re-message them: the person's (b), re-checked against the resume, sent directly with no attachment (no approval: they are `new`). No (b) → a new follow-up from the posting's drafts and tailored resume, marked `new draft`. A previous `typed, <word> to send` (any single word) → note `typed <date>, not sent` |
| 4 | `silent` | A (b), free message (open profile), InMail (old logs) or direct message sent, no reply, ≥3 business days since the last outbound message, no nudge yet | One nudge, ≤300 characters |
| 5 | `stale-pending` | Invitation pending ≥10 calendar days | Leave the invitation. Add the next new person (step 3b) |
| 6 | `waiting` | Anything else | None |

A `## Sent` or `## Follow-up` entry on channel `free message (open profile)` is classified like a
sent (b): it can be `replied`, `silent` or `waiting`, never `accepted` or `stale-pending`.

**Nudge:** the role title, a reminder that the user is interested in it and messaged earlier, and one question:
is the role still open, and would they be open to a short chat or to pointing the user to the right
person. No new claims, no guilt-tripping.

**Reply:** answer only from the posting's tailored resume and `sources/profile.md`,
in the language of the reply (English or French). Anything neither covers (salary with no `sources/profile.md` rule, specific
availability, references) becomes a question in `questions.txt`, not a guess. A request to
schedule → ask the user for times; never invent any.

## 3b. Find new people

For each posting in scope whose `applications.md` row is not `closed` (and not unsubmitted:
`resume`, `ready`, `blocked`, `held`, `skipped`), add new people, up to **2 per posting per run**,
and up to **10 connection requests per run** in total:

- **How many:** one for each `stale-pending` person on the posting; plus one more when no contact
  on the posting is `replied`, `accepted` or waiting on a pending invite (everyone is `done` or
  `silent`). At least one when the posting has no contact at all.
- **Who, in order:** (1) the next person in Shortlist order who has no `## Sent`, `## Follow-up` or
  reconciled send, is not marked skipped / may have left / not at the company, and was not found
  `done (left company)`; (2) when the Shortlist runs out, a fresh LinkedIn people search at the
  company (current employees), as in `/outreach` step 2: the user's 1st-degree connections first, then
  recruiters for the posting's location and the likely hiring manager. Skip anyone already in any
  `outreach.md` (by profile URL). Check the current position. Append each person found to the
  Shortlist table (as a table row, above any `APPROVED <date>: outreach` line) with `added <date>` in the why column, and their class.
- **What:** a **new** person whose message composer says "Free message" (Open Profile; read the
  composer for every new person, per `.claude/skills/linkedin-tab.md`) gets their (b) as that free
  message. Otherwise a **new** person gets a
  connection request (no InMail unless the user OKs that person and text: if the composer shows InMail
  credits, send the connection request instead); with a note while the budget lasts (their
  "Short notes (200-char limit)" entry, else a new note ≤200 characters condensed from their (a),
  else written from the posting's drafts and tailored resume), otherwise without a note. Length
  checked by piping the note on stdin into
  `python -c "import sys; print(len(sys.stdin.read().rstrip(chr(10))))"` (heredoc in Bash). For a
  connection request, also write their (b) into `outreach.md` for when they accept. An **existing connection** gets a
  direct message drafted as in `/outreach` step 3, for approval.
- Nobody left to add on a posting → `none left`.

**Note budget:** count connection requests with a note dated this calendar month across all
`outreach.md` (`## Sent` channel `connection request with note`, or a channel containing
`connection request` with no `(no note)`, plus `## Follow-up` action `invite sent` with a note).
On Premium every request carries its note and this count is shown for information only. On a free
account, notes left = max(0, 3 − count); give them to hiring managers before recruiters. Requests beyond it
go without a note.

## 4. Review sheet

Create `batches/<YYYY-MM-DD-HHMM>-followup/`:

- `manifest.md`: header lines (run date, args, dry run yes/no, note budget, Sent invitations at
  start/end), then the table `# | Posting | Person | Class | State | Days | Last out | Last in | Proposed action | Approval | Result`
  (Approval: `needed` or `not needed`).
  Days: `N bd` (business days) for `silent`, `waiting` after a message and `done` by nudge; `N cd`
  (calendar days) for `stale-pending` and pending `waiting`; `-` otherwise.
- `review.md`: counts per state and the note budget at the top; then `## Needs your OK`: every
  message to an existing connection and every reply, **in full, verbatim** (for `replied`, their
  reply verbatim above the draft; flags `new draft`, `typed <date>, not sent`,
  `approved, not executed`); then `## Going out without approval`: the accepted follow-ups,
  nudges and new connection requests, in full, grouped accepted → silent → new people (flag
  `no note` past the budget); then `waiting` and `done` as short tables; `unparsed` lines; and a
  final `## No contacts` section for postings in scope with no contact found and nobody to add.
- `questions.txt`: plain text, numbered, **approval items only**. One item per message: who, which
  posting, `existing connection` or `reply`, the message verbatim, then `Answer:` (`ok` /
  `edit: <text>` / `skip`). Then reply questions from step 3. Header line: "Only `ok` or `edit:`
  approves; a blank `Answer:` counts as `skip`." No suggested answers. Open it with
  `Invoke-Item` (not in `--dry-run`).

Post a short summary in chat: counts per state, the note budget, no-contact postings, and **the
names of the existing connections awaiting approval** (`Your connections to OK: <Name> (<company>),
...`). If nothing needs approval, go straight to step 6. Otherwise go to step 6 for the
`not needed` items now, and wait for the user before the approval items. Nothing is approved by
silence; an approval of one message does not cover another. `--dry-run` ends here.

## 5. Record approvals

When the user says questions.txt is done, re-read it. For each `ok`/`edit:`, append an approval bullet
to that posting's `## Follow-up` (create the section at the end of `outreach.md` if missing):
`- APPROVED <date> | <Name> | <reply / message (existing connection)> | text:` + the
final text quoted. Save reusable answers to `sources/profile.md` through `.claude/skills/write-source.md` (as a rule when the answer carries
"always" or a condition). Anything unclear → ask before recording.

## 6. Execute

`not needed` items, plus approval items with an `ok`/`edit:`, text verbatim, one at a time,
waiting 3–5 seconds between page opens:

- **Nudge or reply** (no attachment): send in the thread; confirm it appears there.
- **Follow-up (b)** (no attachment): send it directly in the thread; confirm it appears there.
- **Free message (open profile)** to a new person: send their (b) as the free message; confirm it
  appears in the thread.
- **New connection request**: re-check any note is ≤200 characters in code; send the request;
  confirm it shows as pending.
- **Existing connection message**: only with its approval; send in the thread.
- No InMail unless the user OKs that person and text in chat. Attach nothing, and never say a resume is attached.
- After each confirmed send, write its action bullet immediately
  to that posting's `## Follow-up` (format in step 7), before the next item. A run that stops
  midway then never loses the record of a nudge already sent.
- A send that fails or hits a warning: stop and tell the user. No retries.

## 7. Log

- **`outreach.md`**, `## Follow-up`, one action bullet per person handled (sends were
  already logged in step 6; add the rest):
  `- <Name> | <date> | <state> | <action> | text:` + the quoted text if any. Actions:
  `follow-up sent`, `nudge sent`, `reply sent`, `invite sent` (a new
  person, `with note` / `no note`), `free message sent` (a new person, open profile), `message sent` (an existing connection), `replacement sent` /
  `none left` (the stale person), `none`.
  - A newly added person also gets a standard `## Sent` bullet
    (`- <Name> | <profile URL> | <free message (open profile) | connection request with note | connection request (no note) | message (existing connection)> | <date> | text sent:` + quote).
  - `typed, <word> to send` (any single word) is an old-log action only: parse it (see Dates and the `accepted` row),
    never write it.
  - A reconciled send gets a `## Sent` bullet in the same format, with `(reconciled <date>)`
    after the channel.
- **`applications.md`** (only writer this run). Rows: a plain dir → the row with that Posting dir;
  a `*-combined` dir → every row whose Posting dir, after `postings/`, starts with the same company
  prefix and whose dir name or req id is in the combined file's header.
  - Status changes only from `applied`, `outreach-ready`, `outreach-sent`, `outreach-only-ready`,
    `outreach-only-sent`, `in-conversation`, `no-response` or `closed`, checked in order: every contacted person `done` and at least one
    `done (closed)` → `closed`; every contacted person `done` with no reply → `no-response`; any
    person `replied`, or replied earlier in a conversation that is not closed → `in-conversation`;
    otherwise unchanged (a reconciled send or an acceptance only adds a Notes entry).
  - Unsubmitted rows (`resume`, `ready`, `blocked`, `held`, `skipped`) keep their status; the
    outcome goes in Notes only.
  - Every touched row gets a short note with the batch id.
  - Safety net: if the legend line lacks `outreach-only`, rewrite it to
    ``Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`; not applied: `outreach-only-ready` → `outreach-only-sent`.``
- **Manifest** Result column filled. Close the LinkedIn tab. Chat report: sent, skipped,
  stopped-on-warning.

## Guardrails

- Never message an existing connection, or send a reply, without an `ok` / `edit:` in this run.
- At most one nudge per person, ever; the `## Follow-up` action bullets are the record.
- At most 2 new people per posting and 10 connection requests per run; every new person is
  appended to the posting's Shortlist table before contact.
- Every factual claim from the posting's tailored resume or `sources/profile.md`.
- Stop on CAPTCHA, rate-limit or restriction warnings, and on any failed send.
