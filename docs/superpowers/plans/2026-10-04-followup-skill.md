# /followup skill Implementation Plan

- **Status:** approved
- **Date:** 2026-10-04

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `/followup` Claude Code skill to the `jobapps` repo. It re-engages the LinkedIn contacts made by earlier `/outreach` runs: it sends the prepared follow-up after a connection is accepted, nudges people who went silent, drafts answers to replies, and replaces stale invitations. Every outgoing message is approved by the user first.

**Architecture:** A single Markdown skill file (`.claude/skills/followup/SKILL.md`), executed by Claude inline in the main session in its own Chrome tab, in the same style as the existing `apply`, `outreach`, `batch` and `resume` skills. Two small edits keep the neighbours consistent: `outreach/SKILL.md` step 6 and the `applications.md` legend. There is no product code. Date arithmetic is done with a one-line `python -c` command embedded in the skill, not a new tool file.

**Tech Stack:** Claude Code skills (Markdown with YAML frontmatter), the `claude-in-chrome` browser tools, Git Bash / PowerShell on Windows, Python 3 (stdlib only, for the date one-liner and verification hashes).

**Spec:** `docs/superpowers/specs/2026-10-04-followup-skill-design.md` (approved and gate-passed; read it before Task 1). This plan copies everything the executor needs from it.

## Context for a cold executor

- Repo: `<repo-root>` (remote `origin` = the GitHub remote, branch `main`). This is the user's personal job-application workspace. Refer to the user with they/them.
- `postings/<dir>/outreach.md` holds, per posting: a header (posting URL, application status), a shortlist table under a heading that starts with `## Shortlist` (e.g. `## Shortlist (current ... verified ..., 2026-10-04)`; columns `| # | Name | Title | Location | Degree | Profile | Why |`, with an extra `Role`/`Roles` column in the `*-combined` files), per-person drafts, an optional `## Short notes (200-char limit), APPROVED ...` section (these replace note (a) when sending), and a `## Sent` log.
  - **Draft labels:** (a) is a connection note and (b) is a follow-up to send after acceptance. In older files, a company has "Connection note" plus "Follow-up message", and a company has an InMail "Subject/Body" plus "Connection note (fallback)". "Connection note" / "Connection note (fallback)" count as (a); "Follow-up message" / InMail Body count as (b).
  - **`## Sent` bullet variants:**
    - `- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:` followed by `  > quoted text` (e.g. `postings/<Company>-<id>/outreach.md`);
    - the same pipe bullet with no `text sent:` field, followed by an indented `>` quote (three postings);
    - a pipe bullet whose fifth field is the sent text in double quotes, preceded by a prose line giving the channel (a company).
- `*-combined` dirs (`postings/<Company>-combined`) hold the outreach for several postings. Their `applications.md` rows point to the individual dirs. `<Company>-combined`'s header names the dirs; `<Company>-combined`'s header names only req ids (`<req-id>`, `<req-id>`).
- `applications.md` is a table `| Date | Company | Role | Location | Posting dir | Status | Notes |`. Its legend line (line 4) currently reads:
  `` Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent`. ``
- LinkedIn facts (observed 2026-10-04):
  - Premium has lapsed, so there are no InMail credits.
  - A free account gets about 3 personalized invitations per month, and an invitation note is limited to 200 characters.
  - The message composer is a cross-origin iframe, so Claude cannot attach the resume PDF. Messages that need the resume are typed and left unsent for the user to attach and send.
- Batch artifacts live in `batches/<YYYY-MM-DD-HHMM>-<mode>/`. The `/batch` convention for the user's input is a plain-text `questions.txt` with numbered items and `Answer:` lines, opened for the user with `Invoke-Item`.

## Prerequisites (do these first, in order)

1. **Clean, current `main`** (workspace rule):
   - Run `git -C <repo-root> branch --show-current` (expect `main`), then `git fetch` and `git status -sb`.
   - Expect `git status --porcelain` to show only `?? docs/` (the spec, gate records and this plan). Commit `docs/superpowers/` on `main` (or as the user directs) before branching. If anything else is uncommitted, **stop and ask the user**: a worktree branched from committed `main` would not contain it, and the merge could conflict.
2. **Worktree:** create one with the `superpowers:using-git-worktrees` skill, on branch `feat/followup-skill`. Tasks 1–2 run there.
3. Task 3 (dry run) runs in the **main checkout after merge**, because it needs the user's real `postings/` data, including any changes made since the merge. It also needs Chrome with the claude-in-chrome extension and the user logged in to LinkedIn.

## Decisions this plan adds (spec left them to the plan)

1. **Invite budget:**
   - Count the connection requests dated in the current calendar month across all `outreach.md` files. That means `## Sent` bullets whose channel contains `connection request`, plus `## Follow-up` bullets with action `invite sent`.
   - Remaining = max(0, 3 − count).
   - An exhausted budget does not block proposals. The review flags each replacement `over budget` and the user decides.
