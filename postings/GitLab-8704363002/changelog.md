# Changelog: GitLab Backend Engineer (Python), AI Engineering: Agent Foundations (8704363002)

- **Emphasis:** this role is Python backend work on the Duo Agent Platform: LangGraph flows, APIs, async/background processing, pytest plus agent evals, performance bottlenecks, and Tier 2 on-call/observability. Compared with the Duo Chat resume (GitLab-8698314002), this version moves toward backend engineering. The summary now reads "Python backends, APIs, and LangGraph agents with evals and observability". The Accenture SE role gets 2 bullets: sync/async microservices (Lambda on SQS events, Fargate REST APIs, 33% fewer failing pipelines and about 15 min faster runs) and the DynamoDB index fix, framed as a performance bottleneck. Splunk/New Relic/CloudWatch monitoring and alerting is folded into the evals bullet for the on-call/observability ask. The Clinic Ops caching bullet (removing a per-page-view model call) adds a second performance signal. Skills add async microservices, Lambda/SQS and CloudWatch.
- **Close-call cuts:** the Clinic Ops MCP-server bullet, claude-kit's second bullet (agent constraints, 64 tests), Cold-Chain Dispatch (TypeScript, less agent/Python), Research, the Gemini/Vertex chatbot, and the SE Step Functions and CloudFormation/CDK bullets. Leagueware is kept at 1 bullet. No age-rule override.
- **Gaps (stated plainly):** no Ruby on Rails, Vue only via Leagueware, no GraphQL or gRPC (REST only), no LangChain (LangGraph only). No documented on-call rotation (production monitoring/alerting is the closest). No GitLab codebase experience. "Intermediate" level fits about 3 years of full-time experience.
- **Sanity-check:** (1) The DynamoDB bullet calls the full-table scans a "performance bottleneck". The mega resume says "improved query efficiency and reduced cost" by replacing scans, which is a reframe. (2) The evals bullet now also carries the Splunk/New Relic/CloudWatch monitoring item. The mega resume lists that item for production workloads in general, not only the summarization service. (3) The SE first bullet merges the CI/CD microservices, sync/async run-time, Fargate REST and Lambda/SQS items. (4) The Clinic Ops second bullet merges the caching, prompt-injection mitigation and 584-test suite items.

## Questions for Aly
None.

- fill: 0.965
- skills_lines: 5
