# API Overview

All browser calls should go through Nginx.

## Core API

Base path:

```text
/api/core
```

Auth:

- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/logout`

Users:

- `GET /users/me`
- `GET /users`
- `GET /users/search?query=<text>`
- `POST /users`
- `PATCH /users/{user_id}/role`

Projects:

- `GET /projects`
- `POST /projects`
- `GET /projects/{project_id}`
- `PATCH /projects/{project_id}`
- `DELETE /projects/{project_id}`

Project members:

- `GET /projects/{project_id}/members`
- `POST /projects/{project_id}/members`
- `DELETE /projects/{project_id}/members/{user_id}`

Monitoring sources:

- `GET /projects/{project_id}/monitoring-sources`
- `POST /projects/{project_id}/monitoring-sources`
- `GET /projects/{project_id}/monitoring-sources/{source_id}`
- `PATCH /projects/{project_id}/monitoring-sources/{source_id}`
- `DELETE /projects/{project_id}/monitoring-sources/{source_id}`

Project dashboard and incidents:

- `GET /projects/{project_id}/dashboard/summary`
- `GET /projects/{project_id}/incidents`
- `GET /projects/{project_id}/incidents/{incident_id}`

Global incidents:

- `GET /incidents`
- `GET /incidents/{incident_id}`
- `PATCH /incidents/{incident_id}/status`
- `POST /incidents/{incident_id}/resolution-notes`
- `GET /incidents/{incident_id}/timeline`
- `GET /incidents/{incident_id}/similar`

Knowledge base:

- `GET /knowledge-base`
- `GET /knowledge-base/{kb_id}`
- `POST /knowledge-base`

Audit logs:

- `GET /audit-logs`

Internal APIs require:

```text
X-Internal-API-Key: <INTERNAL_API_KEY>
```

Internal endpoints:

- `POST /internal/incidents`
- `PATCH /internal/incidents/{incident_id}/analysis`
- `POST /internal/incidents/{incident_id}/timeline`
- `GET /internal/projects/{project_id}/monitoring-sources/validate?token=<webhook_token>`

## Alert Ingestion API

Base paths:

```text
/api/alerts
/alerts/webhook
```

Endpoints:

- `GET /health`
- `POST /alerts/webhook/project/{project_id}/{webhook_token}`
- `POST /alerts/webhook/prometheus-alertmanager`
- `POST /alerts/manual`
- `POST /alerts/webhook/grafana` returns `410 Gone`
- `POST /alerts/webhook/azure-monitor` returns `410 Gone`

Project webhook response:

```json
{
  "status": "processed",
  "source": "prometheus_alertmanager",
  "project_id": "...",
  "received_alert_count": 2,
  "normalized_alert_count": 2,
  "forwarding_enabled": true,
  "forwarded_count": 2,
  "failed_forward_count": 0
}
```

## AI Analysis API

Base path:

```text
/api/analysis
```

Endpoints:

- `GET /health`
- `POST /analysis/alerts`
- `POST /analysis/correlate`
- `GET /analysis/incidents/{incident_id}`

Only `ai-analysis-service` calls Azure AI Foundry. It supports the Responses API by default and a Chat Completions compatibility mode. `GET /health` does not test Foundry connectivity. AI Analysis stores failure details when configuration is missing, AI calls fail, invalid JSON is returned, or Core API cannot be updated; correlation can still create the incident.

## Notification API

Base path:

```text
/api/notifications
```

Endpoints:

- `GET /health`
- `POST /notifications/events`
- `POST /notifications/slack/test`
- `GET /notifications`
- `GET /notifications/{notification_id}`
- `GET /notifications/incident/{incident_id}`

Notification event types:

- `incident_created`
- `ai_analysis_completed`
- `incident_status_updated`
- `incident_resolved`
- `resolution_notes_added`

## Alert Source

Phase 1 supports Prometheus Alertmanager webhooks only. OpsGPT does not scrape dashboards or query the Prometheus metrics API in Phase 1.
