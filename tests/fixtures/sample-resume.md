# Jordan Avery Quill

Contact: Chicago, IL, USA | jordan.quill@example.com | +1 555-0142 | linkedin.com/in/example-jordan-quill

Fictional sample resume for the onboarding walkthrough. The person, companies and university are made up.

## Experience

### Senior Backend Engineer, Lakeshore Ledger Co. (Chicago, IL) - Mar 2022 to present

- Designed and built a Python and Go payments reconciliation service that matches 4M ledger entries a day against bank files.
- Cut the nightly settlement batch from 3 hours to 40 minutes by moving it to partitioned PostgreSQL queries and parallel workers.
- Led the move of six services from a shared VM fleet to Kubernetes on AWS, with zero customer-facing downtime.
- Introduced contract tests between the billing API and its four consumers, cutting integration incidents by half in two quarters.
- Built an idempotent event pipeline on Kafka so retried webhooks never double-charge a customer.
- Added OpenTelemetry tracing and SLO dashboards, bringing mean time to detect a payment failure under 5 minutes.
- Mentored three junior engineers through design reviews and pairing; two were promoted within 18 months.
- Wrote the team's API versioning guide, adopted by two other backend teams.

### Software Engineer, Prairie Freight Systems (Chicago, IL) - Jul 2019 to Feb 2022

- Built REST and gRPC APIs in Java and Spring Boot for a shipment tracking platform serving 1,200 carriers.
- Replaced a cron-based polling job with a message-driven design on RabbitMQ, cutting tracking update lag from 15 minutes to under 1.
- Designed the Redis caching layer for rate quotes, lowering p95 latency from 900 ms to 120 ms.
- Automated database schema migrations with Flyway and added them to the CI pipeline.
- Wrote load tests with k6 that caught two capacity limits before peak season.
- Raised unit test coverage of the routing module from 35% to 80%.
- Worked with the data team to publish shipment events to the warehouse for daily reporting.

## Projects

### Tidewatch (open source)

- A small Go CLI that watches public transit feeds and posts delay alerts to a chat channel; 300 stars.

### Ledgerlint

- A Python linter for double-entry accounting CSV files that flags unbalanced journal entries before import.

## Education

### Northgate Institute of Technology - B.S. Computer Science, 2019

- Coursework: distributed systems, databases, operating systems, algorithms.

## Skills

- Languages: Python, Go, Java, SQL
- Frameworks: Spring Boot, FastAPI, gRPC
- Data and messaging: PostgreSQL, Redis, Kafka, RabbitMQ
- Cloud and tooling: AWS, Kubernetes, Docker, Terraform, GitHub Actions, OpenTelemetry
