# Behavioral stories

Aly's STAR stories (Situation, Task, Action, Result), for behavioral free-text questions, cover
letters and outreach messages. `/apply` picks the story that fits a question from the index below.
Facts in Situation/Action/Result are Aly's own; anything under **Open** is an unconfirmed prep note
(a missing number, a likely follow-up question): never state it as fact, ask Aly if it is needed.

Typical questions these answer:

- Tell me about a time you faced a problem with multiple possible solutions. How did you decide what
  to do, and what was the outcome?
- Describe a time when you took a risk, made a mistake, or failed. What happened, and what did you
  learn from it?
- Share an example of when you took the lead on a project.
- What did you do to motivate a group or encourage collaboration on a team project?
- How have you used data to develop a strategy or make a decision?

## Index by leadership principle

| Principle | Stories |
|---|---|
| Customer Obsession | 10 Fraud detection POC: met POs and fraud agents to understand their process before building |
| Ownership | 1a LLM-as-a-judge: found the gap, proposed and owned it from scratch · 4 Production monitoring: took it on, not in my scope · 6a/6b Production failure: owned the mistake, rolled back, fixed the system · 8 QA bottleneck · 9 Onboarding |
| Invent and Simplify | 2a KDA Flink deployment fix: blue/green alternating strategy · 8 QA bottleneck: isolated test environment with mocked dependencies · 6c Automated testing tool: 3 hours to 10 minutes · 10 Fraud detection POC |
| Are Right, A Lot | 3 CI/CD sync vs async: analyzed each service, made and defended the calls · 1b LLM judge validation: validated the judge against human labels before trusting scores · 2b Defending the Flink strategy |
| Learn and Be Curious | 5 Multilingual medical LLM research: challenged my own hypothesis, found the translate-first fix · 6a Production failure: treated the incident as a systemic learning |
| Hire and Develop the Best | 9 Onboarding new grads: voluntary buddy for 3 joiners, delivering in 3 weeks |
| Insist on the Highest Standards | 1a LLM-as-a-judge: pushed for eval before shipping · 1b Validated the judge itself · 4 Production monitoring · 6c Automated testing tool: raised the testing bar across all contributing teams |
| Think Big | 10 Fraud detection POC: the POC is becoming a real product another team is building |
| Bias for Action | 2a KDA Flink fix: proposed and drove it without waiting · 8 QA bottleneck: designed and deployed 5 instances to unblock a team of 7 · 7 Masters + full-time job |
| Frugality | 8 QA bottleneck: mocked APIs and DB calls instead of real infrastructure · 6c Automated testing tool: removed 3 hours of manual work per sprint with a lightweight tool |
| Earn Trust | 6a/6b Production failure: immediately owned a mistake that was mine |
| Have Backbone; Disagree and Commit | 2b Flink deployment strategy: pushed back on by a senior engineer, came back with a simpler design and probability data |
| Deliver Results | 3 CI/CD microservices: 33% fewer failing pipelines, 10 min saved per run · 8 QA bottleneck: unblocked a team of 7 · 6c Automated testing tool: 3 hours to 10 minutes every sprint · 7 Masters + full-time job |
| Dive Deep | 1b LLM judge validation against human ground truth · 5 Multilingual research: why the 13 pp accuracy gap existed |

## 1a. LLM-as-a-judge: building the eval pipeline

LP: Insist on the highest standards · Ownership

**Situation**
- Banking client had AI-generated call summaries in production
- No quality measurement system existed; no one had scoped it
- Risk: summaries containing hallucinations reaching live agents
- How to evaluate updates to the LLM prompt or config? That was handled by another team

**Task**
- Identify the gap, propose it, and lead the workstream from scratch to production

**Action**
- Identified the gap myself; proposed and owned the workstream
- Built an eval pipeline comparing generated summaries against the original transcripts
- Scored on 3 dimensions: completeness, hallucination rate, readability
- Took it end to end: scoping, implementation, production deployment

**Result**
- Moved from "ship and hope" to a data-driven quality gate
- Gave the banking client measurable confidence in AI output accuracy
- The eval framework became reusable for future LLM workstreams
- About 1 month from idea to production (Aly, 2026-10-04)

**Open**
- Why LLM-as-a-judge over rule-based or human-only review?

## 1b. LLM-as-a-judge: validating with human labels and a feedback loop

LP: Dive deep · Are right, a lot

**Situation**
- The LLM-as-a-judge eval pipeline was live, but we had no proof the judge itself was accurate
- If the judge was miscalibrated, we were measuring quality with a broken ruler
- Needed to validate the judge before trusting its scores in production

