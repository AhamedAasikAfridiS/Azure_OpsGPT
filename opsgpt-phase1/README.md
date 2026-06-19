# OpsGPT - AI First Responder for Production Incidents

Prometheus Alertmanager driven AI incident management platform for DevOps, SRE, Cloud Engineering, and Operations teams.

## 2. Project Overview

OpsGPT is an internal incident management and first-responder platform for production operations teams. It receives alerts from Prometheus Alertmanager, normalizes the incoming alert data, correlates related alerts into incidents, and uses Microsoft Foundry / Azure AI Foundry direction to generate an AI-assisted incident summary, root cause analysis, confidence score, supporting evidence, and recommended fix.

Phase 1 is focused on local application development. It runs as a Docker Compose based microservices application with a React frontend, FastAPI backend services, Nginx reverse proxy, and one shared PostgreSQL database.

At a high level, OpsGPT:

- Receives alert notifications from Prometheus Alertmanager.
- Validates project-specific webhook URLs.
- Stores raw and normalized alert data.
- Correlates alerts into project-specific incidents.
- Generates AI-assisted analysis when Microsoft Foundry / Azure AI Foundry is configured.
- Displays dashboards, incident lists, and incident details in the frontend.
- Allows engineers to resolve incidents according to RBAC permissions.
- Sends console or Slack notifications depending on configuration.

## 3. Problem Statement

Production operations teams often face several repeating problems:

- Alert fatigue from too many noisy alerts.
- Duplicate alerts for the same underlying failure.
- Slow incident triage because engineers must manually inspect many fields.
- Manual root cause analysis during high-pressure incidents.
- Delayed identification of possible fixes.
- Lack of centralized incident history and knowledge.
- Higher MTTR because useful context is scattered across monitoring tools, chat, and engineer memory.

OpsGPT exists to reduce the time between receiving an alert and understanding what should be done next.

## 4. Proposed Solution

OpsGPT solves these problems through a project-based incident workflow:

- Admins create projects that represent applications, platforms, or operational domains.
- Admins configure Prometheus Alertmanager monitoring sources per project.
- Core API generates a project-specific webhook path and token.
- Prometheus Alertmanager sends alerts to that webhook URL.
- Alert Ingestion validates, stores, and normalizes the alerts.
- AI Analysis correlates related alerts and creates or updates incidents.
- Microsoft Foundry / Azure AI Foundry can generate summaries, RCA, evidence, confidence, and recommended fixes.
- Core API exposes incidents, dashboards, membership, RBAC, and resolution workflows.
- Frontend shows each user only the projects and actions allowed by their role.
- Notification Service sends console or Slack delivery events.
- Historical incidents and knowledge base entries help teams learn from previous failures.

## 5. Phase 1 Scope

### Included

- Local Docker Compose setup.
- Nginx reverse proxy.
- React + Vite frontend.
- FastAPI backend microservices.
- Shared PostgreSQL database.
- Prometheus Alertmanager webhook ingestion.
- Project creation.
- Monitoring source setup.
- Project member assignment.
- Incident management.
- Microsoft Foundry / Azure AI Foundry integration direction.
- Console and Slack notification support.

### Not Included In Phase 1

- Azure deployment.
- AKS deployment.
- Azure Service Bus.
- Terraform.
- Kubernetes manifests.
- Microsoft Entra ID.
- Azure Monitor integration.
- Grafana integration.
- Datadog, Splunk, New Relic, or other monitoring integrations.
- Multi-cloud monitoring integrations.
- Production security hardening.

Phase 1 alert ingestion is only Prometheus Alertmanager webhook based.

## 6. High-Level Architecture

User application flow:

```text
Users
  |
Browser
  |
Nginx Reverse Proxy
  |
Frontend Service
  |
Core API Service
  |
Shared PostgreSQL Database
```

Prometheus Alertmanager flow:

```text
Kubernetes Workloads
  |
Prometheus
  |
Alertmanager
  |
Nginx Webhook Route
  |
Alert Ingestion Service
  |
AI Analysis Service
  |
Core API Service
  |
Notification Service
```