2. **`## Follow-up` layout:** two kinds of bullet in one section, in time order.
   - Approval bullets (step 5): `- APPROVED <YYYY-MM-DD> | <Name> | <kind: nudge / reply / follow-up (b) / replacement invite> | text:` + quote.
   - Action bullets (step 7): `- <Name> | <YYYY-MM-DD> | <state> | <action> | text:` + quote.
   - Collect derives state **only from action bullets**. An approval bullet with no later action bullet for the same person and kind is shown in the review as `approved, not executed (<date>)` and needs a fresh approval to send.
3. **Replacement invitee logging:** the new person gets a standard `## Sent` bullet (the source of their first-send date and channel) and an action bullet `invite sent` in `## Follow-up`. The stale person gets the action `replacement sent`.
4. **"Next unused" shortlisted person:** taken in Shortlist table order. Excluded:
   - anyone with a `## Sent`, `## Follow-up` or reconciled send;
   - anyone whose line in the file says skipped, may have left, or not at the company;
   - anyone found `done (left company)` in this sweep.
5. **Withdrawn or expired invitation** (not pending, not connected, no thread): `done (no-response)`, note `invite withdrawn/expired`.
6. **(b) counts as sent** when the thread shows any outbound message after the connection was accepted, other than the invitation note itself. A `typed, the user to send` action with no such message on the next run means the person is `accepted` again, and the review notes `typed <date>, not sent`.
7. **Days cell:**
   - `N bd` for `silent` / `waiting` with an outbound message, and for `done` by nudge;
   - `N cd` for `stale-pending` / pending `waiting`;
   - `-` for `replied`, `accepted`, and `done (left company | closed)`.
8. **Arguments:**
   - A plain posting dir with no `outreach.md` resolves to the `*-combined` dir whose header names that dir or its req id.
   - A `<company>` prefix ignores matching dirs with no `outreach.md`, and reports `no outreach for <arg>` only when nothing matches.
9. **`no contacts` postings** are listed in a final `## No contacts` section of `review.md` and counted in the chat summary.
10. **Sweep load:**
    - Pending invitations come from one pass over the Sent-invitations page.
    - Reconciling shortlisted people with no logged send uses that page plus the Messaging conversation list. Searching Messaging by name is only for people with a record.
    - Profiles are opened only for people with a record (left-company check, headline/Experience top entry).
    - Wait 3–5 seconds between page opens, using the browser tool's wait action.
    - If more than 40 people have records, ask the user to confirm or narrow the run before sweeping.
11. **Status side-effects:** none beyond the spec's rules. A reconciled hand send on an `applied` row, or an acceptance on a `no-response` / `closed` row, leaves the status unchanged ("otherwise unchanged"); the outcome goes in Notes.
12. **"Nothing sent" in a dry run:** the manifest header records the Sent-invitations count at sweep start and at the end. They must be equal, and the run never clicks Send, Connect or Withdraw.

