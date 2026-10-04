---
name: outreach
description: Apply to a job posting (/apply) and then message 1-3 relevant people at the company on LinkedIn (recruiter / hiring manager near the posting location) with the resume attached; every person and message is approved by Aly before sending. Use when the user runs /outreach.
argument-hint: <posting URL> | <posting dir>
---

# /outreach — /apply + LinkedIn messages, human-in-the-loop

All paths are relative to `jobapps/`. Uses Chrome (load `claude-in-chrome` first); Aly is logged in
to LinkedIn and has Premium (InMail). **Nothing is sent to anyone until Aly has approved both the
person and the exact message text.** Keep volume low (at most 3 people per posting) — LinkedIn
flags automated-looking activity, and the account is Aly's.

## Steps

1. **Apply first.** Run the full `/apply` skill (both phases). If `applications.md` already shows
   this posting as `applied`, skip to step 2. If Aly decides not to submit, stop here.
2. **Find people** (LinkedIn search in a new tab; people search filtered to the company):
   - Recruiter / talent acquisition / technical recruiter at the company, preferring ones covering
     the posting's location or Canada/North America.
   - Likely hiring manager: the eng/AI manager or lead for the team the posting describes, in the
     posting's location (or Aly's, Montreal) if the posting names several.
   - Shortlist up to 5 candidates; for each: name, title, location, connection degree, profile URL,
     and one line on why they fit. Check they still work at the company (current position).
3. **Draft one message per person** (save all in `postings/<dir>/outreach.md`):
   - InMail subject (≤ 60 chars) + body of 500–800 characters: role title and that Aly applied, 1–2
     concrete facts from the tailored resume that match the posting (from `mega_resume.tex` only),
     a low-friction ask (a short chat or forwarding to the hiring team), sign-off with name.
   - Tailor to the reader: recruiter → fit + availability; hiring manager → the most relevant work.
   - No flattery filler, no claims beyond the resume.
4. **Approval gate (HITL).** Show Aly the shortlist and, for each proposed person, the exact
   subject + message. Wait. Aly picks who (up to 3) and approves or edits each message. Do not
   proceed on silence or an ambiguous reply; an approval of one message does not cover another.
5. **Send**, one approved person at a time:
   - 1st-degree connection: regular message with the resume PDF attached.
   - Otherwise: InMail (Message button on the profile, Premium) with the resume PDF attached.
   - If attaching isn't possible in that flow, tell Aly before sending and ask whether to send
     without it (with the posting link) or skip.
   - After sending, confirm the message appears in the sent thread with the attachment.
6. **Log** each send in `postings/<dir>/outreach.md` (name, profile URL, channel, date, text sent)
   and set the `applications.md` row to `outreach-sent` (or `outreach-ready` if waiting on Aly).

## InMail credits

Premium includes a limited number of InMail credits per month. Before drafting InMails, check the
remaining credits (LinkedIn shows them in the InMail compose window or Premium page) and note the
count in `outreach.md`. If there are fewer credits than proposed InMails, say so at the approval
gate and offer the fallback: a connection request with a note (≤ 300 characters, no attachment,
posting link instead), drafted and approved like any other message.

## Running as a batch subagent

When the prompt says you are a batch subagent (orchestrated by the `batch` skill): run `/apply`
Phase 1 under its batch rules, then steps 2–3 in your own tab, **send nothing, submit nothing,
connect with no one**. End with: posting dir, `ASK` count, blockers, and the `outreach.md` path.

## Batch execute mode

Run only on items marked `APPROVED <date>` in `postings/<dir>/`: first the application (`/apply`
batch execute mode) if approved and not yet `applied`, then step 5 for each approved person, with
the approved text **verbatim**, then log to `outreach.md` only (the orchestrator owns
`applications.md`; never write it in batch). Never message a person or send text that isn't marked
approved. Anything needing Aly (attachment impossible, out of InMail credits, CAPTCHA) → stop and
reply `NEEDS ALY: ...`.
