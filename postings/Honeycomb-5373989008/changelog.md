# Changelog: Honeycomb.io, Senior Software Engineer II - Agentic Intelligence (Remote - Canada)

Verification: 1 page, fill 0.965, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected.

Source of facts: `mega-resume-v1.5.tex`. Filename company: `Honeycomb` (from Honeycomb.io).

## Emphasized
- Shipped production LLM systems with end-to-end ownership (their top two asks): summary; Accenture
  billing agent (router + parallel subagents, owned production deployment); Clinic Ops (four
  production LLM workflows, live with a paying client, sole engineer).
- MCP server (they ship Canvas, an MCP server and Canvas Skills): Clinic Ops MCP server and tools;
  claude-kit (Claude Code commands, hooks, skills) as the "current agent architecture" signal.
- Evals and agent quality standards: Langfuse eval framework vs the manual process, LLM-as-a-judge
  degradation detection, Safi's eval-honesty bullet (judge agreement 77% to 96%).
- Observability background (preferred): new "Evals & Observability" skills line; Langfuse tracing;
  Splunk / New Relic / CloudWatch monitoring bullet; Safi ingesting LLM logs (LiteLLM, Helicone,
  Portkey); Ericsson log-analysis tools.
- Agents reasoning over structured data: fraud agent with RAG over customer and transaction history;
  Gemini chatbot generating dashboard visualizations from natural-language queries; real-time
  Kinesis/Flink streaming pipeline.

## Close-call cuts
- Cold-Chain Dispatch cut (no LLM component; space). Leagueware kept per its named exception.
- Research section dropped (both papers) for space; the posting asks for shipped production systems,
  not research.
- Clinic Ops: provider-failure taxonomy / smoke harness, PDPL Azure deployment, 584-test suite.
  Safi: workload-aware planner bullet. claude-kit: detailed constraint list. Accenture: Gemini TTS
  PoC, React operator frontend detail. SWE: all but the 33% bullet.

## Gaps vs the posting
- "Senior Software Engineer II" seniority: about 3 years full time, about 2 in a titled AI role.
- High-cardinality / fast columnar data stores enabling agent reasoning: no direct evidence beyond
  PostgreSQL, DynamoDB and the Kinesis/Flink streaming pipeline.
- Observability/developer-tools background: adjacent only (Langfuse tracing, production monitoring,
  log-analysis tools, LLM-log ingestion in Safi, claude-kit as dev tooling); never worked at an
  observability vendor.
- Work authorization in BC/ON/QC is required: Aly is in Montreal (Quebec), so this should be met.

## Please sanity-check
- Accenture bullet 2 merges the stakeholder/success-criteria/production-deployment bullet with the
  Langfuse evaluation bullet ("benchmarking the agents against the manual process").
- Accenture bullet 5 merges the LLM-as-a-judge bullet with the Langfuse observability bullet.
- Summary "shipping production LLM agents end to end, from prototype to evals, observability, and
  deployment" is a synthesis of the Accenture and project bullets.

## Questions for Aly
- none
