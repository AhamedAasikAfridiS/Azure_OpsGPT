# API Overview

## Frontend Routes

| Route | Purpose |
| --- | --- |
| `/login` | User authentication |
| `/dashboard` | Incident summary and recent incidents |
| `/incidents` | Searchable and filterable incident list |
| `/incidents/:incidentId` | Incident analysis, timeline, similar incidents, and editor actions |
| `/knowledge-base` | Historical incident knowledge |
| `/profile` | Current user profile and role |
| `/projects` | Select an assigned project |
| `/projects/:projectId/dashboard` | Project incident summary |
| `/projects/:projectId/incidents` | Project incident list |
| `/projects/:projectId/incidents/:incidentId` | Project incident detail |
| `/admin/projects` | Admin project and membership management |
| `/admin/projects/:projectId/sources` | Admin monitoring source management |

## Core API Service

Base URL: `http://localhost:8001`

### Authentication

```text
POST /auth/login
GET  /auth/me
POST /auth/logout
```

### Users

```text
GET   /users/me
GET   /users
POST  /users
PATCH /users/{user_id}/role
```

User administration endpoints require the admin role.

Admin user search:

```text
GET /users/search?query={name_email_or_role}&limit=20
```

The search returns active users only and never exposes password hashes.

### Dashboard

```text
GET /dashboard/summary
GET /dashboard/severity-counts
GET /dashboard/status-counts
GET /dashboard/recent-incidents
```

### Incidents

```text
GET   /incidents
GET   /incidents/{incident_id}
PATCH /incidents/{incident_id}/status
POST  /incidents/{incident_id}/resolution-notes
GET   /incidents/{incident_id}/timeline
GET   /incidents/{incident_id}/similar
```

### Knowledge Base and Audits

```text
GET  /knowledge-base
GET  /knowledge-base/{kb_id}
POST /knowledge-base
GET  /audit-logs
```

### Projects and Memberships

```text
GET    /projects
POST   /projects
GET    /projects/{project_id}
PATCH  /projects/{project_id}
DELETE /projects/{project_id}

GET    /projects/{project_id}/members
POST   /projects/{project_id}/members
DELETE /projects/{project_id}/members/{user_id}

GET /projects/{project_id}/dashboard/summary
GET /projects/{project_id}/incidents
GET /projects/{project_id}/incidents/{incident_id}
```

Project modification and membership endpoints require `admin`. Junior and
senior engineers can read only projects assigned to them.

The admin project screen uses `/users/search` to find employees by name,
email, or role before assigning them. Duplicate project memberships return
HTTP 409.

### Monitoring Sources

```text
GET    /projects/{project_id}/monitoring-sources
POST   /projects/{project_id}/monitoring-sources
GET    /projects/{project_id}/monitoring-sources/{source_id}
PATCH  /projects/{project_id}/monitoring-sources/{source_id}
DELETE /projects/{project_id}/monitoring-sources/{source_id}
```

These admin-only endpoints store Grafana, Azure Monitor, or custom source
metadata and return the generated project webhook path and token.

### Internal Service Endpoints

```text
POST  /internal/incidents
PATCH /internal/incidents/{incident_id}/analysis
POST  /internal/incidents/{incident_id}/timeline
GET   /internal/projects/{project_id}/monitoring-sources/validate
```

Internal endpoints require:

```text
X-Internal-API-Key: change-me-internal-key
```

### Health

```text
GET /health
```

## Alert Ingestion Service

Base URL: `http://localhost:8002`

```text
POST /alerts/webhook/azure-monitor
POST /alerts/webhook/grafana
POST /alerts/webhook/project/{project_id}/{webhook_token}
POST /alerts/manual
GET  /alerts
GET  /alerts/{alert_id}
GET  /alerts/{alert_id}/raw
GET  /health
```

Alert Ingestion accepts source payloads, stores raw data, returns normalized
alerts, and optionally forwards valid alerts to AI Analysis.

## AI Analysis Service

Base URL: `http://localhost:8003`

```text
POST /analysis/alerts
POST /analysis/correlate
POST /analysis/generate-summary
POST /analysis/generate-rca
POST /analysis/generate-fix
POST /analysis/similar-incidents
GET  /analysis/incidents/{incident_id}
GET  /health
```

`POST /analysis/alerts` accepts normalized alerts only. It does not accept raw
Azure Monitor or Grafana payloads.

## Notification Service

Base URL: `http://localhost:8004`

```text
POST /notifications/events
POST /notifications/slack/test
GET  /notifications
GET  /notifications/{notification_id}
GET  /notifications/incident/{incident_id}
GET  /health
```

Notification events are normally sent by Core API. Notification Service
formats, delivers, and records them.

## Authentication Summary

Frontend and public Core API workflows use:

```text
Authorization: Bearer <JWT>
```

AI Analysis to Core API communication uses:

```text
X-Internal-API-Key: <shared key>
```

Alert Ingestion, AI Analysis development endpoints, and Notification Service
do not implement user JWT authentication in Phase 1.
