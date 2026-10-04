# Changelog: Salesforce, Forward Deployed Engineer (FDE) (Mid/Senior Level), Toronto

Verification: 1 page, fill 0.964, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no collisions, no orphan words).
Source of facts: `mega-resume-v1.5.tex`.

## Emphasized
- Customer-facing delivery (a stated hard requirement): summary leads with consulting experience
  deploying production AI agents for enterprise clients; Accenture stakeholder bullet first; "sole
  engineer for a paying client" on both client systems, with customer discovery and embedding with a
  non-technical owner.
- Agent intelligence (prompts, reasoning, tool calls, integration): router agent with parallel
  subagents, LangGraph plan-execute fraud agent with RAG, Anthropic structured outputs behind an AI
  gateway, MCP server.
- "Evaluate AI outputs with engineering rigor" / "explain why a prompt failed": Langfuse benchmark vs
  the manual process, LLM-as-a-judge summary evals with tracing, hallucination and prompt-injection
  mitigation.
- Data pipelines: real-time Kinesis/Flink transcript pipeline.
- AI-powered development (posting names Cursor and Claude): kept claude-kit and the Claude Certified
  Architect certification.
- Research section dropped; Education placed before Projects as in the reference.

## Close-call cuts
- Gemini/Vertex AI dashboard chatbot (partial match to "agent performance dashboards"): cut for space.
- Cold-Chain production cutover / RLS / runbooks bullet and the claude-kit agent-constraints bullet:
  cut for space (each project now has 1 bullet, below the prompt's 2-3; Clinic Ops kept at 3).
- Safi, Stocate, Research (both MILA papers), Gemini 2.5 Pro text-to-speech PoC, monitoring/alerting
  bullet, SWE CDK/CloudFormation/DynamoDB/Step Functions bullets.
- No age-rule override.

## Gaps vs the posting
- No Salesforce platform experience or certifications (Apex, Agentforce, Data 360): nice-to-have.
- No Snowflake, Databricks or BigQuery experience (nice-to-have; also named in the pipeline duty).
- No LlamaIndex; LangChain only via LangGraph.
- Years: about 3 years full time (plus internship), meets the mid-level 3+ floor but not the 6-10 for
  Senior.
- Travel ~25% and Toronto location: not gaps (willing to relocate per profile.md).

## Please sanity-check
- Summary "3 years of consulting experience deploying production AI agents for enterprise clients":
  synthesis of Accenture SWE + AI Engineer roles; the SWE years were microservices, not agents.
- LLM-as-a-judge bullet merges in "with Langfuse tracing of prompts and outputs" from the separate
  call-summary observability bullet (same application).
- "Partnered with enterprise client stakeholders" adds "client" (source: engineering consulting client,
  "enterprise stakeholders").

## Questions for Aly
- Posting says "Valid through: September 27, 2026" (fetched 2026-10-04 from Built In); it may be
  closed on Salesforce careers. Resume built anyway; confirm it is still open before applying.
