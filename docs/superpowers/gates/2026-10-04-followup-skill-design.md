# Gate: /followup skill: design

- **Spec:** docs/superpowers/specs/2026-10-04-followup-skill-design.md
- **Spec SHA-256:** 31327f8ebfd2161830c9b9be2f09b1f8a181cbbe683509ce08bcdc92d88a8a0d
- **Verdict:** pass
- **Date:** 2026-10-04
- **Rounds:** 3 discovery + 1 verification (rerun after the user chose the `closed` status; the first run failed on that decision after 3 discovery rounds)

## Key decisions

- One inline pass with its own Chrome tab and one review sheet: no subagents, no /batch followup, no new Python tools
- Four situations plus waiting/done in fixed order: done > replied > accepted > silent > stale-pending > waiting
- Nudge after ≥3 business days of silence, at most one per person ever; nudged + 3 more business days → done (no-response)
- Invite pending ≥10 calendar days: leave it, propose the next unused shortlisted person (≤200-char note), at most one replacement per posting per run; once replaced (or none left) the stale person is done unless they accept or reply
- Claude sends approved nudges, replies and replacement invites; resume-bearing messages are typed and left unsent for the user
- Only explicit ok / edit: in questions.txt approves; a blank answer is skip
- Replies answered only from the tailored resume and profile.md; anything else becomes a question
- Default scope is every postings/*/outreach.md; hand sends are reconciled from LinkedIn into ## Sent (normal runs only)
- Older draft labels map to (a)/(b): Connection note(s) = (a), Follow-up message / InMail Body = (b); people with no (b) get a new draft marked new
- New applications.md statuses in-conversation, no-response, closed; submitted rows (applied, outreach-*, in-conversation, no-response, closed) transition; unsubmitted rows keep status, notes only
- *-combined outreach files map to rows by company prefix plus dir or req id in the header
- --dry-run writes only the batch dir; checked with SHA-256 hashes, not git status
- Out of scope: email, scheduling, people outside the shortlist, fixing the stale Premium line in outreach/SKILL.md

## Findings fixed

- run 1 round 1 [blocking] x4, [minor] x4: no-arg scope, dry-run reconcile writes, Sent log format, applications.md row mapping; criterion/legend/wording minors
- run 1 round 2 [blocking] x5, [minor] x1: replacement note length, stale lifecycle, who is swept, combined-file mapping, hash-based dry-run check; dry run doesn't open questions.txt
- run 1 round 3 [blocking] x2, [minor] x2: date-dependent criterion, applied rows transition; Invoke-Item and "step 1" wording
- The user decision: new `closed` status for postings where everyone is done and someone declined
- round 1 [blocking] Manifest lacked a day-count column: added Days column
- round 1 [blocking] Who writes the classifier check: verifier, by hand, in verification notes
- round 1 [blocking] Late reply couldn't move no-response/closed rows: those statuses now transition
- round 1 [minor] Legend edit duplicated; criterion 4 moved to Guardrails as a post-ship check
- round 2 [blocking] Blank Answer vs no approval by silence: blank = skip, no suggested answers
- round 2 [blocking] Postings without (a)/(b): new-draft rule
- round 2 [blocking] Stale done rule overrode replies: requires no inbound message
- round 2 [minor] x3: postings/ prefix, silent case outbound type, Premium line out of scope
- round 3 [blocking] a company / another company layout misdescribed: real layouts mapped to (a)/(b)
- round 3 [blocking] "All sends dated 2026-10-04" untrue: reconciled hand sends noted in criterion 2
- round 3 [minor] Legend runtime check labelled a safety net

## Plan questions

- Invite budget: count connection requests logged this calendar month vs read LinkedIn; block or warn when exhausted? (Design › Classify)
- Exact ## Follow-up layout; how Collect tells APPROVED from executed actions, incl. interrupted runs (Design › steps 1, 5, 7)
- Replacement invitee logging: ## Sent and/or ## Follow-up invite sent; source of first-send date (Design › steps 3, 7)
- "Unused" shortlisted person: order and exclusions (skipped, left, previously declined) (Design › Classify)
- Withdrawn/expired invitations (neither pending nor connected): which state? (Design › Classify)
- What marks (b) as sent; how a "typed, the user to send" (b) that was never sent is treated next run (Design › Classify)
- Days cell for states without a count (Design › Review sheet)
- Plain-dir arguments covered by a *-combined file, and company matches with no outreach.md (Design › Invocation)
- Where "no contacts" postings are listed (Design › Invocation)
- How left-company is detected (profile open vs thread) and sweep pacing/cap for ~85 searches (Design › LinkedIn sweep)
- Whether a reconciled hand send moves applied → outreach-sent; whether an accept moves no-response back (Design › Log)
- How "nothing sent on LinkedIn" is checked in the dry run (Success criteria 1)

## Open

- none