Key points:

- Users access the application through Nginx.
- Alertmanager sends webhook alerts to Nginx.
- Nginx routes alert webhook traffic to Alert Ingestion.
- The frontend mainly talks to Core API through `/api/core`.
- Backend services communicate internally through REST APIs in Phase 1.
- PostgreSQL is shared in Phase 1, while each backend service owns its logical data area.

## 7. Architecture Diagram Reference

An architecture diagram can be generated as:

```text
app_.png
```

The diagram should show:

- Users.
- Nginx reverse proxy.
- Frontend Service.
- Core API Service.
- Alert Ingestion Service.
- AI Analysis Service.
- Notification Service.
- Shared PostgreSQL database.
- Prometheus Alertmanager flow.
- Microsoft Foundry / Azure AI Foundry integration.
- Future Azure mapping candidates.

This README does not claim that `app_.png` already exists. It describes what the diagram should contain when generated.

## 8. Microservices Overview

| Service | Tech | Port | Main Purpose | Talks To |
| ------- | ---- | ---- | ------------ | -------- |
| `frontend-service` | React + Vite | 3000 | User interface | Core API through `/api/core` |
| `core-api-service` | FastAPI | 8001 | Auth, RBAC, projects, incidents, dashboard, knowledge base | DB, Notification Service, AI Analysis internal calls |
| `alert-ingestion-service` | FastAPI | 8002 | Receives Prometheus Alertmanager webhooks and normalizes alerts | Core API for token validation, AI Analysis, DB |
| `ai-analysis-service` | FastAPI | 8003 | Correlates alerts, creates incidents, calls Microsoft Foundry for AI | Core API, Microsoft Foundry, DB |
| `notification-service` | FastAPI | 8004 | Sends console or Slack notifications | DB |
| `nginx` | Nginx | 8080 | Single entry point and routing | All services |
| `opsgpt-db` | PostgreSQL | internal | Shared Phase 1 database | Backend services |

## 9. Microservice Business Logic In Detail

### 9.1 Frontend Service

The frontend service is the browser-facing React application.

Responsibilities:

- Login.
- Project selection.
- Project dashboard.
- Incidents list.
- Incident detail.
- Admin projects.
- Monitoring source setup.
- Member assignment.
- Profile.
- RBAC-based UI controls.

Business logic:

- Stores the JWT token used for authenticated Core API calls.
- Calls Core API for normal frontend workflows.
- Displays role-based actions.
- Hides admin-only navigation from non-admin users.
- Hides incident edit and resolution controls from junior engineers.
- Shows incident AI fields when available.
- Shows a graceful fallback when AI analysis is missing or failed.

The frontend does not:

- Perform AI analysis.
- Receive alerts directly.
- Send notifications directly.
- Call Alert Ingestion, AI Analysis, or Notification Service during normal user workflows.

Frontend API base:

```env
VITE_CORE_API_URL=/api/core
```

### 9.2 Core API Service

The Core API service owns the primary user-facing application API.

Responsibilities:

- Authentication.
- JWT generation.
- RBAC.
- Project management.
- Project membership.
- Monitoring source metadata.
- Webhook token generation.
- Incident storage.
- Dashboard APIs.
- Incident status updates.
- Resolution notes.
- Audit logs.
- Knowledge base.
- Internal APIs used by other backend services.

Business logic:

- Admin creates projects.
- Admin creates Prometheus Alertmanager monitoring sources.
- Core API generates webhook tokens and project webhook paths.
- Admin assigns users to projects.
- Users see only assigned projects unless their role allows broader access.
- Junior engineers are read-only for incident resolution workflows.
- Senior engineers and admins can update incident status and add resolution notes.
- Project-specific dashboards and incident pages are backed by Core API.

Important logical tables include:

- `users`
- `projects`
- `project_memberships`
- `monitoring_sources`
- `incidents`
- `incident_timeline`
- `resolution_notes`
- `audit_logs`
- `knowledge_base`

### 9.3 Alert Ingestion Service

