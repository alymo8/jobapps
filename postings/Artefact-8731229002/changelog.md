# Changelog: Artefact, Senior Forward Deployed Engineer (Gemini Enterprise) (8731229002)

Verification: 1 page, fill 0.965, skills 5 lines (no category wraps), no LaTeX errors; only sub-1pt
overfulls (same as the reference). PNG inspected. Posting is Montreal, so eligible. Rebuilt over an old PDF
(no .tex or changelog existed). Built from the sibling Artefact-8731948002 resume, re-tilted toward Google.

## Emphasized
- Google AI stack first: summary names GCP (Gemini, Vertex AI); Cloud skill lists GCP first; the two
  Gemini bullets (Vertex AI chatbot, Gemini 2.5 Pro conversational PoC with TTS) now lead the Accenture role.
- Forward-deployed / client-embedded: "embedded with" a business owner (Cold-Chain) and a paying client
  (Clinic Ops), stakeholder-requirements bullet at Accenture.
- Agents, multi-agent, RAG, MCP: router/subagent billing system, LangGraph plan-execute RAG fraud agent,
  MCP server on Clinic Ops.
- Evals and regression tests: Langfuse eval framework, LLM-as-a-judge, 584/116/64-test suites with CI.
- Deployment: containers (Fargate, Container Apps, Docker), serverless (Lambda), IaC restored
  (CloudFormation/CDK bullet, Bicep). Data pipeline: Kinesis/Flink transcript stream.
- Agentic coding with judgment (posting asks for it): Cold-Chain spec-driven pipeline, claude-kit.
- Research section dropped to fit three projects; Education one line per degree (MILA kept).

## Close-call cuts
- Leagueware cut for space (named exception; flagged). claude-kit trimmed to 1 bullet.
- Safi cut; Accenture monitoring/alerting bullet; SWE DynamoDB, Step Functions; Cold-Chain RLS cutover
  and DR backup; Clinic Ops hallucination/injection and caching bullets.
- No age-rule overrides.

## Gaps vs the posting
- No Agent Development Kit, Gemini Enterprise (Agent Designer, Agent Engine), Vertex AI Search or RAG Engine.
- GCP production depth is limited to the Gemini/Vertex AI chatbot and PoC; most production work is Azure/AWS.
- No Google Cloud certification (required within two months of hire); no Terraform (IaC is CloudFormation,
  CDK, Bicep); no BigQuery or Workspace integrations; no warehouse experience.
- RAG: no bullet on ingestion, chunking, embeddings, or hybrid search (only the fraud agent RAG; pgvector in
  mega skills list).
- Node.js appears in skills from the mega skills list but no kept bullet backs it.
- No mentoring or pre-sales lines in the mega resume. Years: about 3 full time, bottom of the 3-5 range.

## Please sanity-check
- Summary "taking client agents, RAG, and LLM evals to production" is a synthesis; the fraud RAG agent is
  not explicitly described as production.
- "Built a multi-agent system" for the billing agent (source: "agentic AI system" with router + parallel
  subagents).
- Accenture call-summary bullet merges three source bullets; SWE bullet 1 merges the 33% Jenkins bullet
  with Fargate, Lambda, and REST API bullets.

## Questions for Aly
- none

Final: fill 0.965, skills_lines 5.

## Cover letter truth check

Test run of /cover-letter (2026-10-04): cover_letter.md, 361 words, PDF 1 page (built for the
check; the form takes text or file). Not pasted into the form.

claim | source
--- | ---
Senior FDE (Gemini Enterprise), Montréal; "idea to production", end-to-end ownership, embedded with clients | posting.md
past three years of client AI work | answers.md "client-facing roles": "past three years as a consultant"
promoted and specialized as an applied AI engineer | mega resume (SWE Sep 2023 → AI Engineer Jan 2025); profile.md framing rule
every AI system delivered for an external client | answers.md "client-facing roles"
billing: broad question → measurable success criteria; router agent + parallel subagents; React/TypeScript operator frontend; owned production deployment | mega resume Accenture bullets 1 and 3; answers.md "client-facing roles"
fraud agent: LangGraph, RAG over customer and transaction history, 96% accuracy across 500 transactions | mega resume Accenture bullet 4
built in four weeks, approved as a production application | stories.md 10 Result (Aly, 2026-10-04)
Gemini on Vertex AI chatbot for dashboard visualizations; conversational PoC on Gemini 2.5 Pro | mega resume Accenture bullets 8 and 9
proposed and built LLM-as-a-judge; completeness, hallucination, readability | stories.md 1a; mega resume Accenture bullet 7
>90% agreement with human labels; one month to production | stories.md 1b and 1a Result (Aly, 2026-10-04)
clinic platform, sole engineer, paying client; four production LLM workflows on structured outputs; MCP server; 584-test suite gating CI | mega resume Clinic Ops bullets 3, 4, 8
agentic coding daily, spec-first workflow open-sourced as claude-kit | mega resume claude-kit + Clinic Ops bullet 8; answers.md "LLM project" (uses LLMs daily)
onboarded new engineers onto complex client projects | stories.md 9
at ease with clients; full stack | answers.md "client-facing roles"; mega resume (React/TS frontend + Python/FastAPI backends)

Steered around (gaps in this changelog): ADK, Agent Designer/Engine, Vertex AI Search, Terraform,
Google certification. None mentioned. Sanity-check: "past three years" counts the 2023-2025 SWE
period as client work (answers.md says so).
