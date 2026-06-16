# OpsGPT Phase 1 - Local Development Run Guide

This guide helps a developer run OpsGPT locally after code generation.

## Phase 1 Scope

- Local development only
- No Azure deployment infrastructure
- No Kubernetes
- No Nginx
- No real Azure Monitor or Grafana setup required
- Alerts can be tested using sample payloads
- AI Analysis uses Microsoft Foundry / Azure AI Foundry

## Architecture Summary

```text
Grafana / Azure Monitor / Observability Source / Manual Alert
↓
Alert Ingestion Service
↓
AI Analysis Service
↓
Core API Service
↓
Frontend Service
↓
Notification Service
```

Grafana, Azure Monitor, and other monitoring tools continuously monitor systems. OpsGPT does not scrape dashboards. OpsGPT receives triggered alert payloads through webhooks.

## Services

| Service | Port | Responsibility | Depends on |
| --- | --- | --- | --- |
| frontend-service | 3000 | React UI | core-api-service |
| core-api-service | 8001 | Auth, RBAC, projects, incidents, dashboard, knowledge base | core-db, notification-service optional |
| alert-ingestion-service | 8002 | Alert receiving, dynamic parsing, normalization | alert-db, core-api-service, ai-analysis-service optional |
| ai-analysis-service | 8003 | Correlation, Foundry AI summary/RCA/fix recommendation | analysis-db, core-api-service |
| notification-service | 8004 | Console/Slack notifications | notification-db |

## Environment Setup

Copy examples to real env files:

```bash
cp core-api-service/.env.example core-api-service/.env
cp alert-ingestion-service/.env.example alert-ingestion-service/.env
cp ai-analysis-service/.env.example ai-analysis-service/.env
cp notification-service/.env.example notification-service/.env
cp frontend-service/.env.example frontend-service/.env
```

Important values:

- Core API: `DATABASE_URL`, `JWT_SECRET_KEY`, `INTERNAL_API_KEY`, `NOTIFICATION_SERVICE_URL`, `ENABLE_NOTIFICATIONS`
- Alert Ingestion: `DATABASE_URL`, `CORE_API_URL`, `INTERNAL_API_KEY`, `AI_ANALYSIS_SERVICE_URL`, `ENABLE_ANALYSIS_FORWARDING`
- AI Analysis: `DATABASE_URL`, `CORE_API_URL`, `INTERNAL_API_KEY`, `AI_PROVIDER=foundry`, `FOUNDRY_ENDPOINT`, `FOUNDRY_API_KEY`, `FOUNDRY_MODEL_DEPLOYMENT`
- Notification: `DATABASE_URL`, `NOTIFICATION_CHANNEL`, `SLACK_WEBHOOK_URL`
- Frontend: `VITE_CORE_API_URL`

## Microsoft Foundry Setup

Set these values in `ai-analysis-service/.env`:

```env
AI_PROVIDER=foundry
FOUNDRY_ENDPOINT=https://<your-foundry-or-azure-ai-endpoint>
FOUNDRY_API_KEY=<your-key>
FOUNDRY_MODEL_DEPLOYMENT=<your-model-deployment>
FOUNDRY_API_VERSION=2024-02-15-preview
FOUNDRY_TIMEOUT_SECONDS=60
FOUNDRY_MAX_RETRIES=2
FOUNDRY_CHAT_COMPLETIONS_PATH=/openai/deployments/{deployment}/chat/completions?api-version={api_version}
```

If the endpoint does not support `response_format`, the client retries once without it and still asks the model to return JSON only.

## Full Local Workflow Mode

To test the full flow:

```env
# alert-ingestion-service/.env
ENABLE_ANALYSIS_FORWARDING=true

# core-api-service/.env
ENABLE_NOTIFICATIONS=true

# notification-service/.env
NOTIFICATION_CHANNEL=console
```

## Docker Compose Commands

Documentation only:

```bash
docker compose build
docker compose up
docker compose down
docker compose down -v
```

## Local URLs

- Frontend: `http://localhost:3000`
- Core API docs: `http://localhost:8001/docs`
- Alert Ingestion API docs: `http://localhost:8002/docs`
- AI Analysis API docs: `http://localhost:8003/docs`
- Notification API docs: `http://localhost:8004/docs`

## Project Webhook Flow

1. Login as admin.
2. Create a project.
3. Add a monitoring source.
4. Copy the generated webhook path:
   `/alerts/webhook/project/{project_id}/{webhook_token}`
5. Configure that URL in Grafana, Azure Monitor, Datadog, or another webhook-capable tool.
6. Send sample payloads from `sample-payloads/`.

Supported sources: Grafana, Azure Monitor, Prometheus Alertmanager, Datadog, New Relic, Splunk, Elastic / Kibana, Sentry, PagerDuty, AWS CloudWatch, Google Cloud Monitoring, Dynatrace, AppDynamics, Zabbix, Nagios, and Custom Webhook.

## Troubleshooting

Issue: Alert is stored but not analyzed
- Set `ENABLE_ANALYSIS_FORWARDING=true`.
- Confirm AI Analysis is running.
- Confirm Foundry env vars are set.

Issue: AI analysis failed
- Check `FOUNDRY_ENDPOINT`, `FOUNDRY_API_KEY`, and `FOUNDRY_MODEL_DEPLOYMENT`.
- Check whether your endpoint path needs a custom `FOUNDRY_CHAT_COMPLETIONS_PATH`.
- Invalid JSON from the model is stored as failed analysis; OpsGPT does not generate fake fallback output.

Issue: Incident created but no notification
- Set `ENABLE_NOTIFICATIONS=true`.
- Use `NOTIFICATION_CHANNEL=console` for local testing.

Issue: Internal API returns unauthorized
- Confirm `X-Internal-API-Key`.
- Confirm `INTERNAL_API_KEY` matches across services.

## Current Limitations

- Vendor parsers are best-effort in Phase 1.
- Universal parsing is intentionally tolerant and should be hardened per vendor in production.
- No real Azure deployment infrastructure.
- No service bus/event broker.
- Local REST communication is used.
