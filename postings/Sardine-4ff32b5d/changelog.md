# Changelog: Sardine, Forward Deployed AI Engineer

Resume: `Aly_Mohamed_Hussein_Resume_Sardine.tex` / `.pdf` (source: `mega-resume-v1.5.tex`)

## Emphasis
- Led with the forward-deployed shape of the role: embedding with clients, turning ambiguous operational
  problems into concrete requirements, and owning delivery to production. The summary names the fraud agent,
  since Sardine is a fincrime company.
- Accenture AI Engineer (5 bullets): the fraud detection agent for a U.S. bank comes first (a direct domain hit),
  then the billing agentic system written as a client engagement (stakeholders, ambiguous requirements turned into
  success criteria, production ownership) with its Langfuse eval benchmark. The call-summary service and the
  LLM-as-a-judge degradation framework cover "rigorous evaluation frameworks... accuracy, safety, reliability".
- Projects chosen for client-facing, end-to-end ownership: Clinic Ops (customer discovery, live deployment,
  hallucination and prompt-injection guardrails), Cold-Chain (embedded with a non-technical owner, solo production
  cutover), Safi (evals as the honesty mechanism), and Leagueware (kept by default, 1 bullet).
- Skills: 5 lines. SQL placed second in Programming Languages, plus a Data & Tools line (PostgreSQL, Pandas,
  NumPy, PyTorch, Kinesis) for the data science angle.

## Close-call cuts
- **Research section dropped entirely** (both papers). The medical-LLM evaluation research fit "evaluation
  frameworks", but there was no room once four projects were in, and the client-facing projects fit an FDE role
  better. Restore it in place of Safi or Leagueware if you prefer.
- claude-kit cut: less relevant to a client-facing fraud role than the three paying-client or eval projects.
- Accenture: Gemini dashboard chatbot, Langfuse observability, monitoring/autoscaling, and Gemini TTS POC cut.
- Clinic Ops MCP server, Azure IaC, and caching bullets cut; Cold-Chain testing and backup bullets cut.
- No age-rule override.

## Gaps vs. posting
- Posting asks for 5+ years in Data Science or Applied AI. You have about 3 years full-time (since Sept 2023),
  of which about 1.75 years are in the AI Engineer role, plus the M.Sc.
- No model fine-tuning or training of custom models in the mega resume. Your agent work is prompt/orchestration,
  RAG, and evaluation.
- No causal-impact measurement or experiment design (A/B testing) experience on record. The closest is the
  Langfuse benchmark against the manual process.
- SQL is listed but no bullet shows complex SQL data manipulation; it is backed only by Postgres work in projects.
- Fincrime domain experience is limited to the one fraud detection agent; no AML or compliance work.

## Accuracy check requests
- Summary: "embedding with clients to turn ambiguous workflows into production AI agents". The production agent is
  the billing system; the fraud agent is not described as production in the mega resume, and "embedded" is the
  mega resume's wording only for Cold-Chain.
- Billing bullet merges the system bullet with the stakeholder/production-ownership bullet.
- SWE bullet merges the 33% failing-pipelines bullet with the ~15 min per run bullet.
- Clinic Ops workflows bullet merges the four-workflows bullet with the guardrails bullet.

## Build
- fill: 0.968, skills_lines: 5, pages: 1, no errors (only sub-1pt overfull warnings, not visible)

## Questions for Aly
- none