The Alert Ingestion service is the only Phase 1 alert receiver.

Responsibilities:

- Receives Prometheus Alertmanager webhook payloads.
- Validates the project webhook token with Core API.
- Stores the raw payload.
- Parses the Alertmanager `alerts[]` array.
- Normalizes each alert into a consistent internal shape.
- Stores normalized alerts.
- Forwards normalized alerts to AI Analysis.

Business logic:

- One Alertmanager webhook payload can contain multiple alerts.
- Each alert in `alerts[]` becomes one normalized alert record.
- The project is identified through the project-specific webhook URL.
- Invalid project IDs or webhook tokens should not create alerts.
- Alert Ingestion does not create incidents.
- Alert Ingestion does not generate AI analysis.

Normalized fields include:

- `alert_id`
- `project_id`
- `source_type`
- `service_name`
- `alert_name`
- `alert_type`
- `severity`
- `message`
- `namespace`
- `cluster`
- `pod`
- `deployment`
- `labels`
- `annotations`
- `raw_alert`

### 9.4 AI Analysis Service

The AI Analysis service owns correlation and AI-assisted incident analysis.

Responsibilities:

- Receives normalized alerts.
- Stores analysis input.
- Detects duplicates.
- Correlates related alerts.
- Creates incidents through Core API.
- Calls Microsoft Foundry / Azure AI Foundry for AI analysis when configured.
- Updates Core API with AI summary, RCA, evidence, confidence, and recommended fix.
- Handles AI failure gracefully.

Business logic:

- Correlation is based on fields such as `project_id`, `service_name`, `namespace`, `cluster`, `environment`, and a time window.
- Critical alerts should create incidents quickly.
- Related alerts can be grouped into one incident.
- AI failure should not block incident creation.
- If AI analysis fails, the incident still exists but AI fields may be empty or marked failed.
- The frontend should display: `AI analysis is not available for this incident yet.` when AI fields are unavailable.

AI outputs include:

- Incident summary.
- Root cause.
- Supporting evidence.
- Confidence score.
- Recommended fix.

### 9.5 Notification Service

The Notification Service owns notification delivery.

Responsibilities:

- Receives notification events.
- Sends console notifications.
- Sends Slack notifications when configured.
- Stores notification history.
- Stores delivery attempts.

Business logic:

- Default mode is console.
- Slack works only if a Slack webhook URL is configured.
- Missing Slack configuration should not break console mode.
- Notification delivery should be tracked for troubleshooting.

## 10. Nginx Routing

Nginx is the single entry point for the Phase 1 local application.

| External Path | Internal Target |
| ------------- | --------------- |
| `/` | `frontend-service:3000` |
| `/api/core/` | `core-api-service:8001` |
| `/api/alerts/` | `alert-ingestion-service:8002` |
| `/api/analysis/` | `ai-analysis-service:8003` |
| `/api/notifications/` | `notification-service:8004` |
| `/alerts/webhook/` | `alert-ingestion-service:8002/alerts/webhook/` |

Main app URL:

```text
http://<VM_IP>:8080
```

Project webhook URL:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

CORS is open for Phase 1 development only. Production deployment should restrict allowed origins.

## 11. Prometheus Alertmanager Integration

Prometheus Alertmanager is the only supported alert source in Phase 1.

Flow:

1. Kubernetes workloads expose metrics.
2. Prometheus scrapes metrics.
3. Prometheus evaluates alert rules.
4. Prometheus sends matching alert events to Alertmanager.
5. Alertmanager sends webhook payloads to OpsGPT.
6. OpsGPT receives fired and resolved alert notifications through Alert Ingestion.

Alertmanager receiver example:

```yaml
receivers:
  - name: opsgpt-webhook
    webhook_configs:
      - url: 'http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}'
        send_resolved: true
```

Important Phase 1 boundaries:

- OpsGPT does not query the Prometheus API in Phase 1.
- OpsGPT does not scrape dashboards.
- OpsGPT does not support Grafana, Azure Monitor, Datadog, Splunk, New Relic, or other alert sources in Phase 1.