**Task**
- Validate the judge's reliability against human judgment
- Close the loop so low quality scores triggered real action

**Action**
- Collected human-labeled examples as a ground-truth baseline
- Compared LLM judge scores against human labels systematically
- Identified where the judge agreed and disagreed with humans; calibrated accordingly
- Implemented a feedback loop: low scores automatically triggered alerts and retraining signals

**Result**
- Proved the judge was reliable, which gave the team confidence to act on its scores
- The feedback loop meant quality issues surfaced automatically, not manually
- Turned a static eval tool into a living quality system
- The judge agreed with human labels more than 90% of the time (Aly, 2026-10-04)

**Open**
- Did the feedback loop ever trigger a real retraining cycle?

## 2a. KDA Flink deployment fix

LP: Invent and simplify · Bias for action

**Situation**
- A real-time LLM app on KDA Flink required deleting the full CloudFormation stack before every prod
  deployment
- That left a window with zero running applications: a real reliability risk for a banking client

**Task**
- Design and implement a safer deployment strategy within the existing infrastructure constraints

**Action**
- Proposed a blue/green alternating strategy: two apps (primary + secondary)
- Delete and redeploy only one at a time; the other stays live
- Added flags to the CloudFormation YAML to control which app deploys, to keep it simple
- Documented and socialized the approach with the team

**Result**
- Eliminated the zero-application window entirely
- Adopted as the team's standard deployment practice

**Open**
- How many prod deployments per month?
- Tradeoffs (e.g. managing two app configs)?

## 2b. Have backbone: defending the Flink deployment strategy

LP: Have backbone; disagree and commit · Are right, a lot

**Situation**
- Same KDA Flink problem: full stack deletion before every prod deploy
- Proposed the alternating strategy; a senior engineer pushed back that it was too complex to manage

**Task**
- Defend the proposal or come back with something stronger

**Action**
- Did not drop it; came back with two things:
  - Simplified the implementation: CloudFormation flags made it a config change, not a process
    overhaul
  - Built a probabilistic case from real data: the likelihood of Jenkins being down during a
    deployment over a full year, showing the old process would statistically cause a
    zero-application window within the year
- Presented both to the senior engineer and the team

**Result**
- The senior engineer was convinced; the team adopted the new strategy
- Learned that pushback is an invitation to strengthen your argument, not abandon it

**Open**
- What probability did you calculate?
- "What would you have done if they still said no?"

## 3. CI/CD microservices: sync vs async

LP: Are right, a lot · Deliver results

**Situation**
- A major U.S. bank's Jenkins CI/CD pipeline had a high failure rate with no early detection
- Needed microservices integrated into the pipeline to catch errors early
- Had to decide synchronous or asynchronous architecture for each service

**Task**
- Lead the development of the microservice layer
- Make the right sync vs async call per service type

**Action**
- Analyzed each service by criticality: does a failure here block the pipeline?
- Decision rule: sync for critical-path services, async for non-critical ones
  - Sync: faster results where needed, clearer error propagation
  - Async: lower overall latency, parallel execution, non-blocking
- Built and deployed the services on AWS Fargate with Spring Boot
- Led development end to end: design, implementation, testing, deployment

**Result**
- Failing pipelines reduced by 33% across the bank
- Average pipeline run time cut by 10 minutes
- Early error detection stopped failures before they cascaded downstream

**Open**
- How many services in total?
- Did anyone push back on the sync/async decisions?
- What happened when a sync service went down, and how was it handled?

## 4. Production monitoring and dashboards

LP: Ownership · Insist on the highest standards

**Situation**
- Real-time LLM summarization app in production for a major bank
- No visibility into system health, latency, or the cost of GenAI calls
- Production issues could go undetected; no alerting existed

**Task**
- Set up full observability for the production workload
- Let the team catch issues proactively, before they reached the client

**Action**
- Built dashboards with AWS CloudWatch, Splunk and New Relic
- Tracked latency, error count, GenAI cost per request, uptime
- Set alerting thresholds so alerts fired on anomalies before client impact
- Added autoscaling triggers tied to CloudWatch metrics
- Took this on proactively; it was not part of my scoped tasks

**Result**
- Full visibility into prod from day one of go-live
- The team could respond to incidents before clients reported them
- GenAI cost tracking enabled optimization discussions with stakeholders
- The dashboard is used daily by ~10 engineers for alert checks, error rates and latency
- Alerts regularly caught real incidents and prevented many production issues (Aly, 2026-10-04)

**Open**
- Approximate GenAI cost reduction from optimizing on the data?
- Why three tools; what did CloudWatch, Splunk and New Relic each cover?

