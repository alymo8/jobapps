# Changelog: Thomson Reuters, Software Engineer - AI (CoCounsel Forward Deployed Engineering)

Verification: 1 page, fill 0.964, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected.

Source of facts: `mega-resume-v1.5.tex` (no `mega_resume.tex` in the repo).

Eligibility: Toronto hybrid (19 Duncan St), Ontario range CA$80K-100K. Aly is in Montreal; the
posting gives no remote option, so a Toronto hybrid commute or relocation is implied.

## Emphasized
- The posting's core asks: RAG pipelines, agentic workflows, LLM evaluation (hallucination, accuracy),
  Python, and regulated domains. The summary leads with all of these and with "technical discovery to
  production deployment" (their client-facing FDE wording).
- Accenture AI Engineer (6 bullets): stakeholder requirement-gathering, router agent with parallel
  subagents, Langfuse benchmark against the manual process, LangGraph RAG fraud agent (96%),
  Llama call-summary service (15 min/call), LLM-as-a-judge hallucination/completeness evals.
- Clinic Ops (4 bullets): customer discovery, production LLM workflows on Anthropic structured outputs,
  hallucination and prompt-injection mitigation with human-in-the-loop, data-residency deployment
  (maps to "accurate, secure", "responsible AI, data privacy, enterprise security").
- Research section kept (merged under "Projects & Research"): medical LLM accuracy evaluation and the
  privacy-preserving NLP benchmark map to "evaluate LLM outputs for accuracy" and "data privacy".

## Close-call cuts
- **Cold-Chain Dispatch cut** to fit the page: strong client-facing signal, but no AI component; the
  Clinic Ops discovery bullet covers the client side.
- **claude-kit cut** (could support "document solutions, reusable components, best practices").
- **Leagueware cut** for space (the prompt says to flag this).
- Safi (LLM cost optimization, evals) cut; Gemini dashboard chatbot, Langfuse observability, and
  monitoring bullets cut. Each research entry has 1 bullet instead of 2.

## Gaps vs the posting
- No legal-domain experience (contract review, litigation, discovery, Westlaw/Practical Law/CoCounsel).
  The closest are banking and healthcare, both regulated.
- No hands-on vector database beyond pgvector, which appears only in the mega resume's skills list
  (the fraud agent's RAG bullet doesn't name the store).
- Years: about 3 years full time, inside their 2-4 band.

## Please sanity-check
- Accenture SWE: "deployed on AWS Fargate and Lambda behind REST APIs" merges two source bullets
  (Spring Boot on Fargate exposing REST APIs; Python Lambdas processing SQS events).
- Summary: "for clients in regulated domains (banking, healthcare)" is a synthesis of the U.S. bank
  work and the Clinic Ops client.

## Questions for Aly
- none (Toronto hybrid location noted above; decide whether to apply from Montreal).
