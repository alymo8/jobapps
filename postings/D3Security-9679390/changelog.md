# Changelog: D3 Security, Agentic AI Engineer (Vancouver, in office)

Verification: 1 page, fill 0.96, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, no collisions, dates aligned).

Source of facts: `mega-resume-v1.5.tex`. Location: Vancouver in-office only; Aly is willing to
relocate and work onsite (profile.md), so not a gap.

## Emphasized
- Agent design patterns (planning, tool use, orchestration): router agent with parallel subagents
  (billing), LangGraph plan-execute fraud agent with RAG, MCP server, Anthropic structured outputs.
- Guardrails, validation, human-in-the-loop: Clinic Ops hallucination / prompt-injection bullet
  (strict schemas, flag-don't-infer, every output a draft the doctor accepts), AI gateway with audit logging.
- Testing, evaluation, observability (responsibility + nice-to-have): Langfuse eval framework vs the
  manual process, LLM-as-a-judge with Langfuse tracing, provider-failure taxonomy, 584-test suite with CI.
- Ambiguous requirements into structured plans: stakeholder bullet on the billing system.
- Full-stack / "Python and/or C#": React/TypeScript operator frontend; Stocate added for C#/.NET + React.
- AI coding tools (nice-to-have): claude-kit (Claude Code plugin, spec-plan-build, AI review gate).
- Fraud detection agent for a bank is the closest hit to their security-operations alert domain.
- Research section dropped (posting says "not research or model training"); Education before Projects.

## Close-call cuts
- **Cold-Chain Dispatch cut** to fit (usual shortlist); its "agent output treated as untrusted" bullet
  was a good fit, but claude-kit covers AI-assisted development and Stocate covers C#.
- **Leagueware cut** (named exception) in favour of Stocate, which carries the C#/.NET requirement.
- Safi, both MILA research entries, Gemini dashboard chatbot, Gemini TTS PoC, monitoring/Splunk bullet,
  SWE CDK/DynamoDB/Step Functions bullets cut.
- No age-rule override.

## Gaps vs the posting
- **Cybersecurity**: no security-product experience; closest are the bank fraud-detection agent,
  prompt-injection hardening, and secret scanning in claude-kit.
- **C#**: only from the Stocate startup project (Stripe back end); professional work is Python/Java/TypeScript.
- **Agent memory**: no explicit memory-design work in the mega resume (RAG over history is the closest).
- Kubernetes: Ericsson internship only.

## Please sanity-check
- Accenture bullet 1 names only "Azure AI Foundry" (mega: AI Foundry, Azure ML, Azure Containers) and
  says "a client" for the engineering consulting client.
- Accenture LLM-as-a-judge bullet folds in "Langfuse tracing" from the separate observability bullet
  (same call-summarization app).
- claude-kit bullet 1 says "AI-assisted engineering workflow" for the mega's "agentic engineering conventions".
- MongoDB stays in Databases though Leagueware (its backing project) is not on this page.

## Questions for Aly
- none