## Global Constraints

- Nothing is sent to anyone without an explicit `ok` or `edit:` from the user in this run's `questions.txt`. A blank `Answer:` counts as `skip`.
- At most one nudge per person, ever. A nudge is ≤300 characters. A replacement invitation note is ≤200 characters, measured in code.
- Thresholds: `silent` after ≥3 business days (Mon–Fri, send day not counted); `stale-pending` after ≥10 calendar days; `done` ≥3 business days after a nudge.
- No people beyond the posting's existing Shortlist table. Every factual claim comes from the posting's tailored resume (`.tex`/`.pdf` in the posting dir) or `profile.md`.
- Stop with no retries on a CAPTCHA, a rate limit, a "restricted activity" warning or a failed send.
- `--dry-run` writes only `batches/<id>-followup/`.
- Out of scope:
  - new Python tool files, subagents, a `/batch followup` mode;
  - scheduling, email follow-ups;
  - fixing the outdated "has Premium (InMail)" line in `outreach/SKILL.md`.

## Review Focus

1. **A person who appears in two postings' shortlists** (same profile URL): they must get one LinkedIn sweep and one state per posting, and at most one nudge in total per run. Task 1's skill text says to dedupe by profile URL, and the Task 1 check greps for it.
2. **A `## Sent` bullet that matches none of the three known variants:** it must be listed as `unparsed`, never guessed or dropped. Pinned by a Task 1 grep.
3. **A reply in French** (the user is bilingual, and the postings are in Montreal): the drafted response is written in the language of the reply. Pinned by a Task 1 grep.
4. **The run is interrupted between steps 5 and 6** (approved, not sent): on the next run the person must not count as nudged. This is decision 2 above, pinned by a Task 1 grep for `approved, not executed`.
5. **The date line on LinkedIn is relative** ("1 week ago", "Tuesday"): use the logged date when one exists. Otherwise convert to an absolute date and mark it `~` in the manifest. Pinned by a Task 1 grep for `~`.

---

### Task 1: Write `.claude/skills/followup/SKILL.md`

**Files:**
- Create: `.claude/skills/followup/SKILL.md`

**Interfaces:**
- Consumes: the file formats described under "Context for a cold executor".
- Produces: the `/followup` skill. It defines the `## Follow-up` bullet formats (decision 2) and the `applications.md` statuses `in-conversation`, `no-response` and `closed`, which Task 2 adds to the legend and to `outreach/SKILL.md`.

- [ ] **Step 1: Write the structural check (it fails first)**

Save this to the session scratchpad as `check_followup_skill.sh` (not in the repo):

```bash
#!/usr/bin/env bash
# Structural checks for .claude/skills/followup/SKILL.md; prints FAIL lines, exits 1 on any.
f=.claude/skills/followup/SKILL.md
fail=0
need() { grep -qF -- "$1" "$f" || { echo "FAIL: missing: $1"; fail=1; }; }
[ -f "$f" ] || { echo "FAIL: $f not found"; exit 1; }
head -1 "$f" | grep -qx -- '---' || { echo "FAIL: no frontmatter"; fail=1; }
need 'name: followup'
need 'Use when the user runs /followup'
need 'argument-hint: "[<posting dir | company> ...] [--dry-run]"'
for s in '## 1. Collect' '## 2. LinkedIn sweep' '## 3. Classify' '## 4. Review sheet' \
         '## 5. Record approvals' '## 6. Execute' '## 7. Log' '## Guardrails'; do need "$s"; done
for st in '`done`' '`replied`' '`accepted`' '`silent`' '`stale-pending`' '`waiting`'; do need "$st"; done
need 'in-conversation'; need 'no-response'; need '`closed`'
need 'a blank `Answer:` counts as `skip`'
need 'approved, not executed'
need 'unparsed'
need 'profile URL'            # dedupe key
need 'language of the reply'
need '~'                      # approximate dates
need 'over budget'
need 'weekday()<5'            # business-day one-liner
need '--dry-run'
need 'Invoke-Item'
need 'typed, the user to send'
need 'replacement sent'
need 'nudged via'
need 'across **all**'
exit $fail
```

