# Changelog: 11x, Forward Deployed Engineer [REMOTE - Canada]

Verification: 1 page, fill 0.964, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected.

Source of facts: `mega_resume.tex` does not exist in the repo; used `mega-resume-v1.5.tex` (the only
mega resume present).

Eligibility: posting says "remotely throughout the U.S. and Canada"; Canada base CA$150K-CA$180K.
Montreal is eligible.

## Emphasized
- Fullstack + agents: the summary leads with fullstack AI agent systems in TypeScript, React, Next.js and
  Python (their required stack), and both Next.js/TypeScript client systems are in Projects.
- Consulting / customer-facing (their stated bonus): Accenture stakeholder bullet first, "sole engineer
  for a paying client" on both projects, customer discovery and embedding with a non-technical owner
  (mirrors "UX and usability for non-technical users").
- Voice / conversational AI (the body calls the role "Voice Agent Engineer"): restored the Gemini 2.5 Pro
  text-to-speech conversational PoC and kept the real-time call-summary/recommendation bullet.
- Agent orchestration and evaluation: router agent with parallel subagents, Langfuse eval framework,
  MCP server, hallucination/prompt-injection mitigation.
- Debugging live systems: monitoring/alerting bullet, and the Cold-Chain silent-failing backup fix.
- Research section dropped; Education placed before Projects as in the reference.

## Close-call cuts
- **claude-kit cut** (usual shortlist) to make the page fit; it partly matched "contribute to internal
  best practices", but the client systems are stronger evidence for a deployment role.
- **Safi cut**; Research section (both MILA papers) cut, although the medical-LLM paper touches
  "prompting strategies".
- **Vodafone chatbot (Node.js, conversational AI) not restored**: considered an age-rule override for
  the conversational-AI angle, but it is a nice-to-have "interest" line and the Gemini TTS PoC covers it.
- Accenture: fraud-detection agent (LangGraph RAG, 96%), LLM-as-a-judge summary evals, Gemini dashboard
  chatbot, Langfuse observability. SWE: CDK/CloudFormation, DynamoDB, Step Functions. Cold-Chain:
  agentic pipeline, 116-test bullet. Clinic Ops: Azure PDPL deployment, caching, 584-test bullet.

## Gaps vs the posting
- Node.js appears only in Skills (no bullet behind it); no explicit Node.js backend work in the mega
  resume beyond Vodafone (cut by the age rule).
- No production voice system: the voice work is a proof of concept (Gemini 2.5 Pro + text-to-speech).
- No startup employment apart from Leagueware co-founding and the solo client work.
- Years: about 3 years full time, right at their 3+ floor.

## Please sanity-check
- Summary: "building fullstack AI agent systems (TypeScript, React, Next.js, Python) from client
  requirements to live deployment; shipped two paid systems solo" is a synthesis; "paid" stands for
  the mega resume's "revenue-generating".
- TTS bullet says "proof of concept of the support call"; the source says "of the call summarization
  process ... using Gemini 2.5 Pro as the support agent".
- Accenture bullet 2 says the system was built "on Azure AI Foundry, Azure ML, and Azure Containers",
  as in the source; the stakeholder bullet keeps "enterprise stakeholders".

## Questions for Aly
- none
