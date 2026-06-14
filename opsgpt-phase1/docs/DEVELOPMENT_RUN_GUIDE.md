# OpsGPT Phase 1 - Local Development Run Guide

## 1. Purpose Of This Guide

This guide helps a developer configure and run the generated OpsGPT Phase 1
project on a local development machine. It explains the services, environment
variables, Docker Compose workflow, login accounts, manual API requests, and
common troubleshooting steps.

All commands in this document are examples for the developer to run manually.

## 2. Phase 1 Scope

OpsGPT Phase 1 is intended for local development and demonstration.

- There is no Azure deployment in Phase 1.
- A real Azure Monitor integration is not required.
- A real Grafana integration is not required.
- Alerts can be tested with the JSON files in `sample-payloads/`.
- Admins create projects, assign members, and register monitoring sources.
- Project sources receive generated webhook URLs and tokens.
- Azure OpenAI is planned as a Phase 2 integration path.
- Phase 1 AI analysis can use Ollama, Gemini, or OpenAI.
- Services communicate through local REST APIs.
- PostgreSQL is used for service-owned databases.

## 3. Architecture Summary

```text
Grafana / Azure Monitor / Manual Alert
                  |
                  v
        Alert Ingestion Service
                  |
                  v
         AI Analysis Service
                  |
                  v
           Core API Service
             |          |
             v          v
      Frontend Service  Notification Service
```

Grafana and Azure Monitor continuously monitor applications, infrastructure,
metrics, logs, and health signals. When an alert rule is triggered, the
monitoring platform sends an alert payload to an OpsGPT webhook.

OpsGPT does not scrape Grafana or Azure Monitor dashboards. It receives and
processes triggered alert payloads through the Alert Ingestion Service.

## 4. Service Responsibilities

| Service | Port | Responsibility | Depends on |
| --- | ---: | --- | --- |
| `frontend-service` | `3000` | React UI | `core-api-service` |
| `core-api-service` | `8001` | Authentication, RBAC, projects, monitoring metadata, incidents, dashboard, and knowledge base | `core-db`; `notification-service` is optional |
| `alert-ingestion-service` | `8002` | Alert receiving, project token validation, parsing, and normalization | `alert-db`, `core-api-service`; `ai-analysis-service` is optional |
| `ai-analysis-service` | `8003` | Correlation, AI summary, RCA, and fix recommendations | `analysis-db`, `core-api-service` |
| `notification-service` | `8004` | Console or Slack notifications | `notification-db` |

Each backend service owns its own data. Services must communicate through
their APIs rather than reading another service's database.

## 5. Prerequisites

Recommended local development prerequisites:

- Docker Desktop with Docker Compose
- Visual Studio Code
- Git
- Optional: Ollama installed locally
- Optional: Gemini API key
- Optional: OpenAI API key
- Optional: Slack Incoming Webhook URL

Only one configured AI provider is required when AI analysis is used.

## 6. Environment Setup

Each service contains a `.env.example` file. Create local `.env` files from
the examples and keep real secrets out of source control.

From the `opsgpt-phase1` directory, Unix-style commands are:

```bash
cp core-api-service/.env.example core-api-service/.env
cp alert-ingestion-service/.env.example alert-ingestion-service/.env
cp ai-analysis-service/.env.example ai-analysis-service/.env
cp notification-service/.env.example notification-service/.env
cp frontend-service/.env.example frontend-service/.env
```

PowerShell equivalents are:

```powershell
Copy-Item core-api-service/.env.example core-api-service/.env
Copy-Item alert-ingestion-service/.env.example alert-ingestion-service/.env
Copy-Item ai-analysis-service/.env.example ai-analysis-service/.env
Copy-Item notification-service/.env.example notification-service/.env
Copy-Item frontend-service/.env.example frontend-service/.env
```

Service-level `.env` files are used when services run directly on the host.
The current `docker-compose.yml` supplies container environment values
directly. Compose overrides such as `AI_PROVIDER` and feature flags can be set
in the terminal or in a root `opsgpt-phase1/.env` file.

### Core API Variables

- `DATABASE_URL`: Core PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret used to sign JWT access tokens
- `INTERNAL_API_KEY`: Shared key accepted by Core internal endpoints
- `NOTIFICATION_SERVICE_URL`: Notification Service base URL
- `ENABLE_NOTIFICATIONS`: Enables the optional notification handoff

### Alert Ingestion Variables

- `DATABASE_URL`: Alert PostgreSQL connection string
- `AI_ANALYSIS_SERVICE_URL`: AI Analysis Service base URL
- `CORE_API_URL`: Core API used to validate project webhook tokens
- `INTERNAL_API_KEY`: Must match the Core API value
- `ENABLE_ANALYSIS_FORWARDING`: Enables automatic normalized-alert forwarding

