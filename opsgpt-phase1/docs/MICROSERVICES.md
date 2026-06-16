# OpsGPT Microservices

| Service | Responsibility | Boundaries |
| --- | --- | --- |
| frontend-service | React UI for project selection, dashboard, incidents, knowledge base, profile, and admin project/source setup | Calls Core API for normal user workflows |
| core-api-service | Auth, RBAC, users, projects, monitoring source metadata, incidents, dashboards, audit logs, knowledge base | Does not receive raw alerts or generate AI analysis |
| alert-ingestion-service | Receives webhooks, validates project webhook tokens, stores raw payloads, dynamically parses and normalizes alerts | Does not create incidents directly |
| ai-analysis-service | Detects duplicates, correlates alerts, calls Microsoft Foundry, creates/updates incidents through Core API internal APIs | Does not parse vendor webhook payloads or write Core DB directly |
| notification-service | Receives notification events and sends console/Slack messages | Does not analyze incidents or update incident status |

## Supported Monitoring Sources

Grafana, Azure Monitor, Prometheus Alertmanager, Datadog, New Relic, Splunk, Elastic / Kibana, Sentry, PagerDuty, AWS CloudWatch, Google Cloud Monitoring, Dynatrace, AppDynamics, Zabbix, Nagios, and Custom Webhook.

Each source is webhook-based. Admins may store dashboard URLs and alert rule URLs as metadata, but OpsGPT does not scrape those dashboards.
