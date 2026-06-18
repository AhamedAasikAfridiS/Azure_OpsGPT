# OpsGPT Project Context

Before doing any future task, Codex must read this file and follow it as the source of truth. If the user confirms new requirements, update this file. Do not add features outside this context unless explicitly requested.

## Project Purpose

OpsGPT is an internal AI first responder for production incidents. It receives Prometheus Alertmanager webhook notifications, normalizes and correlates alerts, creates incidents, requests Microsoft Foundry / Azure AI Foundry analysis when configured, displays incidents in a web UI, and sends operational notifications.

## Phase 1 Scope

Phase 1 is local application development only. The application should run locally or on a VM through Docker Compose and an Nginx reverse proxy.

Do not add Azure deployment infrastructure, AKS deployment, Azure Service Bus, Terraform, Helm, Kubernetes manifests, Azure App Service deployment, Azure Container Apps deployment, Microsoft Entra ID integration, production networking, private endpoints, or cloud infrastructure files unless explicitly requested in a later phase.

## Locked Architecture

Keep exactly these five services:

1. `frontend-service`
2. `core-api-service`
3. `alert-ingestion-service`
4. `ai-analysis-service`
5. `notification-service`

Do not add more microservices. Do not merge these services into a monolith.

## Database Decision

Phase 1 uses one shared PostgreSQL database for all backend microservices.

- Service name: `opsgpt-db`
- Database name: `opsgpt_db`
- User: `opsgpt_user`
- Password: `opsgpt_password`
- Shared URL: `postgresql://opsgpt_user:opsgpt_password@opsgpt-db:5432/opsgpt_db`

The microservices remain separate at the application and service level. The shared database is a Phase 1 development simplification. Future production phases can split databases per service if needed.

Use clear table names to avoid conflicts:

- Core API: `users`, `projects`, `project_memberships`, `monitoring_sources`, `incidents`, `incident_timeline`, `resolution_notes`, `audit_logs`, `knowledge_base`
- Alert Ingestion: `alert_raw_alerts`, `alert_normalized_alerts`, `alert_ingestion_logs`
- AI Analysis: `analysis_alerts`, `analysis_correlation_groups`, `analysis_results`, `analysis_logs`
- Notification: `notification_records`, `notification_delivery_attempts`, `notification_templates`

## Locked Tech Stack

Backend:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- httpx
- JWT authentication for local development
- `passlib[bcrypt]` for password hashing
- `python-jose` for JWT

Frontend:

- React
- Vite
- React Router
- Axios
- Simple maintainable CSS
- No Redux
- No heavy UI libraries unless absolutely necessary

Containerization and routing:

- Docker
- Docker Compose
- Nginx reverse proxy

AI:

- Microsoft Foundry / Azure AI Foundry direction
- No mock AI output
- No fake RCA or fix generation
- If AI config is missing or AI call fails, fail gracefully without crashing the pipeline

## Alert Source

Phase 1 supports Prometheus Alertmanager webhook notifications only.

Do not add Grafana alert webhooks, Azure Monitor webhooks, Datadog, New Relic, Splunk, Elastic, Sentry, PagerDuty, AWS CloudWatch, Google Cloud Monitoring, Dynatrace, AppDynamics, Zabbix, or Nagios.

OpsGPT does not scrape dashboards, query the Prometheus metrics API, or connect to Grafana dashboards in Phase 1.

## Correct Flow

Kubernetes workloads emit metrics. Prometheus scrapes metrics and evaluates alert rules. Alertmanager sends fired or resolved webhook notifications to OpsGPT. The Alert Ingestion Service parses and normalizes alerts. The AI Analysis Service correlates alerts and creates incidents through the Core API Service. The Core API Service stores incidents and exposes APIs. The Frontend Service displays project incidents. The Notification Service sends console or Slack notifications.

## Project Workflow

Admins create projects, create Prometheus Alertmanager monitoring sources, receive project-specific webhook paths, and assign members.

Webhook path:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

Full Nginx URL:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

Engineers log in, select an assigned project, view dashboards and incidents, and open incident details.

## RBAC

Roles:

- `junior_engineer`
- `senior_engineer`
- `admin`

Junior engineers can view assigned projects, dashboards, incidents, AI summaries, RCA, fix recommendations, and knowledge base entries if present. They cannot update incidents, resolve incidents, add resolution notes, manage projects, manage monitoring sources, or assign members.

Senior engineers can do all junior actions. They can update incident status, resolve incidents, and add resolution notes. They cannot manage projects, monitoring sources, or project members.

Admins can manage projects, create/update/deactivate Prometheus Alertmanager monitoring sources, assign/remove project members, view all projects, update/resolve incidents, and add resolution notes.

## Authentication

Use local JWT authentication for Phase 1.

Seed users:

- `junior.engineer@company.com` / `password123` / `junior_engineer`
- `senior.engineer@company.com` / `password123` / `senior_engineer`
- `admin@company.com` / `password123` / `admin`

JWT settings:

- `JWT_SECRET_KEY`
- `JWT_ALGORITHM=HS256`
- `JWT_EXPIRE_MINUTES=60`

Protected routes require an `Authorization: Bearer <token>` header.

## Nginx Routing

Nginx is the single entry point:

- `/` -> `frontend-service:3000`
- `/api/core/` -> `core-api-service:8001/`
- `/api/alerts/` -> `alert-ingestion-service:8002/`
- `/api/analysis/` -> `ai-analysis-service:8003/`
- `/api/notifications/` -> `notification-service:8004/`
- `/alerts/webhook/` -> `alert-ingestion-service:8002/alerts/webhook/`

For Phase 1, CORS allows all origins and does not use credentials.

## UI Theme

Use a professional teal / teal-blue / white / dark slate theme.

- Primary teal: `#0F766E`
- Teal hover: `#115E59`
- Teal blue accent: `#0891B2`
- Dark slate text: `#0F172A`
- Muted text: `#64748B`
- Background: `#F8FAFC`
- Surface: `#FFFFFF`
- Border: `#E2E8F0`
- Success: `#059669`
- Warning: `#D97706`
- Danger: `#DC2626`

## Stability Rules

All backend services must expose `GET /health`, use CORS with `allow_origins=["*"]` and `allow_credentials=False`, handle database sessions safely, log controlled errors, and avoid exposing secrets in logs.

Core API must bootstrap the database inside the Docker container before Uvicorn starts. The bootstrap creates Core API tables and enforces the three default local users so existing Phase 1 Docker volumes with stale credentials are repaired on rebuild.

Alert Ingestion must not crash on unexpected Alertmanager payloads, missing optional labels, or AI Analysis unavailability. Missing or empty `alerts[]` should return a controlled 422 response.

AI Analysis must not crash on missing Foundry config, AI failure, Core API unavailability, or null optional fields. If AI fails after correlation succeeds, create the incident when possible and mark analysis failed without fake AI output.

Frontend must tolerate null AI fields, empty arrays, and API errors with friendly empty/error states.

Notification Service must not crash if Slack URL is missing while console mode is selected.

## Things Not To Add Unless Explicitly Requested

- Azure deployment infrastructure
- Kubernetes manifests
- Terraform
- Helm
- Azure Service Bus
- Microsoft Entra ID
- Additional alert vendors
- Extra microservices
- Redux or complex frontend state management
- Fake AI output

## Last Updated

- 2026-06-18: Initial Phase 1 context created from the pasted requirements, including the shared PostgreSQL database override.
- 2026-06-19: Confirmed Docker remains the target runtime; added Core API container database bootstrap requirement for table creation and default user seeding.
