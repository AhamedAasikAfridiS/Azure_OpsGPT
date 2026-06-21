# OpsGPT Microservices

## frontend-service

React/Vite service on port `3000`. It calls Core API through:

```text
VITE_CORE_API_URL=/api/core
```

The UI includes login, project selection, project dashboard, incidents, incident detail, admin project setup, Prometheus Alertmanager source setup, member assignment, profile, and knowledge base views.

Microsoft Entra ID sign-in uses MSAL redirect flow. The frontend requests the configured Core API scope, attaches the access token to Core API calls, and uses the role returned by `GET /auth/me` for display only.

## core-api-service

FastAPI service on port `8001`.

Responsibilities:

- Microsoft Entra ID access-token validation with cached JWKS
- App-role mapping from token `roles` to existing OpsGPT RBAC roles
- Optional local JWT fallback when explicitly enabled
- User profile
- RBAC
- Project management
- Project membership
- Prometheus Alertmanager monitoring source metadata
- Project-specific webhook token generation
- Incident storage
- Dashboard APIs
- Incident status updates
- Resolution notes
- Audit logs
- Knowledge base
- Internal APIs for AI Analysis and Alert Ingestion
- Optional notification trigger

Core API does not parse Alertmanager raw payloads, generate AI analysis, send Slack directly, or receive monitoring webhooks directly.

Core API never trusts a role supplied by the frontend. It accepts `OpsGPT.Admin`, `OpsGPT.Senior`, and `OpsGPT.Junior` from a validated Entra token's `roles` claim, with Admin/Senior/Junior priority, then upserts the Entra user locally. Internal routes remain protected by `X-Internal-API-Key` rather than Entra user tokens.

## alert-ingestion-service

FastAPI service on port `8002`.

Responsibilities:

- Receive Prometheus Alertmanager webhook payloads
- Validate project webhook token through Core API
- Store full raw payload
- Normalize every item in `alerts[]`
- Store normalized alerts
- Forward normalized alerts to AI Analysis when enabled
- Return controlled failures for malformed payloads or downstream errors

Only `prometheus_alertmanager` is supported. Deprecated Grafana and Azure Monitor routes return `410 Gone`.

## ai-analysis-service

FastAPI service on port `8003`.

Responsibilities:

- Receive normalized alerts
- Store analysis alerts
- Detect duplicates
- Correlate alerts by project, service, namespace, cluster, environment, and a 10-minute window
- Create incidents through Core API
- Call Azure AI Foundry only when configured, using the Responses API by default and Chat Completions as a compatibility mode
- Store analysis results
- Update Core API with AI summary, RCA, evidence, confidence, and recommendations

AI Analysis does not parse raw Alertmanager payloads, manage users/RBAC, send Slack directly, or write directly to Core API tables. Missing Foundry configuration, request failures, or invalid model JSON record a failed analysis without preventing correlated incident creation. No other cloud integration is implemented in Phase 1.

## notification-service

FastAPI service on port `8004`.

Responsibilities:

- Receive notification events from Core API
- Send console or Slack notifications
- Store notification records
- Store delivery attempts

Default channel is:

```text
NOTIFICATION_CHANNEL=console
```

Slack is used only when:

```text
NOTIFICATION_CHANNEL=slack
SLACK_WEBHOOK_URL=<configured>
```

## Shared Database

All backend services use one shared PostgreSQL database in Phase 1. Table prefixes keep service ownership clear:

- Core: normal domain tables such as `users`, `projects`, `incidents`
- Alert Ingestion: `alert_*`
- AI Analysis: `analysis_*`
- Notification: `notification_*`
