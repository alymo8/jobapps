# Changelog: Scotiabank (Tangerine), Senior AI Engineer, req 274918

- **Emphasized:** the posting's core asks: LLM-powered and agentic apps (RAG, multi-step agents, structured outputs, prompt safety) and building MCP servers. The fraud detection agent comes first, since fraud detection is a preferred area. Contact-center AI comes next (call summarization plus the Gemini 2.5 Pro text-to-speech support-agent prototype), which maps to the "NLP and voice response / IVR / contact center intelligence" preference. Vertex AI appears through the Gemini chatbot, React through the billing frontend, and the "translate ambiguous problems" ask through the stakeholder bullet. In Projects, Clinic Ops leads because it covers the MCP server, Anthropic structured outputs, prompt-injection hardening, and the managed-identity/private-networking Azure deployment. Cold-Chain shows automated testing and row-level security.
- **Structure:** Summary, Skills, Experience, Education, Projects. **Research is dropped**: the role is applied engineering and the space went to agentic and production work. Education is compressed to the degrees, GPAs, and MILA. No age-rule override. The filename uses `Scotiabank`, matching the folder and the other Scotiabank posting, even though the posting is branded Tangerine (a Scotiabank subsidiary).
- **Close-call cuts:** **Leagueware was cut for space** (flagged per the prompt; the page overflowed by about 8 lines with it in). claude-kit and Safi were also cut. Other cuts: the Accenture monitoring bullet (Splunk/New Relic/CloudWatch), the JUnit bullet, the Ericsson Kubernetes deployment bullet, the Cold-Chain production-cutover/runbooks and backup bullets, and Arabic/Spanish from Languages.
- **Gaps vs the posting:**
  - **No production OAuth 2.0 / OpenID Connect / SAML experience is in the mega resume, and the posting says it is required.** The closest items are Azure Key Vault with managed identity, Postgres row-level security / multi-tenant isolation, and tokenized driver links in Cold-Chain.
  - Scikit-learn and Matplotlib appear only in pre-2022 cut projects. Classical ML (classification, clustering, credit risk, segmentation) has no recent backing.
  - No Angular.
  - No formal IVR platform. The voice work is the Gemini text-to-speech prototype.
  - "Mentoring peers through code reviews" has no direct source line.
- **Sanity-check these:**
  - The call-summary bullet now says "contact-center call summaries". The source says "customer support call summaries".
  - The "Partnered with enterprise stakeholders" bullet merges the stakeholder/requirements bullet with the Langfuse evaluation framework that benchmarks against the manual process. Both are about the billing system.
  - The LLM-as-a-judge bullet merges in the Langfuse tracing bullet. Both are about the call-summarization app.
  - The Gemini prototype is worded "fully automated Gemini 2.5 Pro support agent with a text-to-speech layer to converse with customers". The source says it was a proof of concept of the call summarization process.
  - The summary's "for major U.S. banks" covers the bank work. The Azure billing system was for an engineering consulting client.
- **Questions for Aly:** none (calls made above; the OAuth/OIDC/SAML gap is worth preparing for in a cover letter or interview).
- **Final build:** pages 1, fill 0.977, skills_lines 5, no errors. The only overfull boxes are the usual 0.56pt project-heading ones, which are invisible on the page.
