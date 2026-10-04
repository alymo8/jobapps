# Changelog: Unit8, Senior Forward Deployed Engineer (Hybrid, Canada) (6E5DB3FE0F)

Verification: 1 page, fill 0.964, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected. Posting is Montreal (hybrid), so eligible.

Source of facts: `mega_resume.tex` does not exist in the repo; used `mega-resume-v1.5.tex`.

## Emphasized
- Data pipelines and processing (the role's core, "developing, deploying, and troubleshooting complex data
  pipelines"): summary leads with "AI and data engineer ... real-time data pipelines"; Kinesis/Flink
  transcript pipeline bullet; Data & ML skills line led by Kinesis and Flink; DynamoDB index bullet.
- Client-facing / technical advisory: stakeholder-requirements bullet first under Accenture, "sole engineer
  for a paying client" on both projects, embedding with a non-technical owner, customer discovery.
- Data quality and troubleshooting: LLM-as-a-judge degradation detection, monitoring/alerting bullet,
  Cold-Chain data migration and the silently failing backup hardened with row-count/truncation checks.
- GenAI (their preferred LLM/GenAI background): router/subagent billing agent, LangGraph RAG fraud agent,
  four production LLM workflows on Clinic Ops.
- Strong Python: Python first in skills and in the summary.

## Close-call cuts
- **Research section dropped** (privacy-preserving NLP synthetic-data pipeline was drafted in, matching the
  Data Science domain, but the page overflowed to 2 pages); M.Sc./MILA stays in summary and education.
- **claude-kit and Leagueware cut** (Leagueware is a named exception; flagged): client systems fit a
  forward-deployed role better. Safi cut.
- Accenture: Gemini dashboard chatbot, Gemini TTS PoC, React front end. Cold-Chain: agentic pipeline and
  116-test bullets. Clinic Ops: MCP server, hallucination/injection, caching, 584-test bullets.
- No age-rule overrides.

## Gaps vs the posting
- **Years:** requires 5+ years in software/data engineering; Aly has about 3 years full time (plus internship).
- **PySpark / Spark:** not in the mega resume. Python is strong; distributed processing evidence is Flink.
- **Palantir Foundry:** none (preferred, and the role emphasizes it).
- **Pre-sales:** no explicit pre-sales lines; technical advisory is shown via stakeholder requirements work
  and customer discovery only.
- No warehouse/lakehouse or batch ETL work in the mega resume.

## Please sanity-check
- Accenture bullet 1 says "an engineering consulting client's stakeholders"; the source says "enterprise
  stakeholders" for the billing system built for an engineering consulting client.
- Accenture bullet 2 merges the billing-system build bullet with the Langfuse evaluation bullet.
- SWE bullet merges the 33% Jenkins bullet with the Fargate and Lambda/SQS bullets.
- Cold-Chain bullet 2 says "real data migration into separate prod and dev Postgres"; the source lists
  "separate prod and dev Postgres, real data migration" as separate items.

## Questions for Aly
- none (the 5-year requirement and PySpark/Foundry gaps are noted above; posting kept as-is)
