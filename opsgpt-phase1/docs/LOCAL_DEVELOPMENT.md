# Local Development

This guide describes the intended local setup. The commands are documentation
only.

## Prerequisites

- Docker Desktop with Docker Compose
- A local Ollama installation for the default AI provider
- The `llama3.1` Ollama model, or another model configured through
  `OLLAMA_MODEL`
- Optional Gemini, OpenAI, or Slack credentials
- Azure OpenAI variables are Phase 2 placeholders and are not required

## Default Configuration

Docker Compose supplies local defaults directly:

```text
Frontend:       http://localhost:3000
Core API:       http://localhost:8001
Alert Ingest:   http://localhost:8002
AI Analysis:    http://localhost:8003
Notification:   http://localhost:8004
```

Databases are internal to Docker and are not exposed to the host.

The default integration settings are:

```text
AI_PROVIDER=ollama
ENABLE_ANALYSIS_FORWARDING=false
ENABLE_NOTIFICATIONS=false
NOTIFICATION_CHANNEL=console
```

## Prepare Ollama

Example commands:

```powershell
ollama pull llama3.1
ollama serve
```

Docker Compose configures AI Analysis to reach host Ollama through
`http://host.docker.internal:11434`.

## Start the Project

From the `opsgpt-phase1` directory:

```powershell
docker compose up --build
```

Open:

```text
http://localhost:3000
```

## Enable the Full Alert Flow

Automatic forwarding and notifications are disabled by default. Enable both
before starting Compose:

```powershell
$env:ENABLE_ANALYSIS_FORWARDING = "true"
$env:ENABLE_NOTIFICATIONS = "true"
docker compose up --build
```

With these flags enabled:

```text
Alert Ingestion -> AI Analysis -> Core API -> Notification Service
```

## Select Another AI Provider

### Gemini

```powershell
$env:AI_PROVIDER = "gemini"
$env:GEMINI_API_KEY = "replace-with-real-key"
$env:GEMINI_MODEL = "gemini-1.5-flash"
docker compose up --build
```

### OpenAI

```powershell
$env:AI_PROVIDER = "openai"
$env:OPENAI_API_KEY = "replace-with-real-key"
$env:OPENAI_MODEL = "gpt-4o-mini"
docker compose up --build
```

### Azure OpenAI

Azure OpenAI is configuration-ready, but it is reserved for Phase 2 and is
not required for Phase 1. The following variables document the future
configuration contract:

```powershell
$env:AI_PROVIDER = "azure_openai"
$env:AZURE_OPENAI_ENDPOINT = "replace-with-endpoint"
$env:AZURE_OPENAI_API_KEY = "replace-with-real-key"
$env:AZURE_OPENAI_DEPLOYMENT = "replace-with-deployment"
$env:AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
docker compose up --build
```

No mock AI provider exists. Missing selected-provider configuration produces a
clear startup error.

## Enable Slack

```powershell
$env:NOTIFICATION_CHANNEL = "slack"
$env:SLACK_WEBHOOK_URL = "replace-with-real-slack-webhook"
$env:ENABLE_NOTIFICATIONS = "true"
docker compose up --build
```

Keep Slack webhooks and paid provider keys out of source control.

## Service Environment Files

Each service includes `.env.example`. These are useful when running a service
outside Compose:

```text
frontend-service/.env.example
core-api-service/.env.example
alert-ingestion-service/.env.example
ai-analysis-service/.env.example
notification-service/.env.example
```

Copy only the file needed by the service being run and replace placeholder
secrets. The `.gitignore` excludes populated `.env` files.

## Stop the Project

```powershell
docker compose down
```

To remove local database volumes as well:

```powershell
docker compose down --volumes
```

The second command deletes local Phase 1 database data.

## Sample Alerts

Use payloads from `sample-payloads/` with Alert Ingestion:

```powershell
curl.exe -X POST `
  "http://localhost:8002/alerts/manual" `
  -H "Content-Type: application/json" `
  --data-binary "@sample-payloads/manual-http-500-alert.json"
```

These commands have not been executed as part of the integration-alignment
task.