### AI Analysis Variables

- `DATABASE_URL`: Analysis PostgreSQL connection string
- `CORE_API_URL`: Core API base URL
- `INTERNAL_API_KEY`: Must match the Core API value
- `AI_PROVIDER`: `ollama`, `gemini`, or `openai` for Phase 1
- `OLLAMA_BASE_URL`: Ollama server URL
- `OLLAMA_MODEL`: Ollama model name
- `GEMINI_API_KEY`: Gemini API key
- `GEMINI_MODEL`: Gemini model name
- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_MODEL`: OpenAI model name

### Notification Variables

- `DATABASE_URL`: Notification PostgreSQL connection string
- `NOTIFICATION_CHANNEL`: `console` or `slack`
- `SLACK_WEBHOOK_URL`: Required when the channel is `slack`

### Frontend Variables

- `VITE_CORE_API_URL`: Browser-accessible Core API URL
- `VITE_ALERT_INGESTION_URL`: Public base URL displayed with generated webhook
  paths

For Docker Compose, the frontend value should remain:

```env
VITE_CORE_API_URL=http://localhost:8001
VITE_ALERT_INGESTION_URL=http://localhost:8002
```

The browser cannot use Docker-only service names such as
`http://core-api-service:8001`.

## 7. Important Default Modes

The default safe local configuration is:

```env
ENABLE_ANALYSIS_FORWARDING=false
ENABLE_NOTIFICATIONS=false
NOTIFICATION_CHANNEL=console
AI_PROVIDER=ollama
```

These defaults mean:

- Alert Ingestion can receive, validate, normalize, and store alerts.
- Alert Ingestion does not automatically forward alerts to AI Analysis.
- Core API does not automatically trigger Notification Service.
- Notification Service prints messages to its console.
- AI Analysis expects a real Ollama server and configured Ollama model.
- No mock or fake AI output is used.

This mode allows developers to inspect services independently before enabling
the complete processing flow.

## 8. Full Local Workflow Mode

For services running directly on the host, update these service files:

`alert-ingestion-service/.env`:

```env
ENABLE_ANALYSIS_FORWARDING=true
```

`core-api-service/.env`:

```env
ENABLE_NOTIFICATIONS=true
```

`notification-service/.env`:

```env
NOTIFICATION_CHANNEL=console
```

For Docker Compose, put the matching overrides in
`opsgpt-phase1/.env`:

```env
ENABLE_ANALYSIS_FORWARDING=true
ENABLE_NOTIFICATIONS=true
NOTIFICATION_CHANNEL=console
```

To use Slack instead of console output:

```env
NOTIFICATION_CHANNEL=slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/replace-with-real-value
```

Do not commit the populated root or service `.env` files.

## 9. AI Provider Setup

Set only the provider and credentials required for the selected provider.
Missing selected-provider configuration causes a clear AI Analysis startup
configuration error.

### Ollama

For AI Analysis running in Docker while Ollama runs on the laptop:

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1
```

Use `host.docker.internal` when a Docker container must call Ollama running on
the host machine.

For AI Analysis running directly outside Docker:

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
```

The configured Ollama model must already be available in the local Ollama
installation.

### Gemini

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=replace-with-real-key
GEMINI_MODEL=gemini-1.5-flash
```

### OpenAI

```env
AI_PROVIDER=openai
OPENAI_API_KEY=replace-with-real-key
OPENAI_MODEL=gpt-4o-mini
```

### Azure OpenAI

Azure OpenAI configuration fields and a provider client are reserved for
Phase 2. Azure OpenAI is not required for Phase 1 local development.

## 10. Docker Compose Overview

The root `docker-compose.yml` includes:

- Five application services
- Four PostgreSQL databases
- One common `opsgpt-network` network
- Four named database volumes

Database ports are internal to the Docker network. Only application ports are
published to the host.

Build the images:

```bash
docker compose build
```

Start the project:

```bash
docker compose up
```

Stop the project:

```bash
docker compose down
```

Stop the project and delete local database volumes:

```bash
docker compose down -v
```

The final command permanently removes data stored in the local Compose
database volumes.

## 11. Local Application URLs

| Component | URL |
| --- | --- |
| Frontend | `http://localhost:3000` |
| Core API documentation | `http://localhost:8001/docs` |
| Alert Ingestion API documentation | `http://localhost:8002/docs` |
| AI Analysis API documentation | `http://localhost:8003/docs` |
| Notification API documentation | `http://localhost:8004/docs` |

## 12. Default Login Users

Core API seeds these local development users:

