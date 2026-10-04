# Changelog: Thomson Reuters, AI Engineer, Product Analytics (JREQ202780)

Verification: 1 page, fill 0.965, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, no collisions).

Source of facts: `mega-resume-v1.5.tex` (no `mega_resume.tex` in the repo).

Eligibility: Toronto, Ontario, hybrid; Ontario range CA$82.1K-132.1K. Aly is in Montreal; the
posting gives no remote option, so a Toronto hybrid commute or relocation is implied.

## Emphasized
- The posting wants agents for product analytics: LLM APIs, tool-calling/MCP integrations,
  prototypes hardened with guardrails, telemetry and logging, its own evaluation, and natural language
  interfaces. The summary leads with agents, tool-calling/MCP, evals and observability.
- Accenture AI Engineer (7 bullets): the Gemini natural-language dashboard chatbot goes first (closest
  to "natural language interfaces" over analytics), then the router/subagent billing agent, the
  stakeholder requirements plus Langfuse benchmark, the LangGraph RAG fraud agent (96%), the streaming
  Llama summarizer (15 min/call), the LLM-as-a-judge feedback loop ("feedback loops", "quality drift"),
  and Langfuse observability ("telemetry").
- Accenture SWE: the 33% pipeline bullet plus the DynamoDB index bullet (data access). Ericsson: the
  log-analysis tool and the microservice refactor ("refactoring into production-ready components").
- Projects: Clinic Ops (Anthropic API, MCP server, guardrails against hallucination and prompt
  injection), Safi (LLM cost and eval honesty, matching "cost and safety considerations"), claude-kit
  ("personal investment in AI, work you can point to", evaluation criteria before building).

## Close-call cuts
- **Research section cut** (both entries) to fit the projects; the privacy-preserving benchmark would
  speak to the "data science background" preference.
- **Leagueware cut** for space (the prompt says to flag this). Cold-Chain Dispatch cut (no AI part).
- Accenture: the monitoring/alerting bullet (Splunk, New Relic, CloudWatch), the Gemini conversational
  PoC, and the Clinic Ops failure taxonomy/caching and Azure data-residency bullets.

## Gaps vs the posting
- No Snowflake/Databricks or modern data-stack experience.
- No explicit experiment design, A/B testing or statistical inference work; closest is the M.Sc. and
  the evaluation frameworks.
- "Strong SQL" is listed in skills but no bullet shows heavy SQL work (Postgres in the projects,
  DynamoDB at Accenture).
- Vector databases: only pgvector (mega skills list); the fraud agent's RAG bullet doesn't name a store.
- No product analytics or tax/audit/accounting domain experience.

## Please sanity-check
- Accenture: "Translated ambiguous billing requirements into measurable success criteria ... and
  created a Langfuse evaluation framework" merges two source bullets.
- Clinic Ops: "a surgeon reports roughly 20 minutes saved per visit" shortens "a practicing Cairo
  chest surgeon ... per patient visit on report writing and administrative work".
- Safi: "eval-guarded layer" paraphrases "quality guaranteed by evals".

## Questions for Aly
- none (Toronto hybrid location noted above; decide whether to apply from Montreal).
