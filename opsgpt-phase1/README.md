# OpsGPT Phase 1

OpsGPT is a local AI-powered incident management platform for DevOps, SRE,
Cloud Engineering, Platform Engineering, and Operations teams.

Phase 1 receives monitoring alerts, normalizes and correlates them, asks a real
AI provider for incident analysis, stores incidents in the Core API, displays
them in a React frontend, and delivers incident notifications through console
or Slack.

## Phase 1 Scope

Phase 1 includes:

- Five application services
- Four PostgreSQL databases
- Local JWT authentication and role-based access control
- Admin-managed projects, memberships, and monitoring source metadata
- Project-specific webhook URLs and incident isolation
- Azure Monitor-style, Grafana-style, and manual alert ingestion
- Rule-based duplicate detection and alert correlation
- Real AI provider integration through Ollama, Gemini, or OpenAI
- Azure OpenAI configuration and client path reserved for Phase 2
- Incident, dashboard, timeline, audit, and knowledge-base APIs
- Console and Slack notification channels
- React user interface
- Dockerfiles and Docker Compose for local development

Phase 1 does not include Azure deployment, Kubernetes, Nginx, Microsoft Entra
ID, message queues, vector search, WebSockets, or production hardening.

## Microservices

| Service | Responsibility | Boundary |
| --- | --- | --- |
| `frontend-service` | Login, dashboards, incidents, knowledge base, profile, and role-aware controls | Calls Core API for normal user workflows |
| `core-api-service` | Authentication, RBAC, projects, monitoring metadata, incidents, timelines, audits, and knowledge base | Does not ingest alerts, generate AI output, or send Slack directly |
| `alert-ingestion-service` | Receives, validates project webhooks, stores, normalizes, and forwards alerts | Does not create incidents or generate analysis |
| `ai-analysis-service` | Project-aware duplicate detection, correlation, real AI analysis, and Core API integration | Does not parse raw monitoring payloads or write to the Core database |
| `notification-service` | Formats and delivers console or Slack notifications and records attempts | Does not analyze or manage incidents |

More detail is available in [docs/MICROSERVICES.md](docs/MICROSERVICES.md).

## Local Development Run Guide

For beginner-friendly environment setup, Docker Compose instructions, AI
provider configuration, sample API requests, troubleshooting, and the final
developer checklist, see
[docs/DEVELOPMENT_RUN_GUIDE.md](docs/DEVELOPMENT_RUN_GUIDE.md).

## Local Ports

| Component | Host Port | Container Port |
| --- | ---: | ---: |
| Frontend Service | `3000` | `3000` |
| Core API Service | `8001` | `8001` |
| Alert Ingestion Service | `8002` | `8002` |
| AI Analysis Service | `8003` | `8003` |
| Notification Service | `8004` | `8004` |

The PostgreSQL databases are available only inside `opsgpt-network` on port
`5432`. They are not published to the host.

## Docker Compose Services

`docker-compose.yml` defines:

- `frontend-service`
- `core-api-service`
- `alert-ingestion-service`
- `ai-analysis-service`
- `notification-service`
- `core-db`
- `alert-db`
- `analysis-db`
- `notification-db`

All containers join the `opsgpt-network` bridge network. Database state is
stored in:

- `core_db_data`
- `alert_db_data`
- `analysis_db_data`
- `notification_db_data`

## Environment Configuration

Each application service contains a `.env.example` file. These files document
the variables used when running a service separately. Docker Compose provides
aligned local defaults directly in `docker-compose.yml`.

Important defaults:

```text
AI_PROVIDER=ollama
ENABLE_ANALYSIS_FORWARDING=false
ENABLE_NOTIFICATIONS=false
NOTIFICATION_CHANNEL=console
INTERNAL_API_KEY=change-me-internal-key
```

The Core API and AI Analysis Service must use the same `INTERNAL_API_KEY`.
Alert Ingestion uses that same key when validating project webhook tokens
through Core API.

The frontend uses `http://localhost:8001` because its requests originate in the
user's browser. Backend containers use Docker DNS names such as
`http://core-api-service:8001`.

The AI container reaches a host-running Ollama server through:

```text
http://host.docker.internal:11434
```

## Safe Default Mode

