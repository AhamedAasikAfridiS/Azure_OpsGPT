# OpsGPT Phase 1

OpsGPT is a local, Docker-based AI incident management platform for DevOps, SRE, Cloud Engineering, and Operations teams.

Phase 1 keeps a five-service microservices architecture:

| Service | Port | Responsibility |
| --- | --- | --- |
| frontend-service | 3000 | React UI for login, project selection, dashboard, incidents, knowledge base, and admin setup |
| core-api-service | 8001 | Auth, RBAC, projects, monitoring source metadata, incidents, dashboard, audit logs, knowledge base |
| alert-ingestion-service | 8002 | Webhook alert receiving, raw payload storage, dynamic parsing, normalization, forwarding |
| ai-analysis-service | 8003 | Correlation, duplicate detection, Microsoft Foundry AI analysis, Core API incident updates |
| notification-service | 8004 | Console or Slack notification delivery |

## Current Phase 1 Flow

1. Admin creates a project in OpsGPT.
2. Admin adds a monitoring source such as Grafana, Azure Monitor, Datadog, Prometheus Alertmanager, or Custom Webhook.
3. OpsGPT generates a project-specific webhook path:
   `/alerts/webhook/project/{project_id}/{webhook_token}`
4. The monitoring system sends triggered alert payloads to that webhook.
5. Alert Ingestion stores the raw payload, uses a source parser or universal fallback parser, and normalizes the alert.
6. AI Analysis correlates alerts and calls Microsoft Foundry / Azure AI Foundry.
7. Core API stores the incident.
8. Frontend displays project-scoped incidents.
9. Notification Service sends console or Slack notifications when enabled.

OpsGPT does not scrape Grafana, Azure Monitor, Datadog, or other dashboards. It receives triggered webhook payloads.

## AI Provider

AI Analysis now uses Microsoft Foundry / Azure AI Foundry only.

Required AI Analysis variables:

```env
AI_PROVIDER=foundry
FOUNDRY_ENDPOINT=
FOUNDRY_API_KEY=
FOUNDRY_MODEL_DEPLOYMENT=
FOUNDRY_API_VERSION=2024-02-15-preview
```

Ollama, Gemini, and direct OpenAI provider modes are removed/deprecated for this project. AI failures are stored as failed analysis records and should not block deterministic incident creation.

## Supported Webhook Sources

Grafana, Azure Monitor, Prometheus Alertmanager, Datadog, New Relic, Splunk, Elastic / Kibana, Sentry, PagerDuty, AWS CloudWatch, Google Cloud Monitoring, Dynatrace, AppDynamics, Zabbix, Nagios, and Custom Webhook.

Vendor parsers are best-effort in Phase 1 and backed by the universal parser fallback.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Microservices](docs/MICROSERVICES.md)
- [Local Development](docs/LOCAL_DEVELOPMENT.md)
- [Development Run Guide](docs/DEVELOPMENT_RUN_GUIDE.md)
- [API Overview](docs/API_OVERVIEW.md)
- [Single VM Docker Deployment](docs/SINGLE_VM_DOCKER_DEPLOYMENT.md)
- [Foundry AI and Dynamic Webhooks](docs/FOUNDRY_AND_DYNAMIC_WEBHOOKS.md)
