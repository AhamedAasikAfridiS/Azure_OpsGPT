# Local Development

Phase 1 is designed for local Docker Compose development. It does not include Azure deployment infrastructure or Kubernetes.

Nginx is the recommended local/VM entry point:

```text
http://<VM_IP>:8080
```

Frontend API calls should use:

```env
VITE_CORE_API_URL=/api/core
```

## Environment Files

Copy each `.env.example` to `.env` and configure values before running locally.

Important AI Analysis settings:

```env
AI_PROVIDER=foundry
FOUNDRY_ENDPOINT=
FOUNDRY_API_KEY=
FOUNDRY_MODEL_DEPLOYMENT=
FOUNDRY_API_VERSION=2024-02-15-preview
```

`INTERNAL_API_KEY` must match between Core API, Alert Ingestion, and AI Analysis.

## Webhook Testing

Use project-specific webhooks for realistic testing:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

If you place your own reverse proxy in front of Docker, route that path to `alert-ingestion-service:8002`. No reverse proxy config is included in this repo.

Sample payloads are available in `sample-payloads/`.

## Safe Defaults

- CORS is open with `*` for Phase 1 development/testing only.
- `ENABLE_ANALYSIS_FORWARDING=false` unless you want Alert Ingestion to forward alerts automatically.
- `ENABLE_NOTIFICATIONS=false` unless you want Core API to trigger Notification Service.
- `NOTIFICATION_CHANNEL=console` by default.
