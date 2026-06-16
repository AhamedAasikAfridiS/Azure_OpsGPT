# API Overview

## Core API Service

- `POST /auth/login`
- `GET /auth/me`
- `GET /projects`
- `POST /projects`
- `GET /projects/{project_id}`
- `PATCH /projects/{project_id}`
- `DELETE /projects/{project_id}`
- `GET /projects/{project_id}/monitoring-sources`
- `POST /projects/{project_id}/monitoring-sources`
- `GET /projects/{project_id}/members`
- `POST /projects/{project_id}/members`
- `GET /projects/{project_id}/dashboard/summary`
- `GET /projects/{project_id}/incidents`
- `GET /projects/{project_id}/incidents/{incident_id}`
- `POST /internal/incidents`
- `PATCH /internal/incidents/{incident_id}/analysis`
- `GET /internal/projects/{project_id}/monitoring-sources/validate?token=...`

Monitoring source types: `grafana`, `azure_monitor`, `prometheus_alertmanager`, `datadog`, `new_relic`, `splunk`, `elastic`, `sentry`, `pagerduty`, `aws_cloudwatch`, `google_cloud_monitoring`, `dynatrace`, `appdynamics`, `zabbix`, `nagios`, `custom`.

## Alert Ingestion Service

- `POST /alerts/webhook/project/{project_id}/{webhook_token}`
- `POST /alerts/webhook/azure-monitor`
- `POST /alerts/webhook/grafana`
- `POST /alerts/manual`
- `GET /alerts`
- `GET /alerts/{alert_id}`
- `GET /alerts/{alert_id}/raw`
- `GET /health`

Project-specific webhooks are recommended. The service validates the token with Core API, selects a parser, stores raw payload, normalizes the alert, and forwards it when enabled.

## AI Analysis Service

- `POST /analysis/alerts`
- `POST /analysis/correlate`
- `POST /analysis/generate-summary`
- `POST /analysis/generate-rca`
- `POST /analysis/generate-fix`
- `POST /analysis/similar-incidents`
- `GET /analysis/incidents/{incident_id}`
- `GET /health`

AI Analysis uses Microsoft Foundry / Azure AI Foundry only. It does not use mock output.

## Notification Service

- `POST /notifications/events`
- `POST /notifications/slack/test`
- `GET /notifications`
- `GET /notifications/{notification_id}`
- `GET /notifications/incident/{incident_id}`
- `GET /health`
