# Development Run Guide

This guide is for manual local testing. Codex did not run installs, tests, Docker Compose, or the application while creating this scaffold.

## Start Locally

From the `opsgpt-phase1` directory, manually run:

```bash
docker compose up --build
```

If login fails with the seeded credentials after code changes, rebuild Core API so the container picks up the latest database bootstrap:

```bash
docker compose build --no-cache core-api-service
docker compose up
```

The Core API container runs this before starting the API server:

```text
python -m app.db.bootstrap
```

It creates tables and resets these default local users to the documented passwords without requiring a volume reset.

Open:

```text
http://localhost:8080
```

Useful direct service URLs:

- Frontend: `http://localhost:3000`
- Core API docs: `http://localhost:8001/docs`
- Alert Ingestion docs: `http://localhost:8002/docs`
- AI Analysis docs: `http://localhost:8003/docs`
- Notification docs: `http://localhost:8004/docs`

## Login

Default users:

- `admin@company.com` / `password123`
- `senior.engineer@company.com` / `password123`
- `junior.engineer@company.com` / `password123`

## Admin Setup Flow

1. Log in as admin.
2. Open Admin.
3. Create a project.
4. Open Configure for that project.
5. Create a monitoring source with source type `Prometheus Alertmanager`.
6. Copy the generated webhook URL.
7. Assign junior and senior engineers to the project.

The generated URL will look like:

```text
http://localhost:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

Use the VM IP instead of `localhost` when configuring Alertmanager outside the VM.

## Alertmanager Receiver

```yaml
receivers:
  - name: opsgpt-webhook
    webhook_configs:
      - url: 'http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}'
        send_resolved: true
```

## Sample Payloads

Use files in `sample-payloads/` for manual webhook testing. Only Prometheus Alertmanager samples are included:

- `prometheus-alertmanager-critical-cpu.json`
- `prometheus-alertmanager-memory-warning.json`
- `prometheus-alertmanager-k8s-crashloop.json`
- `prometheus-alertmanager-multiple-alerts.json`
- `prometheus-alertmanager-resolved-alert.json`

## Azure AI Foundry

The app starts even if Azure AI Foundry variables are blank. To enable AI analysis, obtain the endpoint and API key from Azure AI Foundry or the Azure resource's **Keys and Endpoint** page, and use the model deployment name configured in Foundry. Set these values for `ai-analysis-service`:

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

Only `ai-analysis-service` calls Foundry. The default `responses` mode uses `/openai/v1/responses`; `chat_completions` is available for compatible deployments. `/health` does not test Azure AI Foundry connectivity. If configuration is missing or analysis fails, incidents are still created after correlation and the service records `analysis_status=failed` with a clear error. No other cloud integration is implemented in Phase 1.

## Database

Phase 1 uses one PostgreSQL service:

```text
opsgpt-db
```

Database URL:

```text
postgresql://opsgpt_user:opsgpt_password@opsgpt-db:5432/opsgpt_db
```

The shared database keeps local development simple while the five application services remain separate.
