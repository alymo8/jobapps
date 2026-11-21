# ADR 0008: Read the message composer before choosing a LinkedIn route

- **Status:** superseded by [0015](0015-manual-applying-and-outreach.md)
- **Date:** 2026-10-23

## Context

`/outreach` and `/followup` assumed a free LinkedIn account and treated any 2nd-degree "Message"
button as InMail, so new people got connection requests. In one company's outreach run, a recruiter
was offered to the user as an InMail when his composer had never opened; the user checked and the message
was free. Open Profile is a feature of the *recipient's* Premium: anyone can message an Open Profile
member for free, whatever the sender's plan or degree. Separately, the user's own plan had changed to
Premium (unlimited invitation notes, InMail credits), which the skills did not check.

## Decision

- Before the first send, check the user's plan (invite dialog "unlimited notes with Premium", the
  composer's InMail-credit line, "Reactivate Premium" in the top bar), and ask him if unclear. The
  free-account note budget applies only on a free plan.
- For each new person, open the message composer and read its header: "Free message" means a free
  message; an InMail-credit line means a connection request. Never infer the route from the degree
  or the profile buttons. The shared procedure is in `.claude/skills/linkedin-tab.md`.
- InMail moves from "never" to "only for a very relevant person, after the user OKs that person and that
  text in chat".

Alternatives: keep inferring from the degree (cheaper, but misses free messages, the case that
caused this); allow InMail without approval (spends a scarce credit on the user's account unasked).

## Consequences

One extra composer open per new person, which counts toward the 8-page tab recycle. More people get
a full message instead of a 200-character note. The Profile doc's "Never spend InMail credits" line
is now stricter than the skills; the user's per-person OK is the only way past it.