## 12. Alertmanager Payload Example

Example payload:

```json
{
  "receiver": "opsgpt-webhook",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "HighCPUUsage",
        "severity": "critical",
        "service": "payment-api",
        "namespace": "payments",
        "cluster": "aks-prod-01",
        "pod": "payment-api-7d94c8f9bd-vx2qk",
        "deployment": "payment-api",
        "environment": "production"
      },
      "annotations": {
        "summary": "Payment API CPU usage is above 90%",
        "description": "CPU usage for payment-api has been above 90% for 5 minutes."
      },
      "startsAt": "2026-06-19T10:15:00Z",
      "endsAt": "0001-01-01T00:00:00Z",
      "generatorURL": "http://prometheus.example.local/graph?g0.expr=cpu",
      "fingerprint": "7f3c2c8f9a1b"
    }
  ],
  "commonLabels": {
    "alertname": "HighCPUUsage",
    "severity": "critical",
    "service": "payment-api"
  },
  "commonAnnotations": {
    "summary": "Payment API CPU usage is above 90%"
  },
  "externalURL": "http://alertmanager.example.local"
}
```

OpsGPT stores the raw payload and also creates normalized alert records from each object inside `alerts[]`.

## 13. Normalized Alert Format

Example normalized alert:

```json
{
  "alert_id": "7f3c2c8f9a1b",
  "project_id": 1,
  "source_type": "prometheus_alertmanager",
  "service_name": "payment-api",
  "alert_name": "HighCPUUsage",
  "alert_type": "resource",
  "severity": "critical",
  "message": "Payment API CPU usage is above 90%",
  "namespace": "payments",
  "cluster": "aks-prod-01",
  "pod": "payment-api-7d94c8f9bd-vx2qk",
  "deployment": "payment-api",
  "labels": {
    "alertname": "HighCPUUsage",
    "severity": "critical",
    "service": "payment-api",
    "environment": "production"
  },
  "annotations": {
    "summary": "Payment API CPU usage is above 90%",
    "description": "CPU usage for payment-api has been above 90% for 5 minutes."
  },
  "raw_alert": {
    "status": "firing",
    "fingerprint": "7f3c2c8f9a1b"
  }
}
```

Normalization is needed because Alertmanager payloads can contain many flexible labels and annotations. OpsGPT needs a consistent internal format so correlation, incident creation, AI prompts, dashboards, and future reporting do not depend directly on raw Alertmanager payload shape.

## 14. End-to-End Scenario - High Level

Scenario: Payment API in Kubernetes has high CPU and memory pressure.

1. Prometheus detects CPU usage above 90%.
2. Prometheus sends the alert to Alertmanager.
3. Alertmanager sends the webhook payload to OpsGPT.
4. Alert Ingestion validates the project webhook token.
5. Alert Ingestion stores and normalizes the alert.
6. AI Analysis correlates the alert and creates an incident.
7. Microsoft Foundry / Azure AI Foundry generates summary, RCA, and fix recommendation if configured.
8. Core API stores the incident and related fields.
9. Frontend shows the incident under the selected project.
10. A senior engineer resolves the incident and adds resolution notes.
11. Notification Service sends an update through console or Slack.

## 15. End-to-End Scenario - In Depth

Project:

```text
Payment Platform
```

Monitoring source:

```text
Prometheus Alertmanager
```

Example flow:

1. An admin creates the `Payment Platform` project in OpsGPT.
2. The admin creates a Prometheus Alertmanager monitoring source for the project.
3. Core API generates a webhook path and token for that project.
4. The generated URL is configured in Alertmanager.
5. A Kubernetes workload named `payment-api` starts consuming too much CPU.
6. Prometheus evaluates an alert rule and marks `HighCPUUsage` as firing.
7. Alertmanager sends a webhook payload to:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

