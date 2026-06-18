# OpsGPT Codex Context

This file is the **source-of-truth context** for Codex while working on the OpsGPT project.

Codex must read and follow this file before making any code changes.

---

# 1. Project Identity

## Project Name

**OpsGPT - AI First Responder for Production Incidents**

## Project Purpose

OpsGPT is an internal incident management and response platform for DevOps, SRE, Cloud Engineering, and Operations teams.

The application helps teams:

- Receive monitoring alerts.
- Reduce alert noise.
- Correlate related alerts.
- Create incidents.
- Generate AI incident summaries.
- Generate root cause analysis.
- Suggest remediation steps.
- Notify engineering teams.
- Preserve incident knowledge for future use.

OpsGPT is not a generic SaaS product. It is an organization-internal operations platform.

---

# 2. Current Development Phase

## Phase 1 Scope

This phase is for **local application development and testing only**.

Allowed in Phase 1:

- Python + FastAPI backend services.
- Basic but polished React frontend.
- PostgreSQL databases.
- Dockerfiles.
- Docker Compose.
- `.env` based configuration.
- Nginx for reverse proxy / routing for local/VM testing.
- Local/manual alert testing.
- Webhook-based alert ingestion.
- Microsoft Foundry / Azure AI Foundry configuration for AI workloads.

Not allowed in Phase 1 unless the user explicitly asks:

- Azure cloud deployment.
- Kubernetes.
- Terraform.
- Azure Service Bus implementation.
- Azure App Service deployment.
- Azure Container Apps deployment.
- Microsoft Entra ID login implementation.
- Production-grade secrets management.
- Production CORS restrictions.
- Complex distributed tracing.
- Extra microservices.
- Rewriting the full project from scratch.

---

# 3. Architecture Style

OpsGPT uses a **lightweight event-driven microservices architecture**.

Do not convert the project into a monolith.

Do not create more than the planned services unless the user explicitly asks.

## Accepted Services

1. `frontend-service`
2. `core-api-service`
3. `alert-ingestion-service`
4. `ai-analysis-service`
5. `notification-service`

## Supporting Infrastructure

- `nginx` reverse proxy / routing for local/VM access.
- PostgreSQL database containers.
- Docker Compose network and volumes.

Nginx is not considered an application microservice. It is only an infrastructure/reverse-proxy / routing component.

---

# 4. High-Level Workflow

