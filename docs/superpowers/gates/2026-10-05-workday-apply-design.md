# Gate: Workday applications in /apply and /batch: design

- **Spec:** docs/superpowers/specs/2026-10-05-workday-apply-design.md
- **Spec SHA-256:** a05025676b6862a5f9a669076225df11fc3e0f64d0d841c6c16bc0ef53951cb9
- **Verdict:** pass
- **Date:** 2026-10-05
- **Rounds:** 3 discovery + 1 verification

## Key decisions

- Claude signs in to Workday only through Chrome's saved-password autofill plus clicking Sign In; it never types passwords and never fills Create Account. With no usable login, the user signs in or creates the account in the tab (normal run); a batch records it as BLOCKED with Detail `NO-WORKDAY-LOGIN <tenant> <workday url>: ...` (Decision 1, Playbook 3, ADR 0001).
- Save and Continue drafts need no approval; the single approval point is before the consent checkbox, and "ok" covers ticking it, filling the `After approval` steps and submitting. With no consent checkbox, the run stops on the last pre-Review step, unsaved (Decision 2, Playbook 9-11).
- Always Apply Manually; never Autofill with Resume or Use My Last Application; an existing draft is resumed (Decision 3).
- Existing Work Experience and Education entries in a tenant's Workday profile are edited or deleted to match `## Workday work history` (Decision 4).
- My Experience comes from a local, the user-approved `## Workday work history` section in `profile.md`, built from `mega-resume-v1.5.tex`; in batch, the orchestrator builds it before stage 2, asked with the launch confirmation (Decision 5).
- Workday blockers reuse the BLOCKED/FAILED reasons with Detail prefixes `NO-WORKDAY-LOGIN <tenant> <workday url>` / `NO-WORKDAY-HISTORY`; existing rows get the prefix on their next retry; retries use `/batch <apply|outreach> dlq.md --reason BLOCKED`.
- The review sheet's "Workday logins needed" list spans every open NO-WORKDAY-LOGIN row in dlq.md, grouped by tenant, with the Workday URL from the Detail.
- Tenant name: `<tenant>.wdN` for both myworkdayjobs.com and myworkdaysite.com (path after /recruiting/).
- Cookie banner always declined. Batch execute never writes applications.md.
- Out of scope: other account-walled ATSs, tools/ changes, Chrome extension site-permission denials.

## Findings fixed

- round 1 [blocking] Tenant rule wrong for myworkdaysite.com: per-host tenant rule added.
- round 1 [blocking] NO-WORKDAY-LOGIN vs DLQ reason codes: rows are BLOCKED/FAILED with a Detail prefix.
- round 1 [blocking] Batch handling of missing history undefined: orchestrator builds it before stage 2; NO-WORKDAY-HISTORY fallback.
- round 1 [blocking] Approval point when consent is absent or followed by more steps: consent step, After approval rows and no-consent case specified; Phase 2 re-fills the unsaved step.
- round 1 [blocking] Batch execute would write applications.md: section 11 writes it only in normal runs.
- round 1 [minor] Two sources for Websites: removed from the history format; read from Contact.
- round 1 [minor] "steps 3-5" corrected to "steps 3-6".
- round 2 [blocking] Scope vs Design on apply/SKILL.md sections: Scope In clarified (step 6 and Phase 2 covered by workday.md).
- round 2 [blocking] Tenant sign-in URL undefined: defined.
- round 2 [blocking] Scope of "Workday logins needed": every open row in dlq.md, this run's marked.
- round 2 [minor] Launch confirmation named correctly; background counts corrected (13 open, Salesforce resolved, Mastercard added).
- round 3 [blocking] Sign-in URL wrong for postings found off Workday: Detail carries the Workday URL; list uses it.
- round 3 [minor] Existing DLQ rows get the prefix on retry; retry mode matches the row; Scope In lists the batch history step.

## Plan questions

- Should same-tenant postings be serialized in batch stages 2 and 5 (shared Chrome session)? (/batch SKILL.md changes)
- How are prompt-picker searches (Skills, Field of Study, How Did You Hear) triggered without Enter, and is a field with no suggestions ASK/FAILED rather than a silent skip? (Playbook 6-7)
- How are Address Line 1 / City / Province / Postal Code split from the one-line Contact address? (Playbook 6)
- Should the orchestrator treat postings whose posting.md or DLQ Detail names a Workday tenant as Workday for the pre-stage-2 history check? (/batch SKILL.md changes)
- Should the batch review sheet show tenant, stop step, consent label and After approval rows per Workday posting? (Playbook 10, /batch changes)
- Which URL is "the Sign In element ref" taken from (find vs read_page)? (Playbook 2-3)
- How is the 2-posting batch criterion selected (URLs vs --rows), and how is "no password typed" evidenced (subagent tool-call review)? (Success criteria 3)

## Open

- none
