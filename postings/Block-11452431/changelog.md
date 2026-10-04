# Changelog: Block, AI Evaluation Infrastructure Engineer

Resume: `Aly_Mohamed_Hussein_Resume_Block.tex` / `.pdf` (source: `mega-resume-v1.5.tex`)

## Emphasis
- The role is evaluation infrastructure, so the summary and the top Accenture bullets lead with eval work: the
  LLM-as-a-judge summary grader with its feedback loop (maps to "grader infrastructure" and "the loop that keeps
  offline and online converging"), and the Langfuse framework benchmarking the agentic billing system against the
  manual process.
- Kept the call-summary service (real-time Kinesis/Flink pipeline, Langfuse tracing) for "data pipelines / systems
  that process production logs", and the fraud agent for the measured 96% on 500 transactions.
- Safi gets 3 bullets: a scorer reporting cost, quality and harm separately, a log-ingesting audit tool, and the
  LLM judge agreement lift from 77% to 96% that still caught the real regression. This is the closest match to
  "judge calibration" and "distinguish real improvements from noise".
- Clinic Ops kept for production LLM workflows plus the real-API smoke harness and CI gating (posting: "eval
  results gate CI").
- Research: kept the medical LLM accuracy study (an LLM evaluation framework across languages).
- Skills: 5 lines, with a new "LLM Evaluation & Agents" category (LLM-as-a-judge, eval harness design, Langfuse).

## Close-call cuts
- **Leagueware cut** (the prompt keeps it by default): no room, and it has nothing to do with evaluation.
- claude-kit cut for space (it had the "evaluation criteria agreed before implementation" and CI merge-gate angle).
  Swap it in for Clinic Ops if you prefer.
- Privacy-preserving NLP research cut. Its benchmarking of three approaches fits too, but the page was full.
- Cold-Chain Dispatch cut (no LLM or eval content). Gemini dashboard chatbot cut too.
- No age-rule override.

## Gaps vs. posting
- **Statistics:** the posting stresses confidence intervals, variance, power and multiple comparisons. Nothing in
  the mega resume shows this explicitly (no confidence intervals, significance testing or A/B testing). Be ready
  to talk about it from the M.Sc.
- No online evals, A/B or side-by-side serving, or implicit feedback signals from real users.
- No human-annotation or judge-to-human agreement tooling. Safi's judge agreement is judge vs. reference, not
  judge vs. human raters.
- No leaderboards or eval reporting dashboards, and no distributed batch execution engine at scale.
- The posting gives US pay zones and Built In labels it entry level, but it lists Toronto/Kitchener and remote in
  Canada. The posting note says Block's Greenhouse board lists this title only for the Bay Area, so check the
  application route.

## Accuracy check requests
- Summary says "LLM-as-a-judge graders": "graders" is the posting's word for your LLM-as-a-judge framework.
- Billing bullet merges the agentic system, production ownership, and the Langfuse eval framework bullets.
- Call-summary bullet merges the Llama FastAPI bullet with the Langfuse observability bullet.
- SWE bullet merges the 33% Jenkins bullet with the roughly 15-minutes-per-run bullet.
- Safi "built solo": the mega resume says "wrote essentially all of it solo".

## Build
- fill: 0.961, skills_lines: 5, pages: 1, no errors (only 0.56pt overfull warnings, not visible)

## Questions for Aly
- none
