# Gate: Outreach without apply: design

- **Spec:** docs/superpowers/specs/2026-10-19-outreach-without-apply-design.md
- **Spec SHA-256:** 54c7b3039f1fa134696b2216131ead2e4228bcd8ba93a2f8c006017e87122998
- **Verdict:** pass
- **Date:** 2026-10-19
- **Rounds:** 3 discovery + 1 verification

## Key decisions

- `/outreach` is LinkedIn-only by default; it applies only with `--apply` or when the user asks in plain words; when unsure it does not apply.
- The tailored resume is still built when outreach runs without applying.
- New `outreach-only-ready` / `outreach-only-sent` statuses; every post-submit writer (`/apply`, `workday.md`, `/batch` orchestrator) maps them to `outreach-ready` / `outreach-sent`; prepare leaves them unchanged.
- `--apply` on an already-messaged row (`outreach-only-*`, `in-conversation`, `no-response`, `closed`) applies only and messages no one, in both `/outreach` and `/batch outreach`; on `outreach-ready` / `outreach-sent` it skips `/apply`.
- A continued run on an already-messaged row keeps the status and notes `outreach again <date>` (with `, approval pending` while an approval waits).
- The applied/not-applied fact is lost once a row reaches `in-conversation` / `no-response` / `closed`; the guard is the auto-memory never-reapply rule plus `/apply`'s submit OK.
- `read_postings.py --for outreach` picks applied-but-not-messaged postings and skips every messaged status; the default skip set is unchanged.
- `/batch outreach` without `--apply` records `APPROVED <date>: outreach` (the user's reply without a skip), which admits postings with only new people to execute; no "Mark as applied?" prompt.
- The profile.md LinkedIn rules move into the skills: "interested", never "applied"; nothing attached; never InMail; free message when offered (also `/followup` step 3b); existing-connection messages sent directly after approval.
- ADR 0005's approval classes and the caps are unchanged; ADR 0006 records this change.

## Findings fixed

- round 1 [blocking] `--apply` on an already-messaged posting re-messages the same people: `--apply` on `outreach-only-*`/conversation rows runs `/apply` only; same for `/batch outreach --apply`.
- round 1 [blocking] Execute-stage gate drops outreach-only postings with no existing connections: stage 4 records `APPROVED <date>: outreach`, which stage 5 counts.
- round 1 [minor] Legend safety net skills unclear: named outreach, apply, batch and followup.
- round 1 [minor] Criterion 3 omitted draft-heading parsing: added.
- round 1 [minor] Rerun on `*-ready` rows: step 1 reuses drafts, re-shows the approval, skips people already sent.
- round 2 [blocking] `/apply` Phase 1 overwrote `outreach-only-*` with `ready`: prepare leaves the status, Notes records the form fill.
- round 2 [blocking] `/batch apply` post-submit write unspecified: every post-submit writer applies the mapping, from the pre-run status.
- round 2 [blocking] `/outreach --apply` on `outreach-ready`/`outreach-sent` undefined: skips `/apply`, follows no-apply step 1 rules.
- round 2 [blocking] `/followup` free-message route ambiguous: step 3b uses the new-person route; free-message channel classified like a sent (b).
- round 2 [minor] Criterion 4 manual: now an `rg` listing attributed in the PR description.
- round 2 [minor] `ready` state dropped silently: Notes gets `form filled <date>, not submitted`.
- round 3 [blocking] Workday prepare path wrote `ready`: `workday.md` section 10 in scope and follows the prepare rule.
- round 3 [blocking] Batch vs single `--apply` mismatch: batch exemption extended to conversation statuses.
- round 3 [blocking] Status after "continue" undefined: unchanged, Notes `outreach again <date>`.
- round 3 [minor] Reapply guard wording: corrected.
- verify 1 [minor] Continued-run rule overlap and stranded approval: marked as an override; `approval pending` note tracked by step 1.

## Plan questions

- How does the stage-5 execute subagent learn the mode: a `Mode:` line in the execute prompt, or the presence of `APPROVED <date>: submit`? (Design, `/outreach` batch sections)
- Which section of `outreach.md` holds `APPROVED <date>: outreach`, and what exact line does stage 5 match? (Design, `/batch outreach`)
- Do stages 1a.5 and 1b skip or leave unchanged the status of postings picked by `--for outreach` whose row is already `applied` (record the pre-run status from `postings.json`)? (Design, `/batch outreach`)
- In outreach-only mode, is the stage 4 `application.md` write suppressed entirely? (Design, `/batch outreach`)
- How do tests feed an `applications.md` fixture (patch `read_postings.ROOT`)? (Success criteria 1)

## Open

- none
