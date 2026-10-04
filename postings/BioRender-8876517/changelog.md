# Changelog: BioRender, Applied AI Engineer, Internal Products (Remote, Canada)

Verification: 1 page, fill 0.965, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no collisions, no orphan words).

Source of facts: `mega-resume-v1.5.tex`. Format: `latex_resume.tex` preamble and header verbatim.

## Emphasized
- Agents, tools and workflows for internal teams: Accenture billing agentic system (router +
  parallel subagents, React/TypeScript operator frontend), internal Gemini/Vertex AI chatbot,
  stakeholder bullet (requirements into success criteria, owned deployment).
- Multi-provider LLM APIs (OpenAI, Anthropic, Gemini): Safi provider abstraction across all three;
  Clinic Ops on Anthropic structured outputs + MCP server; Gemini at Accenture. Skills line names
  all three APIs.
- AI model evaluation: Langfuse eval framework, LLM-as-a-judge summary evals, Safi judge
  agreement 77% to 96%.
- Development velocity through AI tooling: claude-kit placed first in Projects; CI/CD pipeline
  microservices (33% fewer failing pipelines) and Ericsson developer log tools (50% faster for 30+
  devs).
- Self-directed, end to end: summary line on two revenue-generating systems shipped solo;
  Clinic Ops "sole engineer for a paying client".
- Python and JavaScript/Node: Skills lead with Python, JavaScript, TypeScript; Node.js under
  Frameworks; Leagueware (JavaScript) kept.

## Close-call cuts
- Cold-Chain Dispatch cut for space (strong self-directed/end-to-end signal, but Safi wins on
  multi-provider APIs and evals, claude-kit on AI dev tooling).
- Research section dropped entirely (medical LLM accuracy and privacy NLP); the privacy project's
  "prompt engineering" was the only explicit prompt-engineering evidence.
- Accenture: fraud detection agent (LangGraph, RAG, 96%), Gemini TTS PoC, monitoring/alerting.
  SWE: Fargate/Lambda/CloudFormation bullet, DynamoDB indexes, Step Functions.
- Clinic Ops: prompt-injection/hallucination mitigation bullet.
- No age-rule override.

## Gaps vs the posting
- 4+ years of software engineering: about 3 years full time (Accenture SWE Sept 2023 onward) plus the
  Ericsson internship and side projects.
- "Prompt engineering" is not named on the page (only evidenced in the cut research project); it is
  implied by the LLM workflows and judge work.
- "SaaS tool experience" / integrating with business tools: no named SaaS integrations (e.g.
  Slack, Notion, Salesforce) in the mega resume beyond Langfuse, Vercel, Supabase and WhatsApp links
  in Cold-Chain (cut).
- Remote/distributed team experience: not explicit in the mega resume.

## Please sanity-check
- Summary "3 years shipping production AI agents and LLM workflows" compresses the mega summary
  "3 years of experience building production AI agents and LLM-powered systems".
- Accenture LLM-as-a-judge bullet merges in the Langfuse observability (tracing) bullet.
- SWE bullet merges the 33% failing-pipelines bullet with the "roughly 15 minutes per run" bullet
  (the latter came from the sync/async microservices).
- Safi bullet 1 merges the planner/provider-abstraction bullet with the 48-request live trace
  (61.7% savings) from the savings-audit bullet.

## Questions for Aly
- none