- [ ] **Step 2: Run it and see it fail**

Run: `bash "$SCRATCH/check_followup_skill.sh"` from the worktree root, with `$SCRATCH` set to the scratchpad path.
Expected: `FAIL: .claude/skills/followup/SKILL.md not found`, exit 1.

- [ ] **Step 3: Write the skill file**

Create `.claude/skills/followup/SKILL.md` with exactly this content:

````markdown
---
name: followup
description: Follow up with the LinkedIn contacts from earlier /outreach runs - send the prepared follow-up after a connection is accepted, nudge people who went silent, draft answers to replies, and replace stale invitations from the posting's shortlist; every message is approved by the user before sending. Use when the user runs /followup or asks to follow up or re-message people from previous outreach batches.
argument-hint: "[<posting dir | company> ...] [--dry-run]"
---

# /followup — re-engage earlier outreach contacts, human-in-the-loop

All paths are relative to `jobapps/`. Runs inline in this session (no subagents) in **one Chrome
tab of its own**: load `claude-in-chrome` first, create a new tab, never touch other tabs. The user is
logged in to LinkedIn on a free account (no InMail; about 3 personalized invitations a month;
invitation notes ≤200 characters). **Nothing is sent to anyone without an explicit `ok` or `edit:`
from the user in this run's `questions.txt`.**

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

Business days = Mon–Fri after the send day, up to and including today. Compute, never estimate:

```
python -c "import datetime as d,sys; a=d.date.fromisoformat(sys.argv[1]); b=d.date.fromisoformat(sys.argv[2]); print(sum(1 for i in range(1,(b-a).days+1) if (a+d.timedelta(i)).weekday()<5))" <send YYYY-MM-DD> <today YYYY-MM-DD>
```

Calendar days = `(today - send).days`. Use the logged date when there is one. When only LinkedIn's
relative label exists ("1 week ago", "Tuesday"), convert it to an absolute date and mark it `~` in
the manifest (e.g. `~2026-09-27`).

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

One record per contacted person: posting dir, name, profile URL, channel, first-send date, last
action and date, nudge sent (yes/no). **Dedupe by profile URL** across postings: one LinkedIn
check per person; one state per posting. "Nudge sent" is computed across **all** `outreach.md`
files: any `nudge sent` action bullet for that profile URL counts, so a person gets one nudge
ever, not one per posting. A person nudged via another posting is classified from that nudge's
date (`done (no-response)` after ≥3 business days with no reply, else `waiting`), note
`nudged via <dir>`. Within one run a due nudge goes on the posting contacted first.

## 2. LinkedIn sweep

If more than 40 people have records, ask the user to confirm or narrow first. Wait 3–5 seconds
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

A CAPTCHA, a rate limit or a "restricted activity" warning: stop, tell the user, no retries. At the end
record `Sent invitations at end: N` in the manifest header.

## 3. Classify

Exactly one state per person, checked in this order:

| # | State | Rule | Drafted next action |
|---|-------|------|---------------------|
| 1 | `done` | Left the company; or the conversation was closed by either side (declined, "not hiring", told to apply elsewhere); or nudged and no reply ≥3 business days after the nudge; or a stale invitation whose `## Follow-up` shows `replacement sent` or `none left`, still not accepted and with no inbound message; or withdrawn/expired | None. State recorded as `done (no-response)`, `done (closed)` or `done (left company)` |
| 2 | `replied` | An inbound message newer than the last outbound one | One-line summary, their text verbatim, a drafted response |
| 3 | `accepted` | Connected, and no outbound message after acceptance other than the invitation note | The person's (b), re-checked against the resume; the user attaches the resume. No (b) → a new follow-up from the posting's drafts and tailored resume, marked `new`. A previous `typed, the user to send` → note `typed <date>, not sent` |
| 4 | `silent` | A (b), InMail or direct message sent, no reply, ≥3 business days, no nudge yet | One nudge, ≤300 characters |
| 5 | `stale-pending` | Invitation pending ≥10 calendar days | Leave the invitation. Propose the next unused shortlisted person (below) |
| 6 | `waiting` | Anything else | None |

