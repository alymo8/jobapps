# Changelog: Decagon, Agent Deployment Engineer (Toronto, on-site)

Verification: 1 page, fill 0.967, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (removed orphan words on the eval,
LLM-judge, and guardrails bullets and a 3-line summary).

Source of facts: `mega-resume-v1.5.tex`. Posting used as saved in `posting.md` (no refetch).

## Emphasized
- End-to-end delivery of AI agents with enterprise customers (their core ask): summary leads with it;
  the Accenture billing agent opens with the stakeholder / success-criteria / production-deployment
  bullet, then its router + parallel-subagent architecture.
- Evaluation and regression against drift ("evaluation and regression-testing frameworks ... guard
  against performance drift"): Langfuse eval framework vs the manual process, plus the LLM-as-a-judge
  bullet restored for "early detection of performance degradation"; new "Evals & Guardrails" skills line.
- Guardrails: Clinic Ops bullet reworded as layered guardrails (flag-not-infer, system-channel isolation,
  strict schemas, human review); prompt-injection hardening in skills.
- Customer-support relevance (Decagon is conversational AI for CX): the call-summary / live
  recommendations service for support associates.
- Customer-facing, ambiguous delivery: both paid solo client systems (discovery, embedding with a
  non-technical owner, production cutover, runbooks).
- Research section dropped (space; not core to a delivery role); Education before Projects as in the reference.

## Close-call cuts
- Age rule: considered overriding for the Vodafone chatbot (43M customers), since this is a
  conversational-AI role, but did not: the recent Accenture customer-support LLM work is a stronger,
  current signal and space was tight.
- Accenture: Langfuse observability bullet (tracing of prompts/outputs; would map to "execution traces"),
  Gemini text-to-speech conversational support-agent PoC, Gemini dashboard chatbot.
- Safi (eval-backed LLM optimization) and both MILA research projects; claude-kit cut to 1 bullet;
  Software Engineer REST/Fargate/Lambda clause.

## Gaps vs the posting
- Asks for 5+ years in a technical customer-facing role (solutions / forward-deployed / consulting);
  Aly has ~3 years full time at Accenture (consulting) plus solo client work.
- No direct experience named with CRM or ticketing-system integrations, or voice/chat CX platforms.
- No PRD-writing evidence on the resume (closest: specs/ADRs and customer discovery).
- Location: on-site Toronto; Aly will relocate (profile.md), so header unchanged.

## Please sanity-check
- Summary "deploying production AI agents with enterprise customers, from success criteria to evals and
  launch" is a synthesis of the billing-agent bullets.
- Skills "Langfuse tracing" is backed by the mega resume's observability bullet, which is not on this page.
- Clinic Ops "human review of every draft" compresses "a human-in-the-loop gate where every output is a
  draft the doctor accepts".

## Questions for Aly
- none
