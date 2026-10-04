# Changelog: OpenTable, AI Applied Engineer, Business Solutions

Resume: `Aly_Mohamed_Hussein_Resume_OpenTable.tex` / `.pdf` (source: `mega-resume-v1.5.tex`)

## Emphasis
- Summary mirrors the posting: LLM applications, RAG pipelines, agentic workflows in Python, "from business
  discovery through deployment" (the role's end-to-end ownership ask).
- Accenture AI Engineer (6 bullets): stakeholder-driven billing automation (ambiguous requirements to success
  criteria, router/subagent agentic system, production deployment), Langfuse eval benchmark vs. the manual process
  and LLM-as-a-judge + tracing (posting's "evaluation frameworks and monitoring"), RAG fraud agent, Llama call-summary
  service (measurable impact: 15 min/call), Gemini natural-language dashboard chatbot (AI for business users).
- Software Engineer: pipeline automation (33% fewer failures) and Step Functions orchestration (closest to Airflow).
- Projects chosen for business-facing applied AI: Clinic Ops (customer discovery, 4 production LLM workflows,
  hallucination/prompt-injection quality controls), Cold-Chain (embedded with a non-technical owner, automated a
  manual operation), Safi (OpenAI/Anthropic/Gemini SDKs, evals), Leagueware (1 bullet).
- Skills: 5 lines; LLMs & Agents lists OpenAI/Anthropic/Gemini APIs, RAG (pgvector as the vector store), evals.

## Close-call cuts and overrides
- Research section dropped (both papers) for space and fit: the role is business-facing applied AI, not research.
- claude-kit cut; Safi trimmed to one bullet (the 77% to 96% judge story cut).
- Accenture cuts: monitoring/alerting (Splunk, New Relic, CloudWatch) bullet and the Gemini TTS PoC.
- DynamoDB dropped from skills to keep the line from wrapping. No age-rule override.

## Gaps vs. posting
- **5+ years required:** about 3.5 years full-time (Sept 2023 onward) plus the Ericsson internship.
- **Snowflake and Airflow:** not in the mega resume (SQL/PostgreSQL and AWS Step Functions / Kinesis are the closest).
- **LangChain and LlamaIndex:** not in the mega resume (LangGraph is). Vector DB experience is pgvector only.
- Level listed as Senior; salary CAD 110-123k. Location (Toronto hybrid, 2 days/week) is not a gap (willing to relocate).

## Accuracy check requests
- Billing bullet: "automate billing checks" condenses "automate the previously manual billing verification steps".
- LLM-as-a-judge bullet folds in Langfuse tracing; both are on the call-summarization service in the source.
- Call-summary bullet: "live agent recommendations" = "real-time recommendations to customer support associates".
- SWE bullet 2: "with CDK" condenses "CloudFormation and AWS CDK"; Step Functions was a proof of concept ("prototyped").

## Build
- fill: 0.968, skills_lines: 5, pages: 1, no errors (only 0.56pt overfull warnings, not visible)

## Questions for Aly
- none
