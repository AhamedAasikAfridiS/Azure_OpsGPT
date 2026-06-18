# OpsGPT - Phase 1

OpsGPT is an AI first responder for production incidents. Phase 1 is a local or VM-runnable application that receives Prometheus Alertmanager webhooks, normalizes and correlates alerts, creates project incidents, optionally calls Microsoft Foundry / Azure AI Foundry for incident analysis, displays incidents in React, and sends console or Slack notifications.

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

AI Analysis uses Foundry only when configured:

```text
AI_PROVIDER=foundry
FOUNDRY_ENDPOINT=
FOUNDRY_API_KEY=
FOUNDRY_MODEL_DEPLOYMENT=
FOUNDRY_API_VERSION=2024-02-15-preview
FOUNDRY_TIMEOUT_SECONDS=60
FOUNDRY_MAX_RETRIES=2
```

If Foundry config is missing or the AI response fails, AI Analysis does not fake output. It still creates the incident when correlation succeeds and records analysis failure with a clear error.

## Manual Local Run

Do this manually when you are ready to run the application:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8080
```

The root prompt explicitly asked Codex not to run tests, installs, Docker Compose, or the application during generation, so this scaffold was created without executing those commands.
