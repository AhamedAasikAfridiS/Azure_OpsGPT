# OpsGPT Architecture

OpsGPT Phase 1 is a local, webhook/event-driven microservices application.

```text
Grafana / Azure Monitor / Datadog / Prometheus / Other Source
        |
        | triggered webhook payload
        v
Alert Ingestion Service
        |
        | normalized alert
        v
AI Analysis Service
        |
        | internal REST API
        v
Core API Service
        |
        | user-facing REST API
        v
Frontend Service

Core API Service -> Notification Service
```

Grafana, Azure Monitor, Datadog, and other tools continuously monitor systems. OpsGPT does not scrape dashboards or monitoring UIs. OpsGPT receives alert payloads only when those tools trigger webhook notifications.

## Project-Based Webhooks

Admins create projects and monitoring sources in the Core API. Each monitoring source gets a webhook token and path:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

The Alert Ingestion Service validates the project and token with the Core API, selects the parser for the source type, stores the raw payload, normalizes it, and optionally forwards it to AI Analysis.

## Dynamic Parsing

Alert Ingestion uses source-specific parsers when possible. If a payload does not match a fixed vendor schema, the universal parser recursively searches common field aliases and assigns safe defaults. This allows production-style dynamic payloads to be accepted without brittle schema failures.

## AI Analysis

AI Analysis uses Microsoft Foundry / Azure AI Foundry only. It sends structured prompts asking for JSON incident analysis. If the Foundry call fails or returns invalid JSON, the failure is stored and the incident pipeline continues with deterministic incident data.