The default Compose configuration starts all services but keeps automatic
cross-service side effects disabled:

- Alert Ingestion stores normalized alerts but does not forward them because
  `ENABLE_ANALYSIS_FORWARDING=false`.
- Core API does not emit notification events because
  `ENABLE_NOTIFICATIONS=false`.
- Notification delivery uses the console channel.
- AI Analysis is configured for a real Ollama model and never returns mock
  output.

Enable the full processing flow only after Ollama or another real provider is
configured:

```powershell
$env:ENABLE_ANALYSIS_FORWARDING = "true"
$env:ENABLE_NOTIFICATIONS = "true"
docker compose up --build
```

These commands are documentation only and have not been executed by Codex.

## Expected Local Workflow

1. An admin creates a project, assigns engineers, and adds a monitoring source.
2. OpsGPT returns a project-specific webhook URL and token.
3. Azure Monitor, Grafana, or a custom source sends a triggered alert to that
   webhook.
4. Alert Ingestion validates the token with Core, stores the original JSON,
   and creates a project-scoped normalized alert.
5. When forwarding is enabled, Alert Ingestion sends the normalized alert to
   AI Analysis.
6. AI Analysis detects duplicates and correlates related alerts within the
   project.
7. AI Analysis asks the configured real provider for summary, RCA, confidence,
   evidence, and recommended fixes.
8. AI Analysis creates or updates the project incident through Core API REST
   endpoints.
9. Assigned engineers select the project and view its incidents in the
   frontend.
10. When notifications are enabled, Core API sends a complete event to
   Notification Service.
11. Notification Service writes to the console or posts to Slack.

OpsGPT receives alerts that monitoring systems trigger. It does not scrape or
poll Grafana and Azure Monitor dashboards. See
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Development Order Completed

1. Core API
2. Alert Ingestion
3. AI Analysis
4. Notification
5. Frontend

## Important Notes

- Do not enable Slack until `SLACK_WEBHOOK_URL` is configured correctly.
- Do not select Gemini or OpenAI until the matching API key and model values
  are configured.
- Azure OpenAI is a Phase 2-ready configuration path and is not required for
  Phase 1.
- Paid provider keys must never be committed.
- The default notification mode is `console`.
- The default AI provider is `ollama`.
- Ollama must have the configured model installed before AI requests succeed.
- The placeholder JWT and internal API secrets are for local development only.

## Seed Users

Core API creates these local users when its database is empty:

| Email | Password | Role |
| --- | --- | --- |
| `junior.engineer@company.com` | `password123` | `junior_engineer` |
| `senior.engineer@company.com` | `password123` | `senior_engineer` |
| `admin@company.com` | `password123` | `admin` |

## Manual API Examples

The following examples are documentation only.

### Health Endpoints

```powershell
curl.exe http://localhost:8001/health
curl.exe http://localhost:8002/health
curl.exe http://localhost:8003/health
curl.exe http://localhost:8004/health
```

### Login

```powershell
$login = Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8001/auth/login" `
  -ContentType "application/json" `
  -Body '{"email":"admin@company.com","password":"password123"}'

$token = $login.access_token
```

### Read Dashboard

```powershell
Invoke-RestMethod `
  -Method Get `
  -Uri "http://localhost:8001/dashboard/summary" `
  -Headers @{ Authorization = "Bearer $token" }
```

### Submit Sample Alerts

```powershell
curl.exe -X POST `
  "http://localhost:8002/alerts/webhook/azure-monitor" `
  -H "Content-Type: application/json" `
  --data-binary "@sample-payloads/azure-monitor-cpu-alert.json"

curl.exe -X POST `
  "http://localhost:8002/alerts/webhook/grafana" `
  -H "Content-Type: application/json" `
  --data-binary "@sample-payloads/grafana-latency-alert.json"

curl.exe -X POST `
  "http://localhost:8002/alerts/manual" `
  -H "Content-Type: application/json" `
  --data-binary "@sample-payloads/manual-database-alert.json"
```

## Documentation

- [Local Development Run Guide](docs/DEVELOPMENT_RUN_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Microservices](docs/MICROSERVICES.md)
- [Local Development](docs/LOCAL_DEVELOPMENT.md)
- [API Overview](docs/API_OVERVIEW.md)

No service should be treated as production-ready.
