# API Overview

Nginx is the recommended local/VM entry point.

```text
Frontend:          http://<VM_IP>:8080
Core API:          http://<VM_IP>:8080/api/core
Alert Ingestion:   http://<VM_IP>:8080/api/alerts
AI Analysis:       http://<VM_IP>:8080/api/analysis
Notification:      http://<VM_IP>:8080/api/notifications
Project Webhook:   http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

## Core API

Main route prefix through Nginx:

```text
/api/core/
```

Important endpoints:

- `POST /auth/login`
- `GET /auth/me`
- `GET /projects`
- `POST /projects`
- `GET /projects/{project_id}/dashboard/summary`
- `GET /projects/{project_id}/incidents`
- `GET /projects/{project_id}/incidents/{incident_id}`
- `GET /projects/{project_id}/monitoring-sources`
- `POST /projects/{project_id}/monitoring-sources`
- `GET /internal/projects/{project_id}/monitoring-sources/validate?token=...`

## Alert Ingestion

Main route prefix through Nginx:

```text
/api/alerts/
```

Recommended webhook route:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

This route intentionally stays outside `/api/alerts` so external monitoring systems can use a clean webhook URL.

## AI Analysis

Main route prefix through Nginx:

```text
/api/analysis/
```

AI Analysis uses Microsoft Foundry / Azure AI Foundry.

## Notification

Main route prefix through Nginx:

```text
/api/notifications/
```
