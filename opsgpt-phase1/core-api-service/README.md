# Core API Service

The Core API Service is the user-facing backend for OpsGPT Phase 1. It owns
users, roles, incidents, timelines, resolution notes, audit logs, and knowledge
base records.

It does not ingest raw monitoring alerts, generate AI analysis, or send Slack
messages directly.

## Run With Docker Compose

From the `opsgpt-phase1` directory:

```powershell
Copy-Item core-api-service\.env.example core-api-service\.env
docker compose up --build core-api-service
```

The API is available at `http://localhost:8001`, with interactive
documentation at `http://localhost:8001/docs`.

Stop the service and database with:

```powershell
docker compose down
```

## Seed Users

The service creates these users at startup when they do not already exist:

| Email | Password | Role |
| --- | --- | --- |
| `junior.engineer@company.com` | `password123` | `junior_engineer` |
| `senior.engineer@company.com` | `password123` | `senior_engineer` |
| `admin@company.com` | `password123` | `admin` |

These credentials are for local Phase 1 development only.

## Authentication

Login uses JSON:

```json
{
  "email": "admin@company.com",
  "password": "password123"
}
```

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

Internal endpoints require:

```text
X-Internal-API-Key: change-me-internal-key
```

## RBAC

- `junior_engineer`: read-only incident and knowledge-base access
- `senior_engineer`: reader access plus status and resolution-note updates
- `admin`: editor access plus user administration and audit logs

## Optional Notifications

`ENABLE_NOTIFICATIONS=false` is the default. When enabled, the Core API sends
complete event payloads to the configured Notification Service over HTTP. It
never sends Slack messages itself.