```text
Monitoring System / Manual Alert
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

Correct alerting model:

```text
Grafana / Azure Monitor / Other Monitoring Tools continuously monitor systems.
When alert rules are triggered, they send webhook payloads to OpsGPT.
OpsGPT receives those triggered payloads and processes them.
```

Incorrect model:

```text
OpsGPT scrapes Grafana dashboards.
OpsGPT scrapes Azure Monitor dashboards.
OpsGPT continuously polls dashboards for alerts.
```

OpsGPT must **not** scrape dashboards.

---

# 5. Service Responsibilities

## 5.1 Frontend Service

Technology:

- React
- Vite
- React Router
- Axios
- Clean CSS or lightweight existing CSS setup

Responsibilities:

- Login page.
- Project selection page.
- Project dashboard page.
- Project incident list page.
- Project incident detail page.
- Knowledge base page.
- Profile page.
- Admin project management page.
- Admin monitoring source management page.
- Admin project member assignment UI.
- Role-based UI controls.
- Clean, modern, maintainable UI.

Important UI expectations:

- UI should look professional, not like a plain static HTML page.
- Keep it simple and maintainable.
- Use reusable components.
- Use API wrapper files.
- Use protected routes.
- Use role utility functions.
- Use centralized route/constant helpers.
- Add back navigation buttons wherever needed.
- Sidebar active selection must highlight only the correct tab.
- Admin member assignment must support searching users by name/email/role.

Frontend must mainly communicate with:

```text
Core API Service
```

Frontend must not directly perform:

- Alert parsing.
- Alert correlation.
- AI summary generation.
- RCA generation.
- Notification sending.

---

## 5.2 Core API Service

Technology:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT auth for Phase 1
- RBAC dependencies

Responsibilities:

- Authentication.
- User profile.
- RBAC.
- User management.
- Project management.
- Project member management.
- Monitoring source metadata management.
- Incident management.
- Dashboard APIs.
- Incident status updates.
- Resolution notes.
- Audit logs.
- Knowledge base.
- Internal APIs used by AI Analysis Service.
- Optional notification trigger to Notification Service.

Core API owns the main user-facing business data.

Core API must not:

- Receive raw Grafana/Azure/custom alert payloads.
- Parse monitoring payloads.
- Generate AI summary/RCA/fix recommendations.
- Send Slack messages directly.
- Directly perform monitoring integrations.

---

## 5.3 Alert Ingestion Service

Technology:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- HTTP client for forwarding to AI Analysis

Responsibilities:

- Receive webhook alerts.
- Receive manual alert submissions.
- Validate project webhook token.
- Store raw alert payloads.
- Parse alert payloads.
- Normalize alerts into OpsGPT internal alert schema.
- Store normalized alerts.
- Forward normalized alerts to AI Analysis Service when forwarding is enabled.

Alert Ingestion must not:

- Create incidents directly.
- Generate AI output.
- Generate RCA.
- Generate fix recommendations.
- Send notifications.
- Manage users/RBAC.

Important:

- Existing stable support must include:
  - Grafana
  - Azure Monitor
  - Manual alerts
  - Custom webhook fallback

Do not add many vendor-specific parser files unless the user explicitly asks for that exact task again.

If payloads are dynamic, prefer a controlled universal/custom parser fallback instead of creating a large incomplete vendor parser explosion.

---

## 5.4 AI Analysis Service

Technology:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- HTTP client
- Microsoft Foundry / Azure AI Foundry client configuration

Responsibilities:

- Receive normalized alerts.
- Detect duplicates.
- Correlate related alerts.
- Group alerts by project, service, environment, and time window.
- Create or update incidents through Core API internal APIs.
- Generate AI incident summary.
- Generate root cause analysis.
- Generate confidence score.
- Generate fix recommendations.
- Store analysis results and failures.

Current AI direction:

- Final target AI provider is **Microsoft Foundry / Azure AI Foundry**.
- Do not add mock AI output.
- Do not silently generate fake AI responses.
- Do not reintroduce Ollama/Gemini/OpenAI provider switching unless the user explicitly asks.
- If the Foundry AI call fails, the incident pipeline must not crash.

AI failure behavior:

- Incident creation should still succeed with basic deterministic incident data if correlation succeeds.
- AI-specific fields can be empty/null when AI fails.
- Store `analysis_status=failed`.
- Store a clear `error_message`.
- Add an analysis log entry.
- Frontend must show a clean message like:
  `AI analysis is not available yet` or `AI analysis failed`.

AI Analysis must not:

- Receive raw monitoring webhook payloads directly.
- Parse Grafana/Azure/custom source-specific schemas directly.
- Manage users/RBAC.
- Update incident status from frontend.
- Send Slack/notification messages.
- Directly write to Core API database.

---

## 5.5 Notification Service

Technology:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- HTTP client for Slack webhook

Responsibilities:

- Receive notification events from Core API.
- Format notification messages.
- Send console notifications in development.
- Send Slack notifications when configured.
- Store notification history.
- Store delivery attempts.
- Track delivery status.

Notification Service must not:

- Parse alerts.
- Correlate alerts.
- Generate AI output.
- Manage users/RBAC.
- Update incidents.

Default Phase 1 notification mode:

```env
NOTIFICATION_CHANNEL=console
```

Slack can be enabled with:

```env
NOTIFICATION_CHANNEL=slack
SLACK_WEBHOOK_URL=<webhook-url>
```

---

# 6. RBAC Rules

Do not change these rules unless the user explicitly asks.

## junior_engineer

Can:

- Login.
- View assigned projects.
- View project dashboard.
- View incidents.
- View AI summaries.
- View RCA reports.
- View knowledge base.

Cannot:

- Create projects.
- Manage monitoring sources.
- Assign project members.
- Update incident status.
- Resolve incidents.
- Add resolution notes.

## senior_engineer

Can:

- Perform all junior/read-only actions.
- View assigned projects.
- Update incident status for assigned projects.
- Resolve incidents for assigned projects.
- Add resolution notes for assigned projects.

Cannot:

- Create/delete projects.
- Manage monitoring sources.
- Assign project members.

## admin

Can:

- View all projects.
- Create/update/deactivate projects.
- Create/update/deactivate monitoring sources.
- Assign/remove project members.
- Perform all incident update/resolve actions.
- Add resolution notes.

---

# 7. Project-Based Feature

OpsGPT is project-based.

## Correct Admin Flow

```text
Admin logs in
→ Creates project
→ Adds monitoring source
→ OpsGPT generates project-specific webhook path/token
→ Admin configures that webhook URL in Grafana/Azure/custom monitoring system
→ Monitoring system sends alerts to OpsGPT
```

## Correct Engineer Flow

```text
Junior/Senior engineer logs in
→ Selects assigned project
→ Views project dashboard
→ Views project incidents
→ Senior can update/resolve incidents
→ Junior remains read-only
```

## Monitoring Source Metadata

Admins can store:

- Source type.
- Source name.
- Dashboard URL.
- Alert rule URL.
- Generated webhook token/path.
- Active/inactive flag.

Important:

- Dashboard URLs are metadata/reference links.
- OpsGPT should not scrape those dashboard URLs.
- Triggered alerts must arrive through webhooks.

Stable source types for current implementation:

- `grafana`
- `azure_monitor`
- `manual`
- `custom`

More observability tools can be added later, but do not implement broad vendor support unless explicitly requested.

---

# 8. Webhook Design

Recommended project webhook format:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

With Nginx reverse proxy:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

Alert Ingestion must validate:

- `project_id`
- `webhook_token`

Validation is done by calling Core API internal endpoint.

If validation fails:

- Return 401/403.
- Do not forward to AI Analysis.
- Do not create incidents.

---

# 9. Alert Payload Parsing Rules

Production alert payloads may be dynamic.

Do not overfit to one fixed schema.

Required approach:

1. Store raw payload exactly as received.
2. Use source-specific parser when the source is known.
3. Use universal/custom fallback parser for unknown/dynamic schemas.
4. Normalize into internal OpsGPT alert schema.
5. Do not reject alerts only because optional fields are missing.
6. Reject only if:
   - payload is empty,
   - payload is not JSON/object,
   - project webhook validation fails.

Minimum normalized alert fields should be best-effort:

- `alert_id`
- `project_id`
- `source`
- `source_type`
- `service_name`
- `alert_type`
- `severity`
- `message`
- `description`
- `environment`
- `metric_name`
- `metric_value`
- `threshold`
- `resource_id`
- `dashboard_url`
- `runbook_url`
- `fired_at`
- `status`

Safe defaults:

- Generate `alert_id` if missing.
- Use `unknown-service` if service cannot be found.
- Use `informational` if severity cannot be found.
- Use `custom` if alert type cannot be inferred.
- Use `production` as default environment unless configured otherwise.
- Use a clear generic message if no message exists.

Do not create a large number of incomplete vendor-specific parser files unless asked.

---

# 10. AI Analysis Rules

Correlation should be deterministic and explainable.

Group alerts by:

- `project_id`
- `service_name`
- `environment`
- correlation time window

Do not correlate alerts across different projects.

Severity decision:

- Any critical alert -> incident severity critical.
- Else any warning alert -> warning.
- Else informational.

Incident creation:

- If one critical alert arrives, create incident.
- If multiple related warning/informational alerts arrive in the correlation window, group them.
- Use deterministic incident title first.
- AI can improve explanation, but incident creation should not depend entirely on AI success.

AI prompt should include:

- project_id
- service_name
- alert_type
- severity
- message
- description
- metric_name
- metric_value
- threshold
- environment
- labels/annotations if available
- related alerts
- parsing confidence if implemented

AI must return structured JSON when possible.

If AI response is invalid:

- Store failure cleanly.
- Do not crash the service.
- Do not fake a response.

---

# 11. Nginx Reverse Proxy

Nginx is used for local/VM testing and to reduce CORS problems.

Recommended access:

```text
http://<VM_IP>:8080
```

Routes:

```text
/                           -> frontend-service:3000
/api/core/                  -> core-api-service:8001
/api/alerts/                -> alert-ingestion-service:8002
/api/analysis/              -> ai-analysis-service:8003
/api/notifications/         -> notification-service:8004
/alerts/webhook/            -> alert-ingestion-service:8002/alerts/webhook/
```

Frontend environment in Nginx mode:

```env
VITE_CORE_API_URL=/api/core
```

Admin monitoring source page should display webhook URL using:

```javascript
window.location.origin + webhook_path
```

Do not hardcode localhost.

---

# 12. CORS Rules for Phase 1

For Phase 1 development only:

FastAPI services may use permissive CORS:

```python
allow_origins=["*"]
allow_credentials=False
allow_methods=["*"]
allow_headers=["*"]
```

Nginx may also allow CORS for development.

Do not set:

```python
allow_credentials=True
```

when using wildcard origins.

Production note:

- CORS must be restricted to trusted domains in later phases.

---

# 13. Documentation Rules

Every meaningful feature/change must update relevant docs.

Docs to keep updated:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/MICROSERVICES.md`
- `docs/LOCAL_DEVELOPMENT.md`
- `docs/DEVELOPMENT_RUN_GUIDE.md`
- `docs/API_OVERVIEW.md`
- `nginx/README.md` if Nginx behavior changes

