# Changelog: Artefact, Senior AI & Agentic Engineer (8731948002)

Verification: 1 page, fill 0.963, skills 5 lines (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected. Posting is Montreal (hybrid), so eligible.
Rebuilt: the folder had a PDF from an earlier run but no .tex or changelog.

## Emphasized
- Full stack end to end: summary leads with "full-stack AI engineer"; React/TypeScript front end on the
  billing agent, Next.js/TypeScript client systems, FastAPI services.
- Agentic behavior and RAG: router agent orchestrating parallel subagents, LangGraph plan-execute fraud
  agent with RAG, MCP server on Clinic Ops (posting names MCP twice).
- Evaluation and reliability (their "not just the happy path"): Langfuse eval framework vs the manual
  process, LLM-as-a-judge on summaries with Langfuse tracing, test suites and CI gates on the projects.
- Platform depth: Anthropic (API, MCP, Claude Code, Claude Certified Architect listed first since the
  posting names Claude certification), plus Gemini on Vertex AI and Azure AI Foundry.
- AI-native work with judgment about verification: Cold-Chain agentic pipeline treating agent output as
  untrusted, and claude-kit (Claude Code plugin).
- Client-facing: stakeholder-requirements bullet, "sole engineer for a paying client" on both projects.
- Data pipelines: Kinesis/Flink real-time transcript pipeline.
- Research section dropped (both MILA papers) to fit three projects; Education compressed to one line
  per degree. M.Sc./MILA stays in summary and education.

## Close-call cuts
- **Leagueware cut** for space (named exception; flagged). Projects are Clinic Ops, Cold-Chain, claude-kit.
- Safi cut (LLM cost layer; posting mentions monitoring cost, but the three kept projects fit better).
- Accenture: TTS Gemini PoC, monitoring/alerting bullet. SWE: CloudFormation/CDK IaC bullet (cut on the
  last fit pass; IaC still shown via Bicep on Clinic Ops), DynamoDB, Step Functions. Cold-Chain: RLS
  cutover, DR backup. Clinic Ops: hallucination/injection bullet, prompt caching bullet.
- No age-rule overrides.

## Gaps vs the posting
- Vector search / embeddings: only "RAG" (fraud agent) and pgvector in the mega skills list; no bullet on
  ingestion, chunking, embeddings or hybrid search.
- No named agent SDK beyond LangGraph (no Google ADK, Claude Agent SDK, OpenAI Agents SDK); no Terraform
  (IaC is CloudFormation, CDK, Bicep); no LangSmith/promptfoo (Langfuse yes).
- No warehouse/lakehouse experience; data pipeline evidence is the Kinesis/Flink stream.
- No explicit mentoring, pre-sales or demo-building lines in the mega resume.
- Years: about 3 years full time plus an internship, at the bottom of the 3-5 range.

## Please sanity-check
- Summary "shipping agentic systems, RAG, and LLM evaluations to production on Azure, GCP, and AWS" is a
  synthesis; the fraud RAG agent is not explicitly described as production in the mega resume.
- Accenture bullet 4 merges three source bullets on the same summarization app (Llama FastAPI + Kinesis/
  Flink, Langfuse observability, LLM-as-a-judge eval).
- SWE bullet merges the 33% Jenkins bullet with Fargate, Lambda and REST API bullets.
- Cold-Chain bullet 2 shortens "check-then-insert race" to "a race".

## Questions for Aly
- none
