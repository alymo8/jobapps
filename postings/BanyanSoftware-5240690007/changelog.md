# Changelog: Banyan Software, Forward Deployed AI Engineer (Toronto, hybrid 3 days/week)

Verification: 1 page, fill 0.966, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected.

Source of facts: `mega-resume-v1.5.tex` (stands in for `mega_resume.tex`, per the batch instructions).

## Emphasized
- Embedding with business teams and turning manual workflows into AI tools (the role's core): the summary
  leads with it; Accenture stakeholder-to-success-criteria bullet first; billing automation framed as
  automating a manual business process; "embedded with a non-technical owner" and customer discovery on
  the two client projects.
- ROI / measuring impact: Langfuse benchmark against the manual process, 15 min/call saved, ~20 min/visit
  saved, 33% fewer failing pipelines, 50% faster support.
- LLMs, retrieval, agentic workflows: router + parallel subagents, LangGraph plan-execute fraud agent with
  RAG, four production Anthropic structured-output workflows.
- Claude Code (named twice in the posting): in summary and skills, and claude-kit (a Claude Code plugin)
  kept as a project.
- Engineering practice list (reviewed PRs, tests, secrets, IaC, CI/CD, environment separation): Cold-Chain
  prod/dev split, CI gates and leaked-key scan; Clinic Ops Bicep/azd IaC, Key Vault, 28 reviewed PRs and a
  584-test suite; AWS CDK/CloudFormation bullet restored for the SWE role ("bespoke applications on AWS").
- BI-adjacent: kept the Gemini natural-language dashboard chatbot.
- Research section dropped; Education placed before Projects as in the reference.

## Close-call cuts
- **Leagueware cut** (default-eligible): space forced it once claude-kit, which hits the Claude Code
  requirement directly, was in.
- Safi (LLM cost optimization, evals) cut; would support the "business case" angle but space ran out.
- Research (both MILA papers) cut; the medical-LLM evaluation paper touches "model evaluation".
- Cold-Chain "designed around how users actually work" bullet and agentic-pipeline / 116-test bullets;
  Clinic Ops MCP server, hallucination/prompt-injection mitigation and caching bullets; Accenture
  LLM-as-a-judge summary evals, Langfuse observability, Gemini TTS PoC, monitoring bullet.
- No age-rule override.

## Gaps vs the posting
- **n8n / automation-orchestration platforms**: nothing in the mega resume (closest: AWS Step Functions
  PoC, not listed). No explicit build-vs-buy decision on record.
- **Excel and BI tools (Looker, Power BI, Tableau)**: not in the mega resume. SQL is only in the skills
  list (Postgres work backs it); no dedicated data-modelling or analytics bullet.
- **Years**: posting asks 6 to 10 years total with 3+ in AI; Aly has about 3 years full time
  (plus internships), so it is below the floor on total experience.
- Staged rollout / rollback: not explicitly shown.
- Financial/commercial acumen, training teams and driving adoption: only indirectly (customer
  discovery, runbooks for the customer).

## Please sanity-check
- Summary: "embedding with business teams to turn manual workflows into production LLM, retrieval, and
  agentic tools ... built with Claude Code" is a synthesis of the Accenture stakeholder work, the
  Cold-Chain embedding, and claude-kit; "built with Claude Code" assumes Claude Code is your day-to-day
  agentic tool on these builds.
- Accenture billing bullet: "Automated a consulting client's manual billing verification" (source: "to
  automate the billing process of an engineering consulting client ... previously manual billing
  verification steps").
- SWE bullet says "deployed on AWS Fargate behind REST APIs" (Lambda dropped, since the Lambdas processed
  SQS events, not REST).

## Questions for Aly
- none (years-of-experience gap is below their 6-year floor; applied anyway as the batch asked)