8. Nginx routes `/alerts/webhook/` traffic to Alert Ingestion.
9. Alert Ingestion validates the project and token using Core API.
10. Alert Ingestion stores the raw payload.
11. Alert Ingestion extracts each item from `alerts[]`.
12. Alert Ingestion normalizes fields such as service, namespace, cluster, severity, message, labels, and annotations.
13. Alert Ingestion forwards the normalized alert to AI Analysis.
14. AI Analysis checks whether the alert is a duplicate or related to an existing incident.
15. AI Analysis creates a new incident through Core API when needed.
16. AI Analysis calls Microsoft Foundry / Azure AI Foundry when configured.
17. AI Analysis updates the incident with summary, RCA, evidence, confidence score, and recommended fix.
18. Notification Service sends a console or Slack notification.
19. Engineers open the frontend and select `Payment Platform`.
20. Junior engineers can view the incident.
21. Senior engineers and admins can update the status and add resolution notes.
22. The incident history remains available for future reference.

## 16. Project-Based Webhook System

OpsGPT routes alerts by project. Each project can have a Prometheus Alertmanager monitoring source. When the source is created, Core API generates a webhook path and token.

Webhook format:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

Full URL format:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

Why this matters:

- Alertmanager does not need a frontend login session.
- Each project has its own webhook identity.
- Alert Ingestion can map incoming alerts to the correct project.
- Invalid or stale tokens can be rejected.
- Future production architecture can add stronger gateway validation if required.

## 17. Incident Lifecycle

Typical incident lifecycle:

1. Alertmanager sends one or more alerts to the project webhook.
2. Alert Ingestion stores raw and normalized alert data.
3. AI Analysis correlates the alert with existing incidents.
4. AI Analysis creates a new incident or groups the alert with a related incident.
5. Core API stores incident state.
6. Frontend displays the incident in dashboard and incident list views.
7. AI fields are displayed when available.
8. Notifications are delivered.
9. Senior/admin users update status and resolution notes.
10. Incident data remains available as operational history.

Possible incident statuses depend on the frontend and Core API implementation, but the important Phase 1 concept is that junior users are read-only while senior/admin users can perform resolution actions.

## 18. RBAC Model

OpsGPT uses local JWT authentication and role-based access control in Phase 1.

Roles:

| Role | Purpose |
| ---- | ------- |
| Admin | Manages projects, monitoring sources, memberships, and can resolve incidents |
| Senior | Works assigned incidents and can update or resolve incidents |
| Junior | Views assigned projects and incidents in read-only mode |

RBAC behavior:

- Admin-only navigation appears only for admin users.
- Project access is based on memberships.
- Junior engineers can view incidents but should not see edit or resolution controls.
- Senior and admin users can update incident status and add resolution notes.
- Frontend hides disallowed actions, while backend APIs should still enforce permissions.

## 19. Shared Database

Phase 1 uses one shared PostgreSQL database:

```text
Container/service: opsgpt-db
Database name: opsgpt_db
```

All backend services use the same database, but each service owns its logical tables.

This is a Phase 1 simplicity decision. OpsGPT remains a microservices application at the service and application level because each backend service has separate runtime boundaries and responsibilities.

Future production architecture can split databases per service if stronger isolation, independent scaling, or service ownership boundaries are required.

## 20. Microsoft Foundry / Azure AI Foundry Workflow

Microsoft Foundry / Azure AI Foundry is the first cloud integration for incident analysis and is used only by `ai-analysis-service`.

Expected AI workflow:

1. AI Analysis receives normalized alert context.
2. AI Analysis builds an incident-analysis request.
3. AI Analysis sends the request to Microsoft Foundry / Azure AI Foundry when configured.
4. The AI response is parsed into structured incident fields.
5. Core API stores the AI-generated output.
6. Frontend displays AI summary, RCA, supporting evidence, confidence score, and recommended fix.

If AI is not configured or the AI call fails:

- Incident creation should still succeed.
- AI Analysis records `analysis_status=failed` and a controlled error message; AI fields remain empty.
- The frontend should clearly show that AI analysis is not available yet.

AI should assist responders, not replace human judgment. Senior/admin users remain responsible for final resolution decisions.

## 21. Notification Workflow

Notification Service supports console and Slack delivery behavior.

