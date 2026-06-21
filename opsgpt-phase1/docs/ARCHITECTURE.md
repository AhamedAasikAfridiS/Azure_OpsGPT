# OpsGPT Architecture

## Phase 1 Topology

OpsGPT Phase 1 is a local Docker Compose application fronted by Nginx.

```text
Browser
  |
  v
Nginx :8080
  |-- /                  -> frontend-service:3000
  |-- /api/core/         -> core-api-service:8001
  |-- /api/alerts/       -> alert-ingestion-service:8002
  |-- /api/analysis/     -> ai-analysis-service:8003
  |-- /api/notifications/-> notification-service:8004
  |-- /alerts/webhook/   -> alert-ingestion-service:8002/alerts/webhook/
```

## Alert Flow

Prometheus and Alertmanager usually run inside Kubernetes. Prometheus scrapes workload metrics and evaluates alert rules. Alertmanager sends fired or resolved alert notifications to OpsGPT's project webhook.

OpsGPT does not scrape dashboards, query Prometheus metrics, or connect to Grafana dashboards in Phase 1.

```text
Kubernetes workloads
  -> Prometheus
  -> Alertmanager
  -> OpsGPT Alert Ingestion
  -> OpsGPT AI Analysis
  -> OpsGPT Core API
  -> OpsGPT Frontend
  -> OpsGPT Notification Service
```

## Shared Database

Phase 1 uses one PostgreSQL service named `opsgpt-db` with database `opsgpt_db`.

All backend services use the same database URL:

```text
postgresql://opsgpt_user:opsgpt_password@opsgpt-db:5432/opsgpt_db
```

This is a Phase 1 development decision. The microservices remain separate at the application and service level. Future production phases can split databases per service if needed.

The Core API container runs a pre-start bootstrap that creates Core API tables and enforces the default local users. This keeps first startup and stale development volumes recoverable without introducing a separate migration service.

## Project Webhook

Admins create a project and then create a Prometheus Alertmanager monitoring source. Core API generates:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

Through Nginx:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

Alert Ingestion validates `{project_id}` and `{webhook_token}` through Core API before accepting the project-scoped payload.

## AI Failure Behavior

AI Analysis creates deterministic incidents when correlation succeeds. Foundry AI fields are added only if Foundry is configured and returns valid JSON. Missing config, request failure, or invalid JSON records an analysis failure and leaves AI fields empty for the frontend.

## Microsoft Entra ID IAM

The browser signs in through MSAL and sends an Entra access token only to Core API. Core API fetches and caches Entra JWKS, validates the token signature, issuer, audience, expiry, and tenant, then maps the token `roles` claim to the existing RBAC role.

```text
OpsGPT_Admins  -> OpsGPT.Admin  -> admin
OpsGPT_Seniors -> OpsGPT.Senior -> senior_engineer
OpsGPT_Juniors -> OpsGPT.Junior -> junior_engineer
```

Entra Groups are assigned to app roles in the Enterprise Application. Raw group object IDs are not used as the primary authorization mechanism. Alert Ingestion and AI Analysis keep using `X-Internal-API-Key` for internal Core API routes and are not redirected through Entra authentication.

## Next Phase Exclusions

Azure deployment, AKS, Azure Service Bus, Terraform, Helm, Kubernetes manifests, App Service, Container Apps, private endpoints, and production networking are intentionally excluded from Phase 1.
