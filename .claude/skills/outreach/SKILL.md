---
name: outreach
description: Apply to a job posting (/apply) and then message people at the company on LinkedIn - Aly's own 1st-degree connections there first, then recruiters / hiring managers near the posting location as new connection requests. Messages to Aly's existing connections are approved by Aly (names shown first); new connection requests and messages to people who are not Aly's connections go out without approval. Use when the user runs /outreach.
argument-hint: <posting URL> | <posting dir>
---

# /outreach — /apply + LinkedIn messages, connections first

All paths are relative to `jobapps/`. Uses Chrome (load `claude-in-chrome` first); Aly is logged in
to LinkedIn. Keep volume low (at most 3 people per posting): LinkedIn flags automated-looking
activity, and the account is Aly's. All LinkedIn work happens in one tab, per
`.claude/skills/linkedin-tab.md` (direct URLs, recycled every 8 page opens, closed at the end).

## Resume link

Messages carry the tailored resume as a link, never an attachment (attaching left a tab open per
message, and the composer's cross-origin iframe blocks `file_upload` anyway). The link is one line
under the title of `postings/<dir>/outreach.md`: `Resume link: <url>`. Aly makes it: uploads the
posting's resume PDF (e.g. to Google Drive, shared as "anyone with the link can view") and gives
the URL. Drafts write `<resume link>` where it goes; the text sent has the real URL, and length
checks count it. Before the first send that uses a new link, open it once in the LinkedIn tab and
check that the PDF shows (not a sign-in page); otherwise ask Aly for a working one.

## Approval rule

| Person | Approval |
|--------|----------|
| **Existing connection**: 1st-degree when this run finds them (before any request from us) | **Required.** Show Aly their **names** (plus title and why) and the exact message; send only after an explicit OK for that person and that text |
| **Everyone else**: 2nd/3rd-degree, out of network, people Aly does not follow | **Not required.** Send the connection request / message, then report it |

A person stays in the class they had when first found: someone who accepts our request later is a
*new* connection, not an existing one (see `/followup`). Silence or an ambiguous reply never
approves an existing-connection message; an approval of one message does not cover another.

## Steps

0. **Pull the sources.** Follow `.claude/skills/pull-sources.md`, unless the skill that ran this one
   already pulled them in this run.
1. **Apply first.** Run the full `/apply` skill (both phases). If `applications.md` already shows
   this posting as `applied`, skip to step 2. If Aly decides not to submit, stop here.
2. **Find people** (LinkedIn people search in the run's LinkedIn tab, filtered to the company's
   current employees). Check each one still works there (current position).
   1. **Aly's connections first**: the same search with the Connections filter set to `1st`. Every
      1st-degree connection at the company is a candidate, whatever their role (anyone inside can
      refer or forward); rank engineers / managers on the posting's team, then recruiters, then
      the rest.
   2. **Then new people**: recruiter / talent acquisition / technical recruiter at the company,
      preferring ones covering the posting's location or Canada/North America; and the likely
      hiring manager (the eng/AI manager or lead for the team the posting describes, in the
      posting's location, or Aly's (Montreal) if the posting names several).
   - Write the shortlist (`## Shortlist` table in `postings/<dir>/outreach.md`): name, title,
     location, connection degree, **class** (`existing connection` / `new`), profile URL, and one
     line on why they fit. Up to 5 candidates, existing connections at the top.
   - Pick up to 3 to contact: existing connections first (up to 3), then fill the remaining slots
     with new people.
3. **Draft one message per picked person** (save all in `outreach.md`):
   - **Existing connection** → a direct message, 400–800 characters: friendly and personal (they
     know Aly), role title and that Aly applied, 1–2 concrete facts from the tailored resume that
     match the posting (from `sources/mega-resume.tex` only), the ask: a referral, forwarding
     to the hiring team, or a short chat; and the resume as `<resume link>`.
   - **New person** → (a) a connection note ≤ 200 characters (role, that Aly applied, one fact),
     length checked in code by piping it on stdin into
     `python -c "import sys; print(len(sys.stdin.read().rstrip(chr(10))))"`; and (b) the follow-up
     message for after acceptance, 500–800 characters, same content rules as above (resume link
     included), tailored to the reader: recruiter → fit + availability; hiring manager → the most relevant work. With Premium
     InMail credits, (b) can go now as an InMail with a subject ≤ 60 chars instead of (a).
   - No flattery filler, no claims beyond the resume.
4. **Approval gate, existing connections only.** Before anything is sent, show Aly in chat:
   - A line naming them: `Your connections at <company> I'd message: <Name>, <Name>.`
   - For each: title, why, and the exact message text.
   - Then the new people (name, title, channel, the note), for information only: they are sent in
     step 5 without waiting for an answer.
   - If `outreach.md` has no `Resume link:` line, ask for it in the same message: `Resume link for
     <company>? Upload <resume PDF path> and paste the URL.` Connection requests (a) carry no link
     and don't wait for it; an existing-connection message waits for both the OK and the link.

   Wait for Aly on the existing connections only: Aly picks who and OKs or edits each text. If there
   are no existing connections at the company, say so in one line and go on.
5. **Send**, one person at a time, waiting 3–5 seconds between page opens (in the one tab, per
   `.claude/skills/linkedin-tab.md`):
   - **New person**: send the connection request with note (a) right away, no approval needed;
     confirm it shows as pending. Notes are budgeted (below); past the budget send the request
     **without a note**, and (b) goes later through `/followup` once they accept.
   - **Existing connection**: only after the OK, the approved text verbatim (the resume link
     filled in) as a regular message; confirm it appears in the thread. Nothing is typed and left
     unsent for Aly.
   - A CAPTCHA, rate limit, "restricted activity" warning or failed send: stop and tell Aly. No
     retries.
6. **Log** each send in `postings/<dir>/outreach.md` under `## Sent`, one bullet per send in exactly
   this format (the `/followup` skill parses it):
   `- <Name> | <profile URL> | <channel> | <YYYY-MM-DD> | text sent:` followed by the text sent as a
   `>` quote on the next line(s). Channel is one of `message (existing connection)`,
   `connection request with note`, `connection request (no note)`, `InMail` (older files may show
   `typed, Aly to send` after the channel, from before resume links; `/followup` still reads it). Set the `applications.md` row to
   `outreach-sent` (or `outreach-ready` if an existing-connection message is waiting on Aly).
   Close the LinkedIn tab. End with a chat report: who was messaged (by name, existing connections
   marked), requests sent, anything waiting on Aly (an OK or the resume link). Later follow-ups are handled by `/followup`.

## Invitation and InMail budget

A free account gets about 3 personalized invitations (with a note) per month (seen 2026-10-04);
requests without a note are not capped that way, but LinkedIn limits them weekly, so send at most
10 connection requests per run across all postings. Count notes already sent this calendar month
across all `outreach.md` (`## Sent` channel `connection request with note`, plus `## Follow-up`
action `invite sent` with a note). Give the notes left to the most relevant new people (hiring
manager before recruiter); the rest go without a note. With Premium, check the remaining InMail
credits first and note the count in `outreach.md`.

## Running as a batch subagent

When the prompt says you are a batch subagent (orchestrated by the `batch` skill): skip step 0
(the orchestrator has already pulled the sources), then run the part the prompt names:

- **Application part**: `/apply` Phase 1 under its batch rules. Do not open LinkedIn.
- **LinkedIn part**: steps 2–3 in one LinkedIn tab of your own, per
  `.claude/skills/linkedin-tab.md`; close it at the end.

Either way **send nothing, submit nothing, connect with no one** (subagents must not act on Aly's
account at once). End with: posting dir, `ASK` count, blockers, the `outreach.md` path, and the
names of any existing connections found.

## Batch execute mode

Run on `postings/<dir>/`: first the application (`/apply` batch execute mode) if approved and not
yet `applied`; then step 5 for each **new** person in the shortlist's picks not marked skipped (no approval mark
needed) and for each **existing connection** marked `APPROVED <date>`, with the text **verbatim**;
all LinkedIn sends in one tab per `.claude/skills/linkedin-tab.md`, closed at the end; then log to
`outreach.md` only (the orchestrator owns `applications.md`; never write it in batch).
Never message an existing connection without an approval mark. Anything needing Aly (no working
`Resume link:` for a message that needs it, budget exhausted, CAPTCHA) → stop and reply `NEEDS ALY: ...`.