Documentation must not claim unsupported features are complete.

Documentation must clearly say:

- Phase 1 is local development.
- OpsGPT receives alerts through webhooks.
- OpsGPT does not scrape dashboards.
- Project-specific webhook URLs are generated by OpsGPT.
- AI provider target is Microsoft Foundry / Azure AI Foundry.
- Nginx reverse proxy is used for local/VM testing.

---

# 14. Codex Operating Rules

Codex must follow these rules for every task.

## General

- Make minimal targeted changes.
- Do not rewrite the full application.
- Do not change architecture unless explicitly asked.
- Do not add new microservices.
- Do not add unrelated features.
- Do not invent requirements.
- Do not remove accepted features.
- Do not change RBAC.
- Do not add cloud deployment code unless explicitly asked.
- Do not add Kubernetes/Terraform unless explicitly asked.
- Do not introduce heavy UI libraries unless explicitly approved.
- Do not hardcode secrets.
- Use `.env` and `.env.example`.

## Execution

Unless the user explicitly asks, do not run:

- tests
- docker compose
- npm install
- npm build
- pip install
- curl commands
- database migrations
- verification commands

Just create/update code files and explain what changed.

## If Requirements Are Ambiguous

Stop and ask for clarification.

Do not guess.

## After Every Task

Codex should explain only:

