# Changelog: GC AI, Member of Technical Staff, Forward Deployed Engineer (Remote, Canada)

Verification: 1 page, fill 0.965, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, no collisions, dates aligned).

Source of facts: `mega-resume-v1.5.tex`. Location: remote across Canada; Aly is open to the 25% travel
and relocation (profile.md), so not a gap.

## Emphasized
- Customer-embedded delivery (the core of the role): summary leads with consulting and integrating
  LLM systems into enterprise client workflows; Accenture stakeholder bullet first; both client
  projects open with "sole engineer for a paying client" (discovery, embedding with a non-technical owner).
- Workflow automation in critical business processes (their contract review / procurement analogue):
  the agentic billing-verification automation for the engineering consulting client.
- API / integration work: REST APIs on Fargate, integration into the bank's Jenkins pipeline,
  async Lambda/SQS event processing, an AI gateway and MCP server on Clinic Ops.
- Compliance and documentation (nice-to-have + "reference implementations, documentation"):
  PDPL data residency deployment, human-in-the-loop gate, ADRs plus 5 runbooks on Cold-Chain.
- Research section dropped; Education placed before Projects as in the reference.

## Close-call cuts
- **claude-kit cut** (usual shortlist) to fit; it matches "repeatable patterns / best practices", but
  the client systems are stronger evidence for an FDE role.
- Safi cut (developer-platform/LLM-cost angle) and both MILA research entries cut.
- Accenture: LLM-as-a-judge summary evals, Langfuse observability, Gemini TTS PoC. SWE: CDK/
  CloudFormation, DynamoDB, Step Functions. Cold-Chain: "designed around how users work", agentic
  pipeline, backup hardening. Clinic Ops: caching, 584-test bullet.
- No age-rule override.

## Gaps vs the posting
- **5+ years building production software**: about 3 years full time (Sep 2023 onward) plus the
  Ericsson internship and side projects; below their floor.
- **3+ years directly with customers**: Accenture client work since 2023 plus 2026 solo client work; close
  to but arguably under 3 years of truly customer-facing time.
- **Webhooks**: no explicit webhook work in the mega resume (closest: SQS event processing, SSE pass-through
  in Safi, tokenized WhatsApp links).
- **Legal tech / procurement**: none; closest is compliance (PDPL) and billing verification.

## Please sanity-check
- Summary "3 years of consulting experience" frames Accenture (a consulting firm) as consulting;
  "paid systems" stands for the mega resume's "revenue-generating".
- SWE bullet 2 merges "synchronous and asynchronous microservices ... reducing pipeline run time by
  roughly 15 minutes" with the Lambda/SQS bullet; check the 15-minute saving is attributable to that set.
- Clinic Ops bullet 3 compresses the Azure/PDPL and human-in-the-loop bullets.

## Questions for Aly
- none
