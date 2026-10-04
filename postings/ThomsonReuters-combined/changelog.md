# Changelog: Thomson Reuters, combined resume for LinkedIn outreach

Covers both roles: AI Engineer, Product Analytics (JREQ202780) and Software Engineer - AI, CoCounsel
Forward Deployed Engineering (9090356). Not an application; each role keeps its own tailored resume.

Verification: 1 page, fill 0.967, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, no collisions, dates and
rules aligned).

Source of facts: `mega-resume-v1.5.tex`. Every bullet is reused from one of the two per-posting
resumes (both already truth-checked against it) and re-checked against the mega resume.

## Emphasized
- What both roles share: LLM agents, RAG, tool-calling/MCP, evaluation of LLM outputs (hallucination,
  accuracy), observability, Python, and turning ambiguous business needs into production systems. The
  summary leads with these and adds the FDE angle ("client work in regulated domains, from discovery
  to production").
- Accenture AI Engineer (7 bullets): stakeholder requirements, router/subagent billing agent, Langfuse
  benchmark, LangGraph RAG fraud agent (96%), Llama call summaries (15 min/call), LLM-as-a-judge loop,
  and the Gemini natural-language dashboard chatbot (for Product Analytics).
- Clinic Ops (4 bullets): customer discovery (FDE), production LLM workflows, MCP server plus
  hallucination/prompt-injection guards (both), data residency and security (CoCounsel's "secure,
  data privacy").
- Safi (LLM cost and eval honesty) and the medical LLM accuracy research (evaluating LLM outputs for
  accuracy in a high-stakes domain, the closest analogue to legal accuracy).

## How it differs from each per-posting resume
- vs Product Analytics (JREQ202780): adds the client-discovery framing in the summary, the Clinic Ops
  discovery and data-residency bullets, and the medical LLM accuracy research; drops claude-kit, the
  Langfuse observability bullet, the DynamoDB index bullet, the Ericsson refactor bullet, and the
  Data & ML skills line (Pandas, NumPy, PyTorch, Kinesis). Stakeholder and Langfuse-benchmark bullets
  are split back into two, as in the FDE version.
- vs CoCounsel FDE (9090356): adds the Gemini dashboard chatbot, the Clinic Ops MCP server, Safi, and
  SQL/pytest in skills (Spring Boot dropped from skills); drops the privacy-preserving NLP research.
  The SWE bullet now reads "for early error detection" instead of the merged Fargate/Lambda wording.

## Close-call cuts
- claude-kit ("personal investment in AI" for Product Analytics) and the privacy-preserving NLP
  benchmark ("data privacy" for FDE), both for space.
- Leagueware cut for space (flagging per the prompt). Cold-Chain Dispatch cut (no AI part).

## Gaps vs the postings (unchanged from the per-posting changelogs)
- No legal-domain experience (CoCounsel, Westlaw, Practical Law) and no tax/audit/accounting or
  product-analytics domain experience.
- No Snowflake/Databricks, A/B testing or statistical inference work.
- Vector databases: only pgvector (mega skills list); no bullet names the store.

## Please sanity-check
- Summary: "client work in regulated domains (banking, healthcare)" synthesizes the U.S. bank work
  and the Clinic Ops client.
- Clinic Ops: "roughly 20 minutes saved per visit" shortens "per patient visit on report writing and
  administrative work".

## Questions for Aly
- none