| Email | Password | Role |
| --- | --- | --- |
| [junior.engineer@company.com](mailto:junior.engineer@company.com) | `password123` | `junior_engineer` |
| [senior.engineer@company.com](mailto:senior.engineer@company.com) | `password123` | `senior_engineer` |
| [admin@company.com](mailto:admin@company.com) | `password123` | `admin` |

Role behavior:

- `junior_engineer` has read-only incident and knowledge-base access.
- `senior_engineer` can update and resolve incidents and add resolution notes.
- `admin` can update and resolve incidents, add notes, and use administrative
  APIs.

These accounts and passwords are for local Phase 1 development only.

## 13. Manual Testing Workflow

The following PowerShell and `curl.exe` examples are documentation only. Run
them from the `opsgpt-phase1` directory after the required services are
available.

### Step A: Login As Admin

```powershell
$login = Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8001/auth/login" `
  -ContentType "application/json" `
  -Body '{"email":"admin@company.com","password":"password123"}'

$adminToken = $login.access_token
```

Equivalent endpoint:

```text
POST http://localhost:8001/auth/login
```

### Step B: Create An Incident Through The Core Internal API

```powershell
curl.exe -X POST `
  "http://localhost:8001/internal/incidents" `
  -H "Content-Type: application/json" `
  -H "X-Internal-API-Key: change-me-internal-key" `
  -d '{
    "incident_id": "INC-2026-000001",
    "title": "Payment API incident detected - critical",
    "service_name": "payment-api",
    "severity": "critical",
    "status": "open",
    "related_alert_ids": ["ALT-MANUAL-001"]
  }'
```

### Step C: Update Incident Analysis

```powershell
curl.exe -X PATCH `
  "http://localhost:8001/internal/incidents/INC-2026-000001/analysis" `
  -H "Content-Type: application/json" `
  -H "X-Internal-API-Key: change-me-internal-key" `
  -d '{
    "ai_summary": "Payment API is experiencing database connectivity failures.",
    "root_cause": "PostgreSQL connection pool exhaustion",
    "supporting_evidence": [
      "Database timeout alert",
      "Elevated API latency"
    ],
    "confidence_score": 92,
    "recommended_fix": {
      "immediate_actions": [
        "Review active database sessions",
        "Increase the connection pool within approved limits"
      ],
      "long_term_actions": [
        "Optimize slow database queries"
      ],
      "runbook_suggestions": [
        "Database connectivity troubleshooting runbook"
      ]
    }
  }'
```

### Step D: View The Incident

Open the frontend:

```text
http://localhost:3000/incidents/INC-2026-000001
```

Or call Core API:

```powershell
curl.exe `
  "http://localhost:8001/incidents/INC-2026-000001" `
  -H "Authorization: Bearer $adminToken"
```

### Step E: Submit A Manual Alert

```powershell
curl.exe -X POST `
  "http://localhost:8002/alerts/manual" `
  -H "Content-Type: application/json" `
  --data-binary "@sample-payloads/manual-database-alert.json"
```

Another manual example is available at:

```text
sample-payloads/manual-http-500-alert.json
```

### Step F: Submit The Azure Monitor Sample

```powershell
curl.exe -X POST `
  "http://localhost:8002/alerts/webhook/azure-monitor" `
  -H "Content-Type: application/json" `
  --data-binary "@sample-payloads/azure-monitor-cpu-alert.json"
```

### Step G: Submit The Grafana Sample

```powershell
curl.exe -X POST `
  "http://localhost:8002/alerts/webhook/grafana" `
  -H "Content-Type: application/json" `
  --data-binary "@sample-payloads/grafana-latency-alert.json"
```

When `ENABLE_ANALYSIS_FORWARDING=false`, Steps E through G store and normalize
alerts but do not trigger AI analysis automatically.

### Project-Based Webhook Workflow

1. Login as `admin`.
2. Open `Admin Projects` and create a project.
3. Open the membership section and search active users by name, email, or
   role.
4. Select a user and choose `Assign to Project`.
5. Open the project's `Monitoring sources` page.
6. Add a Grafana, Azure Monitor, or custom source.
7. Copy the generated webhook URL.
8. Configure the monitoring tool's webhook/contact point to POST triggered
   alert payloads to that URL.
9. Login as an assigned engineer and select the project.
10. View project-scoped dashboard and incident pages.

Dashboard and alert rule URLs are metadata links only. OpsGPT does not scrape
them.

## 14. Expected End-To-End Flow

1. An alert is submitted to Alert Ingestion.
2. For project webhooks, Alert Ingestion validates the project token with
   Core API.
3. Alert Ingestion stores the original raw payload.
4. Alert Ingestion parses, validates, normalizes, and stores the project ID.
5. If forwarding is enabled, it sends the normalized alert to AI Analysis.
6. AI Analysis checks for duplicates and correlates only within the project.
6. AI Analysis calls the configured real AI provider.
7. AI Analysis creates an incident through the Core internal API when needed.
8. AI Analysis updates Core with the generated summary, RCA, evidence,
   confidence score, and recommended fix.
9. Core API stores and exposes the incident.
10. The frontend reads incident and dashboard data from Core API.
11. If notifications are enabled, Core API triggers Notification Service.
12. Notification Service sends the formatted message to console or Slack and
    records its delivery attempts.

## 15. Common Issues And Fixes

### Frontend Cannot Connect To The Backend

- Check `VITE_CORE_API_URL`.
- For browser requests, use `http://localhost:8001`.
- Check that `core-api-service` is available on port `8001`.
- Restart or rebuild the frontend after changing a Vite environment variable.