## 5. Multilingual medical LLM research

LP: Learn and be curious · Dive deep

**Situation**
- Researching LLM accuracy on medical data across languages at McGill/Mila
- Initial hypothesis: GPT-4o would perform consistently regardless of query language
- Medical AI is high stakes: accuracy gaps across languages carry real patient-harm risk

**Task**
- Build a framework to evaluate LLM accuracy across languages on a medical dataset
- Identify and understand any performance gaps

**Action**
- Built a Python evaluation framework to test GPT-4o on a multilingual medical dataset
- Ran evaluations in English, Arabic and other languages with consistent prompts
- Found a 13 percentage point accuracy gap: English outperformed Arabic
- Challenged my initial hypothesis and dug into why
- Hypothesized the model's internal representation was stronger in English
- Tested translate-first: prompt the model to translate the query to English before answering
- Translate-first significantly improved accuracy, which supported the hypothesis

**Result**
- Finding: GPT-4o is 13 pp more accurate in English than Arabic on medical data
- Translate-first prompting is a practical mitigation for practitioners
- Contributed to responsible-AI discussion of multilingual medical AI deployment

**Open**
- Exact dataset used?
- Peer reviewed or presented anywhere?
- What it means for real-world medical AI deployment

## 6a. Faulty production deployment

LP: Earn trust · Learn and be curious

**Situation**
- Working on an ECS Orchestrator service for a major banking client at Accenture
- Deployed a change that added a sync task on one entrypoint that exceeded the client's default
  timeout
- 100% of requests to that entrypoint failed, about 20% of total requests
- It went undetected for a full business day

**Task**
- Own the mistake, fix it fast, and prevent it from recurring

**Action**
- Immediately acknowledged it was my change; did not deflect or wait
- Diagnosed the root cause: sync task latency exceeded the client timeout and was not caught before
  deployment
- Rolled back and patched the issue
- Ran a post-mortem and was honest with the team about what I missed
- Made latency measurement a mandatory check in the component and live dependency tests: every
  entrypoint's latency is now validated before deployment
- Made it a habit to think adversarially before any prod push: what are the latency and timeout
  implications of this change?

**Result**
- Resolved the same day it was discovered
- The down entrypoint had blocked the client's ability to shift left on AWS config errors; that was
  restored
- Latency is now a standard test dimension across the service; the edge case is permanently closed
- The deployment process is stronger for the whole team, not just me

**Prepared answers**
- "What would you do differently?" I would have had latency and timeout validation in my
  pre-deployment checklist from day one.
- "Why did it take a full day to catch?" No alerting existed at the time; that gap was fixed
  separately with PagerDuty (6b).

## 6b. Production failure and alerting

LP: Earn trust · Ownership

**Situation**
- Co-owning an ECS Orchestrator service used by multiple teams at Accenture
- My change missed an edge case and caused ~20% of requests to fail
- It went undetected for a full business day before a teammate caught it

**Task**
- Fix the immediate issue and make sure it could never go undetected again

**Action**
- Immediately owned the mistake; rolled back and patched the edge case
- Identified the real problem: no alerting, so a 20% failure rate sat silent for a day
- Set up PagerDuty alerts on error-rate thresholds: any future spike pages the team in minutes

**Result**
- Resolved the same day it was discovered
- The team went from blind in production to alerted in real time
- Learned to own failures directly and fix the system, not just the symptom
- PagerDuty coverage is now part of every important feature we add

**Open**
- "Why did your change miss this edge case?" Own it specifically, don't be vague.
- Did PagerDuty fire after go-live?

## 6c. Automated testing tool: 3 hours to 10 minutes

LP: Invent and simplify · Insist on the highest standards

**Situation**
- Manual testing meant triggering several Jenkins pipelines and watching results by hand: 3 hours
  every two-week sprint
- Multiple teams contributed to the service, all subject to the same weak process

**Task**
- Build a better testing process and raise the bar across all contributing teams

**Action**
- Built component tests and live dependency tests covering the critical edge cases the old process
  missed
- Built an automated tool that triggered the Jenkins pipelines and observed and reported results
- Ran knowledge transfer sessions with contributing teams; our pipeline gated their deployments, so
  they had to pass the new tests to ship

**Result**
- Manual testing time cut from 3 hours to 10 minutes, every sprint
- The new edge-case coverage closed the gap that caused the original incident (6a)
- New standards rolled out across all contributing teams, not just ours
- The new tests caught multiple errors and serve as a regression suite on every deployment

**Open**
- How did other teams respond to the new testing gate?

## 7. Master's and a full-time job at the same time

