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

## Foundry AI

The app starts even if Foundry variables are blank. To enable AI analysis, set these values for `ai-analysis-service`:

```text
FOUNDRY_ENDPOINT=
FOUNDRY_API_KEY=
FOUNDRY_MODEL_DEPLOYMENT=
FOUNDRY_API_VERSION=2024-02-15-preview
```

If AI fails, incidents are still created after correlation. The frontend shows a friendly empty state for AI fields.

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
