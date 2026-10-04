# Plan gate: /followup skill Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-04-followup-skill.md
- **Plan SHA-256:** 45429457a4750120a035913edc307aef1ecfd65cfab87cdd6f2495fe3358e2af
- **Spec:** docs/superpowers/specs/2026-10-04-followup-skill-design.md
- **Spec SHA-256:** 31327f8ebfd2161830c9b9be2f09b1f8a181cbbe683509ce08bcdc92d88a8a0d
- **Verdict:** pass-with-decisions
- **Date:** 2026-10-04
- **Rounds:** 2 discovery + 0 verification
- **Decisions approved:** 2026-10-04

## Plan-introduced decisions

- Invite budget = connection requests logged this calendar month; remaining = max(0, 3 − count); exhausted budget only flags `over budget`, never blocks
- ## Follow-up holds separate APPROVED bullets and action bullets; state comes only from action bullets; an approval never executed shows `approved, not executed` and needs fresh approval
- A replacement invitee gets a standard ## Sent bullet plus an `invite sent` action; the stale person gets `replacement sent`
- "Next unused" = Shortlist order, excluding anyone already contacted, marked skipped / may have left / not at company, or found to have left
- Withdrawn or expired invitation → `done (no-response)`, note `invite withdrawn/expired`
- (b) counts as sent on any outbound message after acceptance; an unsent `typed, Aly to send` makes the person `accepted` again with note `typed <date>, not sent`
- Days cell: `N bd`, `N cd`, or `-` for replied/accepted/done (left company or closed)
- Plain dir with no outreach.md resolves to the *-combined dir naming it; company-prefix matches without outreach.md ignored; `no outreach for <arg>` when nothing matches
- `no contacts` postings listed in a final ## No contacts section of review.md and counted in the chat summary
- Sweep load: one pass over Sent invitations; reconcile unlogged shortlisted people from that page plus the Messaging conversation list (no per-name search); profiles opened only for people with a record (top Experience entry); 3–5 s between page opens; ask Aly first if >40 people have records
- A reconciled hand send or an acceptance never changes Status; Notes only
- Dry-run "nothing sent" proof: Sent-invitation counts at start and end recorded in the manifest and equal; never click Send/Connect/Withdraw
- Cross-posting dedupe by profile URL: one nudge per person across all postings; someone nudged via another posting is classified from that nudge (note `nudged via <dir>`)
- Replies drafted in the language of the inbound message (English or French)
- Relative LinkedIn dates converted to absolute and marked `~`; logged date wins
- Reusable answers saved to profile.md as a rule when the answer carries "always" or a condition
- The dry-run batch dir is committed on main as acceptance evidence after the merge

## Findings fixed

- round 1 [blocking] One nudge ever enforced only per posting: nudge-sent computed across all outreach.md by profile URL; check greps added
- round 1 [blocking] Task 3 "no new paths" had no baseline: git status snapshot before, diff after
- round 1 [minor] Censys Sent variant described accurately; Shortlist heading/columns described; prerequisite reason; duplicate cleanup removed; dropped applied→outreach-sent transition (spec says otherwise unchanged)
- round 2 [minor] Prerequisite updated to current clean main; argument-hint quoted for YAML; reload note for the new skill; expected states per run date; note length measured from stdin

## Open

- none