Phase 1 behavior:

- Console notification is the default.
- Slack notification works when a Slack webhook URL is configured.
- Missing Slack configuration should not break the application.
- Notification history and delivery attempts help with troubleshooting.

Notification Service does not own incident business rules. It receives notification events and handles delivery.

## 22. Future Azure Deployment Planning Notes

This README is intended to help plan future Azure infrastructure. Phase 1 does not include Azure deployment files, Terraform, Kubernetes manifests, or production hardening.

Possible future Azure mapping candidates:

| Phase 1 Component | Future Azure Candidate |
| ----------------- | ---------------------- |
| Nginx reverse proxy | Azure Application Gateway, Azure Container Apps ingress, or AKS ingress |
| Frontend Service | Azure Static Web Apps, App Service, Container Apps, or AKS |
| FastAPI services | Azure Container Apps, App Service for Containers, or AKS |
| PostgreSQL shared DB | Azure Database for PostgreSQL Flexible Server |
| Slack webhook secret | Azure Key Vault |
| Internal REST calls | Private networking or service discovery |
| AI Analysis Foundry calls | Azure AI Foundry / Microsoft Foundry |
| Logs and metrics | Azure Monitor and Log Analytics |
| Production async messaging | Azure Service Bus, if later required |
| Container images | Azure Container Registry |

Future deployment design should answer:

- Which service hosting model will run the five services?
- How will Nginx routing be replaced or preserved?
- Should the database remain shared or be split?
- How will secrets be stored and rotated?
- Which services need public ingress?
- Which services should be private only?
- How will Alertmanager reach the webhook URL?
- How will Foundry credentials be managed?
- How will logs, metrics, and audit events be retained?

## 23. Local Development URLs

Main app:

```text
http://localhost:8080
```

Core API through Nginx:

```text
http://localhost:8080/api/core
```

Alert webhook route through Nginx:

```text
http://localhost:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

For a VM-based local-style deployment, replace `localhost` with the VM IP or DNS name:

```text
http://<VM_IP>:8080
```

## 24. Important Phase 1 Boundaries

- Alert source is only Prometheus Alertmanager webhook.
- Frontend normal workflow should call Core API through `/api/core`.
- The application does not support Azure Monitor ingestion in Phase 1.
- The application does not support Grafana ingestion in Phase 1.
- The application does not support Datadog, Splunk, New Relic, or other alert sources in Phase 1.
- Azure deployment is not part of Phase 1.
- Terraform is not part of Phase 1.
- Kubernetes manifests are not part of Phase 1.
- Production security hardening is not part of Phase 1.

## 25. How To Use This README For Future Infrastructure Planning

Use this README as a planning map before designing Azure infrastructure:

1. Start from the service table to identify deployable units.
2. Use the Nginx routing section to design ingress and path routing.
3. Use the webhook section to decide how Alertmanager will reach OpsGPT.
4. Use the database section to decide whether Phase 1 shared DB is acceptable for production.
5. Use the RBAC section to plan identity and access changes, such as a future move to Microsoft Entra ID.
6. Use the Foundry workflow section to plan AI networking, credentials, and secret storage.
7. Use the notification workflow section to decide where Slack secrets and delivery logs should live.
8. Use the Azure mapping table to convert local services into cloud resources.

The main design principle is simple: keep the Phase 1 behavior stable while changing only the deployment architecture around it.

## Appendix - Earlier Quick Notes

## Services

The application has exactly five services:

- `frontend-service`: React/Vite UI.
- `core-api-service`: authentication, RBAC, projects, monitoring sources, incidents, dashboard APIs, audit logs, and internal incident APIs.
- `alert-ingestion-service`: Prometheus Alertmanager webhook receiver, raw payload storage, alert normalization, and forwarding to AI Analysis.
- `ai-analysis-service`: duplicate detection, alert correlation, incident creation through Core API, and Foundry-backed AI analysis.
- `notification-service`: console or Slack notification delivery and delivery history.

Nginx is the single entry point at:

```text
http://<VM_IP>:8080
```

## Phase 1 Boundaries

Prometheus Alertmanager is the only alert source in Phase 1. Prometheus and Alertmanager usually run inside Kubernetes. Prometheus scrapes metrics and evaluates alert rules; Alertmanager sends fired or resolved alert notifications to OpsGPT.

OpsGPT does not scrape dashboards, query the Prometheus metrics API, connect to Grafana dashboards, or integrate Azure Monitor in Phase 1.

Azure deployment, AKS, Terraform, Helm, Kubernetes manifests, Azure Service Bus, Azure App Service, Azure Container Apps, Microsoft Entra ID, production networking, and private endpoints are next-phase items and are not included.

## Database

Phase 1 uses one shared PostgreSQL database for simplicity:

- Service: `opsgpt-db`
- Database: `opsgpt_db`
- User: `opsgpt_user`
- Password: `opsgpt_password`

All backend microservices use:

```text
DATABASE_URL=postgresql://opsgpt_user:opsgpt_password@opsgpt-db:5432/opsgpt_db
```

The microservices remain separate at the application/service level. Future production phases can split the databases per service if needed.

The Core API container runs a database bootstrap before Uvicorn starts:

```text
python -m app.db.bootstrap
```

That bootstrap creates the Core API tables and enforces the default local users. If an existing Docker volume has stale default-user hashes, rebuilding the Core API image repairs them without deleting the volume.

## Project Webhook Flow

1. Admin logs in.
2. Admin creates a project.
3. Admin creates a Prometheus Alertmanager monitoring source.
4. Core API generates `webhook_token` and `webhook_path`.
5. Admin copies the full URL.
6. Alertmanager sends alerts to OpsGPT.
7. Alert Ingestion validates the token with Core API.
8. Alert Ingestion stores the raw payload and normalized alerts.
9. AI Analysis correlates alerts and creates incidents through Core API.
10. Frontend displays incidents by project.

Project webhook path:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

Full URL through Nginx:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

Alertmanager receiver example:

```yaml
receivers:
  - name: opsgpt-webhook
    webhook_configs:
      - url: 'http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}'
        send_resolved: true