1. Files created/modified.
2. What changed.
3. Any assumptions made.
4. Any TODOs or risks.

Do not continue to the next feature automatically.

---

# 15. Current Accepted Feature Set

The current accepted feature set is:

1. Authentication and user profile.
2. RBAC.
3. Project-based workflow.
4. Admin project management.
5. Admin monitoring source management.
6. Admin project member assignment with search.
7. Project-specific webhook URLs/tokens.
8. Alert ingestion for Grafana/Azure/manual/custom webhooks.
9. Dynamic/best-effort payload parsing with raw payload storage.
10. Alert correlation.
11. AI incident summary.
12. Root cause analysis.
13. Fix recommendation.
14. Incident dashboard.
15. Incident detail page.
16. Incident timeline.
17. Resolution notes.
18. Knowledge base.
19. Similar incident search.
20. Notification service with console/Slack mode.
21. Nginx reverse proxy for local/VM testing.
22. Improved React UI with reusable components.

---

# 16. Current Non-Goals

Do not implement these unless explicitly requested:

- Full Azure deployment.
- Azure Service Bus.
- Microsoft Entra ID authentication.
- Kubernetes manifests.
- Terraform.
- Real production Grafana setup automation.
- Real Azure Monitor alert rule automation.
- Dashboard scraping.
- Dozens of vendor-specific parser implementations.
- Complex RAG/vector database.
- Automated runbook execution.
- Multi-tenant SaaS billing or customer management.
- Advanced notification preference system.
- Production security hardening.

---

# 17. Stable Local URLs

With direct service access:

```text
Frontend:              http://localhost:3000
Core API:              http://localhost:8001
Alert Ingestion API:   http://localhost:8002
AI Analysis API:       http://localhost:8003
Notification API:      http://localhost:8004
```

With Nginx reverse proxy:

```text
Frontend:              http://<VM_IP>:8080
Core API:              http://<VM_IP>:8080/api/core
Alert Ingestion API:   http://<VM_IP>:8080/api/alerts
AI Analysis API:       http://<VM_IP>:8080/api/analysis
Notification API:      http://<VM_IP>:8080/api/notifications
Project Webhook:       http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

---

# 18. Environment Defaults

Use safe development defaults.

Core API:

```env
ENABLE_NOTIFICATIONS=false
INTERNAL_API_KEY=change-me-internal-key
```

Alert Ingestion:

```env
ENABLE_ANALYSIS_FORWARDING=false
CORE_API_URL=http://core-api-service:8001
AI_ANALYSIS_SERVICE_URL=http://ai-analysis-service:8003
INTERNAL_API_KEY=change-me-internal-key
```

AI Analysis:

```env
AI_PROVIDER=foundry
FOUNDRY_ENDPOINT=
FOUNDRY_API_KEY=
FOUNDRY_MODEL_DEPLOYMENT=
FOUNDRY_API_VERSION=2024-02-15-preview
CORE_API_URL=http://core-api-service:8001
INTERNAL_API_KEY=change-me-internal-key
```

Notification:

```env
NOTIFICATION_CHANNEL=console
```

Frontend with Nginx:

```env
VITE_CORE_API_URL=/api/core
```

---

# 19. Recovery Rule If Codex Gets Confused

If Codex finds conflicting code, docs, or requirements:

1. Follow this `CONTEXT.md`.
2. Preserve the accepted architecture.
3. Make the smallest fix.
4. Do not invent a new design.
5. Ask the user before making broad changes.

This file has higher priority than old generated README content if the old README conflicts with it.