LP: Deliver results · Bias for action

**Situation**
- Pursuing an MSc in Machine Learning at McGill/Mila while working full time as a Software Engineer
  at Accenture
- Both had real deadlines and deliverables; neither could be deprioritized
- High cognitive load: research, coursework and production engineering in parallel

**Task**
- Deliver strong results in both, with no shortcuts on either side

**Action**
- Ruthlessly prioritized: mapped deadlines across both tracks every week
- Blocked focused work time and kept research mode and engineering mode separate
- Told my manager ahead of time when the academic load peaked
- At school, focused on high-leverage research tasks, not busywork
- Treated time as the constraint: every hour had to count

**Result**
- Promoted at Accenture while completing the degree
- Learned that prioritization and focus matter more than hours worked

**Open**
- Confirm the MSc GPA and the promotion title before claiming "strong GPA" or "publishable research"
- "Did quality ever slip?" Be honest; this question is about self-awareness.

## 8. Unblocking QA: isolated testing environment for KDA Flink

LP: Invent and simplify · Deliver results · Ownership · Frugality

**Situation**
- A team of 7 engineers on a production KDA Flink application
- The QA environment had a single instance, shared by our team and sister teams
- Only one person could test at a time, creating long queues before any QA or prod deployment

**Task**
- Remove the bottleneck so the team could test and ship independently and in parallel
- Keep the new applications cheap and easy to maintain

**Action**
- Identified the root cause: one shared QA instance with no isolation between testers
- Designed a new isolated testing environment, separate from the shared QA instance
- Mocked all API and DB calls so it never interfered with the real QA app used by our team and
  sister teams
- Deployed 5 isolated instances of the app, one per developer
- Each engineer could test independently and in parallel without blocking anyone
- Kept costs low with mocked API calls and auto-stopping applications

**Result**
- Removed the one-person-at-a-time bottleneck for a team of 7
- Faster testing cycles and faster deployments to production
- Sister teams were no longer affected by our testing
- Waits of 2-4 hours per deployment dropped to zero

**Open**
- How many deployments per sprint were unblocked?
- Why mocking specifically; what would have happened without it?

## 9. Onboarding and mentoring new-grad joiners

LP: Hire and develop the best · Ownership

**Situation**
- Three new-grad engineers joined the team at Accenture
- Joining a large consulting firm on a complex client project is overwhelming: company processes,
  technical context and team dynamics all at once
- No one was formally assigned to support them

**Task**
- Volunteered as the buddy for all three
- Goal: get them productive and delivering real work as fast as possible

**Action**
- Ran onboarding sessions on company processes: how we work, how we ship, how the client engagement
  operates
- Delivered KTs on the team's core systems: the KDA Flink app, the CI/CD pipeline, the ECS
  Orchestrator service
- Mapped the team's subject matter experts by area and personally introduced each new grad to the
  right SME for their work, so they knew exactly who to go to
- Stayed available for questions throughout their first weeks

**Result**
- All three were contributing and delivering their first tasks within 3 weeks of joining
- Strong positive feedback from the new grads directly
- Less of the ramp-up friction that usually slows new joiners on complex client projects

**Open**
- One specific moment where the support made a real difference for one of them
- "Would you do anything differently?"

## 10. Customer obsession: fraud detection AI agent POC

LP: Customer obsession · Think big · Invent and simplify

**Situation**
- AI Engineer at Accenture on a banking client engagement
- Fraud detection was handled manually by human agents, with no AI involved
- Outside my immediate scope, but I saw an opportunity to apply AI meaningfully

**Task**
- Understand the fraud detection process deeply enough to know if and how AI could help
- Go beyond the requirements and talk to the people actually doing the work

**Action**
- Set up meetings with Product Owners and fraud detection agents on my own initiative
- Asked about their process end to end: how alerts came in, how they investigated, what data they
  used, where they spent the most time
- Found the process was highly sequential and reasoning-heavy: a good fit for an agentic approach
- Designed and built a POC with a Plan, Execute, Replan pattern: the agent receives a fraud alert,
  plans an investigation, executes it over customer and transaction history via RAG, then replans
  if new information changes the picture
- Presented the POC to stakeholders with a clear mapping to the real agent workflow

**Result**
- The POC was well received and validated that AI could meaningfully augment fraud detection
- Another team is now building it into a real product
- Going directly to the end users, not just the POs, made the POC credible and grounded in the
  real workflow rather than assumptions
- Built in 4 weeks; very good feedback, and it was approved as a production application to
  implement (Aly, 2026-10-04)

**Open**
- "What would the POC have looked like without talking to the agents?"