```

## Authentication

Seeded users:

- `junior.engineer@company.com` / `password123` / `junior_engineer`
- `senior.engineer@company.com` / `password123` / `senior_engineer`
- `admin@company.com` / `password123` / `admin`

Phase 1 uses local JWT authentication with bearer tokens.

## Microsoft Foundry Configuration

AI Analysis uses Azure AI Foundry only when configured. Copy the endpoint, API key, and deployed model name from Azure AI Foundry or the Azure resource's **Keys and Endpoint** page. These values are supplied to `ai-analysis-service`; no other OpsGPT service calls Foundry directly.

```text
AI_PROVIDER=azure_foundry
AZURE_FOUNDRY_API_MODE=responses
AZURE_FOUNDRY_ENDPOINT=
AZURE_FOUNDRY_API_KEY=
AZURE_FOUNDRY_MODEL=
AZURE_FOUNDRY_API_VERSION=2025-04-01-preview
AZURE_FOUNDRY_TIMEOUT_SECONDS=60
AZURE_FOUNDRY_MAX_RETRIES=2
AZURE_FOUNDRY_TEMPERATURE=0.2
```

Responses API is the default mode. `chat_completions` remains available for compatible deployments. `/health` reports only service health and never tests Foundry connectivity. If Foundry configuration is missing or the AI response fails, AI Analysis does not fake output: it still creates the incident when correlation succeeds and records analysis failure with a clear error. Azure Service Bus, Azure deployment infrastructure, and other cloud integrations are not implemented in Phase 1.

## Manual Local Run

Do this manually when you are ready to run the application:

```bash
docker compose up --build
```

After pulling changes that affect Core API startup or seeding, rebuild the Core API image:

```bash
docker compose build --no-cache core-api-service
docker compose up
```

Then open:

```text
http://localhost:8080
```

The root prompt explicitly asked Codex not to run tests, installs, Docker Compose, or the application during generation, so this scaffold was created without executing those commands.