**Nudge:** the role title, a reminder that the user applied and messaged earlier, and one question:
is the role still open, and would they be open to a short chat or to pointing the user to the right
person. No new claims, no guilt-tripping.

**Reply:** answer only from the posting's tailored resume and `profile.md`, in the language of the
reply (English or French). Anything neither covers (salary with no `profile.md` rule, specific
availability, references) becomes a question in `questions.txt`, not a guess. A request to
schedule → ask the user for times; never invent any.

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

When the user says questions.txt is done, re-read it. For each `ok`/`edit:`, append an approval bullet
to that posting's `## Follow-up` (create the section at the end of `outreach.md` if missing):
`- APPROVED <date> | <Name> | <nudge / reply / follow-up (b) / replacement invite> | text:` + the
final text quoted. Save reusable answers to `profile.md` (as a rule when the answer carries
"always" or a condition). Anything unclear → ask before recording.

## 6. Execute

Approved items only, text verbatim, one at a time:

- **Nudge or reply** (no attachment): send in the thread; confirm it appears there.
- **Follow-up (b)**, or any approved text that says the resume is attached: type it in the thread
  and leave it **unsent** in its own tab; list those tabs for the user, who attaches the PDF and sends.
- **Replacement invite**: re-check the note is ≤200 characters in code; send the connection
  request with it; confirm it shows as pending.
- A send that fails or hits a warning: stop and tell the user. No retries.

## 7. Log

- **`outreach.md`**, `## Follow-up`, one action bullet per person handled:
  `- <Name> | <date> | <state> | <action> | text:` + the quoted text if any. Actions:
  `nudge sent`, `reply sent`, `typed, the user to send`, `invite sent` (the replacement person),
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
- **Manifest** Result column filled. Chat report: sent, typed for the user (with tab list), skipped,
  stopped-on-warning.

## Guardrails

- Never send anything not approved (`ok` / `edit:`) in this run.
- At most one nudge per person, ever; the `## Follow-up` action bullets are the record.
- No people beyond the posting's Shortlist table.
- Every factual claim from the posting's tailored resume or `profile.md`.
- Stop on CAPTCHA, rate-limit or restriction warnings, and on any failed send.
````

- [ ] **Step 4: Run the check and see it pass**

Run: `bash "$SCRATCH/check_followup_skill.sh"` from the worktree root.
Expected: no output, exit 0.

- [ ] **Step 5: Check the business-day one-liner**

Run each command; the expected output is in the comment:

```bash
B='import datetime as d,sys; a=d.date.fromisoformat(sys.argv[1]); b=d.date.fromisoformat(sys.argv[2]); print(sum(1 for i in range(1,(b-a).days+1) if (a+d.timedelta(i)).weekday()<5))'
python -c "$B" 2026-10-01 2026-10-06   # Thu -> Tue: 3
python -c "$B" 2026-10-02 2026-10-05   # Fri -> Mon: 1
python -c "$B" 2026-10-04 2026-10-07   # Sun -> Wed: 3
python -c "$B" 2026-10-04 2026-10-04   # same day: 0
```

Expected: `3`, `1`, `3`, `0`. Also confirm the one-liner in the file is identical to `$B`:
`grep -cF "$B" .claude/skills/followup/SKILL.md` → `1`.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/followup/SKILL.md
git commit -m "feat: add /followup skill for re-engaging outreach contacts

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

