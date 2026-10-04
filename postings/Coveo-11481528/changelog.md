# Changelog: Coveo, Forward Deployed Engineer (FDE)

Verification: 1 page, fill 0.967, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no collisions, no orphan words, dates
and rules aligned).

Source of facts: `mega-resume-v1.5.tex`. Base layout reused from the 11x FDE resume (same preamble
as `latex_resume.tex`).

Eligibility: posting says "Remote (2 locations available)"; Coveo is a Quebec company and the
listing is on Built In Toronto. Aly is Montreal-based, bilingual EN/FR and open to relocation or
hybrid/onsite, so no eligibility issue.

## Emphasized
- Prototyping (their core ask): summary leads with prototypes and production AI systems built from
  customer requirements across APIs, data pipelines and full-stack apps (their exact triad); kept the
  Gemini 2.5 Pro proof of concept and added the AWS Step Functions proof of concept (SWE role).
- Data pipelines: the real-time Kinesis/Flink transcript pipeline bullet, Kinesis and Flink in Skills.
- RAG / search-adjacent (Coveo's product is AI search and retrieval): restored the LangGraph fraud
  agent with RAG (96% on 500 transactions); RAG leads the LLMs & Agents line.
- Customer-facing / bridging business and tech: Accenture stakeholder bullet first, "sole engineer for
  a paying client" on both client systems, Clinic Ops customer discovery that disproved the original
  thesis (mirrors "experimentation-driven mindset", "refine customer needs").
- Production readiness: Cold-Chain cutover and runbooks; Clinic Ops real-API smoke harness and
  human-in-the-loop gate.

## Close-call cuts
- **Safi** was in the first draft (FastAPI recorder, eval honesty story) but pushed the page to 2;
  cut it rather than client-system bullets.
- **claude-kit** cut; the client systems are stronger evidence for a customer-deployment role.
- Research section (both MILA papers) cut.
- Accenture: Langfuse observability, LLM-as-a-judge summary evals, Gemini dashboard chatbot,
  monitoring/alerting. SWE: CDK/CloudFormation, DynamoDB indexing. Cold-Chain: agentic pipeline,
  116-test bullet, backup fix. Clinic Ops: Azure PDPL deployment, prompt-injection details.

## Gaps vs the posting
- **Years:** posting asks for 7+ years hands-on; Aly has about 3-4 years full time (plus internships).
  This is the main gap; the posting says "you don't need to check every box".
- Level is Senior; no formal senior/lead title in the mega resume.
- No direct search/relevance-engine (Coveo platform) experience; closest is RAG in the fraud agent
  and the Clinic Ops LLM workflows.

## Please sanity-check
- Summary "AI engineer (3 years) building prototypes and production AI systems from customer
  requirements across APIs, data pipelines, and full-stack apps" is a synthesis of the Accenture
  and client-project bullets.
- Clinic Ops bullet 3 combines the source's smoke-harness/failure-taxonomy bullet with the
  hallucination-mitigation bullet (strict schemas, human-in-the-loop draft gate).
- TTS bullet says "proof of concept of the support call"; the source says "of the call summarization
  process ... using Gemini 2.5 Pro as the support agent".

## Questions for Aly
- none