### AI Analysis Fails With Ollama

- Check that Ollama is running.
- Check `OLLAMA_BASE_URL`.
- Check that `OLLAMA_MODEL` identifies an available model.
- When a Docker container calls host Ollama, use
  `http://host.docker.internal:11434`.
- Use `http://localhost:11434` only when AI Analysis runs on the host.

### Gemini Or OpenAI Fails

- Check the selected API key.
- Check the selected model name.
- Check that `AI_PROVIDER` matches the configured provider.
- Check provider account access, quota, and network connectivity.

### Slack Notification Is Not Sent

- Check `NOTIFICATION_CHANNEL=slack`.
- Check that `SLACK_WEBHOOK_URL` contains a real webhook URL.
- Check the Notification Service logs and stored delivery attempts.
- Check that the Notification Service can reach the Slack webhook endpoint.

### Alert Is Stored But Not Analyzed

- Check `ENABLE_ANALYSIS_FORWARDING=true`.
- Check `AI_ANALYSIS_SERVICE_URL`.
- Check that AI Analysis is running and its provider is configured.

### Incident Is Created But No Notification Is Sent

- Check `ENABLE_NOTIFICATIONS=true`.
- Check `NOTIFICATION_SERVICE_URL`.
- Check that `notification-service` is running.
- Check the configured notification channel.

### Internal API Returns 401

- Check the `X-Internal-API-Key` header.
- Check that `INTERNAL_API_KEY` matches between Core API and AI Analysis.
- Check that the request is being sent to an `/internal/...` endpoint.

### User Action Returns 403

- Confirm the user role.
- `junior_engineer` is intentionally read-only.
- Use `senior_engineer` or `admin` for status and resolution-note actions.

## 16. Development Notes

- Sidebar navigation uses exact route patterns so only the relevant section is
  highlighted.
- Project incident, project dashboard, project incident list, and monitoring
  source pages include logical back navigation.
- Keep service responsibilities separate.
- The frontend should call Core API for normal user workflows.
- Do not make the frontend call AI Analysis directly.
- Do not make Alert Ingestion create incidents directly.
- Do not make Notification Service perform incident analysis.
- Do not make AI Analysis write directly to the Core database.
- Do not hardcode secrets or provider keys.
- Use ignored `.env` files for local secrets.
- Keep `INTERNAL_API_KEY` synchronized between Core API and AI Analysis.

## 17. Current Phase 1 Limitations

- No real Azure Monitor webhook configuration is included.
- No real Grafana contact point configuration is included.
- No Azure OpenAI migration is included.
- No Kubernetes deployment is included.
- No production security hardening is included.
- No centralized logging platform is included.
- No service bus or event broker is included.
- Local synchronous REST communication is used between services.
- Database tables are created through SQLAlchemy metadata rather than a full
  migration workflow.
- Existing local database volumes must be recreated once after adding the
  project tables and nullable project columns because Phase 1 has no migration
  runner.

## 18. Future Phase 2 Ideas

- Azure OpenAI
- Real Azure Monitor webhook integration
- Real Grafana webhook contact point
- Azure Service Bus
- Azure App Service or Azure Container Apps deployment
- Private networking
- Microsoft Entra ID login
- Microsoft Teams notifications
- RAG and vector search for incident knowledge
- Centralized observability and distributed tracing
- Managed database migrations

## 19. Final Developer Checklist

- [ ] `.env` files created from `.env.example`
- [ ] `INTERNAL_API_KEY` matches between Core API and AI Analysis
- [ ] `INTERNAL_API_KEY` also matches Alert Ingestion
- [ ] `AI_PROVIDER` configured
- [ ] Ollama, Gemini, or OpenAI configured
- [ ] Docker Desktop running
- [ ] `docker compose build` completed
- [ ] `docker compose up` completed
- [ ] Frontend accessible on port `3000`
- [ ] Core API documentation accessible on port `8001`
- [ ] Admin project created and engineers assigned
- [ ] Monitoring source webhook generated
- [ ] Manual alert submitted successfully
- [ ] Project incident visible in the dashboard