### Task 2: Wire `/followup` into `/outreach` and the `applications.md` legend

**Files:**
- Modify: `.claude/skills/outreach/SKILL.md` (step 6, the line starting `6. **Log** each send`)
- Modify: `applications.md:4` (the legend line)

**Interfaces:**
- Consumes: the statuses and the `## Sent` bullet format defined in Task 1's SKILL.md.
- Produces: nothing new for later tasks.

- [ ] **Step 1: Write the failing check**

Save this to the scratchpad as `check_wiring.sh`:

```bash
#!/usr/bin/env bash
fail=0
o=.claude/skills/outreach/SKILL.md
grep -qF '`/followup`' "$o" || { echo "FAIL: outreach has no /followup pointer"; fail=1; }
grep -qF -- '- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:' "$o" || { echo "FAIL: outreach lacks the required Sent format"; fail=1; }
grep -qF 'Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`.' applications.md || { echo "FAIL: legend not updated"; fail=1; }
exit $fail
```

- [ ] **Step 2: Run it and see it fail**

Run: `bash "$SCRATCH/check_wiring.sh"`
Expected: all three FAIL lines, exit 1.

- [ ] **Step 3: Edit `outreach/SKILL.md` step 6**

Read the current step 6 first, because the user's committed version may differ from the text below. Keep any existing content in it that this edit doesn't cover. The result must be:

```markdown
6. **Log** each send in `postings/<dir>/outreach.md` under `## Sent`, one bullet per send in exactly
   this format (the `/followup` skill parses it):
   `- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:` followed by the text sent as a
   `>` quote on the next line(s). Set the `applications.md` row to `outreach-sent` (or
   `outreach-ready` if waiting on the user). Later follow-ups (accepted connections, nudges, replies)
   are handled by `/followup`.
```

- [ ] **Step 4: Edit the `applications.md` legend (line 4)**

Replace:
``Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent`.``
with:
``Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`.``
Touch no other line.

- [ ] **Step 5: Run both checks**

Run: `bash "$SCRATCH/check_wiring.sh"; bash "$SCRATCH/check_followup_skill.sh"`
Expected: no output, both exit 0. Then run `git diff --stat`, which should show only these two files changed in this task.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/outreach/SKILL.md applications.md
git commit -m "docs: point /outreach at /followup; add follow-up statuses to legend

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

**Review checkpoint:** after Task 2, integrate the branch into `main` with `superpowers:finishing-a-development-branch` (the user picks merge or PR). Task 3 runs on `main`.

### Task 3: Dry-run acceptance on real data (main checkout)

**Files:**
- Create (by the skill): `batches/<YYYY-MM-DD-HHMM>-followup/manifest.md`, `review.md`, `questions.txt`
- Scratch only: `$SCRATCH/hashes-before.txt`, `$SCRATCH/hashes-after.txt`, `$SCRATCH/classifier-check.md`

**Interfaces:**
- Consumes: the merged `/followup` skill and the user's real `postings/` data.
- Produces: the evidence for the spec's success criteria.

- [ ] **Step 1: Hash the files the dry run must not touch**

```bash
cd <repo-root>
python - > "$SCRATCH/hashes-before.txt" <<'EOF'
import glob, hashlib
for p in sorted(["applications.md", "profile.md", *glob.glob("postings/*/outreach.md")]):
    print(hashlib.sha256(open(p, "rb").read()).hexdigest(), p)
EOF
ls batches > "$SCRATCH/batches-before.txt"
git status --porcelain --untracked-files=all > "$SCRATCH/status-before.txt"
```

- [ ] **Step 2: Run the dry run**

Make sure the user is available, since a LinkedIn warning stops the run. If `followup` is not in this session's available-skills list, start a new Claude Code session in the main checkout (or run `/reload-plugins`) first. Then invoke `/followup --dry-run` (Skill tool, skill `followup`, args `--dry-run`) and follow the skill.
Expected:
- A new `batches/<id>-followup/` with three files.
- A chat summary.
- No Send, Connect or Withdraw click.
- `Sent invitations at start` equals `at end` in the manifest header.

- [ ] **Step 3: Check that nothing else changed**

```bash
python - > "$SCRATCH/hashes-after.txt" <<'EOF'
import glob, hashlib
for p in sorted(["applications.md", "profile.md", *glob.glob("postings/*/outreach.md")]):
    print(hashlib.sha256(open(p, "rb").read()).hexdigest(), p)
EOF
diff "$SCRATCH/hashes-before.txt" "$SCRATCH/hashes-after.txt" && echo HASHES-IDENTICAL
ls batches | diff "$SCRATCH/batches-before.txt" - 
```

Expected:
- `HASHES-IDENTICAL`.
- The batches diff shows exactly one added line, `> <id>-followup`.
- `git status --porcelain --untracked-files=all | diff "$SCRATCH/status-before.txt" -` shows only added lines, all under `batches/<id>-followup/`.

- [ ] **Step 4: Check the manifest against the rules**

For every person in every `postings/*/outreach.md` `## Sent` log, plus every `(reconciled ...)` record:
- They appear in `manifest.md` with exactly one state.
- That state is the one the step 3 table gives for today's date, using the Days and Last out/in columns.
  - People logged on 2026-10-04 get whichever state the step 3 table gives on the run date (e.g. `stale-pending` from 2026-10-14 for invitations still pending, `silent` from 2026-10-07 for unanswered direct messages).
  - Reconciled contacts (one messaged in September, another pending before 2026-10-04) may be `silent`, `stale-pending` or `done`. Check them with their LinkedIn dates.

List any mismatch as a defect.

- [ ] **Step 5: Classifier table check (by hand)**

Write `$SCRATCH/classifier-check.md` with each case worked from the step 3 rules and the date one-liner:

| Case | Expected |
|------|----------|
| (b) sent Thu 2026-10-01, checked Tue 2026-10-06, no reply, no nudge | 3 bd → `silent` |
| (b) sent Fri 2026-10-02, checked Mon 2026-10-05 | 1 bd → `waiting` |
| Invite sent 2026-10-04, still pending on 2026-10-14 | 10 cd → `stale-pending` |
| Nudged Thu 2026-10-01, no reply, checked Tue 2026-10-06 | 3 bd → `done (no-response)` |
| Inbound reply newer than last outbound, a nudge was also due | `replied` |

Expected: every row matches.

- [ ] **Step 6: Report**

Tell the user:
- the batch dir path and the counts per state;
- the result of each criterion (hashes, manifest coverage, invitation counts, classifier table), with the evidence lines.

- [ ] **Step 7: Commit the dry-run evidence**

```bash
git add batches/<id>-followup/
git commit -m "chore: /followup dry-run acceptance batch

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

(The batch dirs are tracked in this repo, like the earlier `batches/*-outreach/` runs.) The worktree and branch were already removed at the Task 2 checkpoint; delete the scratch files (`$SCRATCH/*.sh`, `*.txt`, `classifier-check.md`) after reporting.

## Success criteria (from the spec)

1. The dry run on real data:
   - lists every `## Sent` and reconciled person in `manifest.md` with exactly one state, each the state the step 3 table gives for the run date, with the Days count shown;
   - sends nothing;
   - leaves the SHA-256 hashes of `applications.md`, `profile.md` and all `postings/*/outreach.md` identical, and creates new files only under `batches/<id>-followup/` (Task 3).
2. The five synthetic classifier cases match (Task 3, Step 5).
3. `followup/SKILL.md` has the frontmatter `name`, a `description` triggering on `/followup`, an `argument-hint` and numbered steps, and the `outreach` and `applications.md` edits match the spec (Tasks 1–2 checks).
