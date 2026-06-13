# Alert Ingestion Service

The Alert Ingestion Service is the entry point for monitoring alerts in OpsGPT
Phase 1. It receives source payloads, stores the raw JSON, normalizes valid
alerts, records processing events, and optionally forwards normalized alerts
to the AI Analysis Service.

## Responsibilities

- Azure Monitor-style webhook intake
- Grafana-style webhook intake
- Manual alert submissions
- Raw alert storage
- Validation, parsing, and normalization
- Normalized alert storage
- Ingestion event logging
- Forwarding normalized alerts to AI Analysis

This service will not create incidents, generate AI output, manage users, or
send notifications.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/alerts/webhook/azure-monitor` | Receive Azure Monitor Common Alert Schema payloads |
| `POST` | `/alerts/webhook/grafana` | Receive Grafana webhook payloads |
| `POST` | `/alerts/manual` | Submit a manual alert |
| `GET` | `/alerts` | List normalized alerts |
| `GET` | `/alerts/{alert_id}` | Get the latest normalized record for an alert ID |
| `GET` | `/alerts/{alert_id}/raw` | Get the latest raw payload for an alert ID |
| `GET` | `/health` | Get service health |

## Forwarding

Forwarding is disabled by default. When
`ENABLE_ANALYSIS_FORWARDING=true`, the service sends the normalized alert JSON
to:

```text
POST {AI_ANALYSIS_SERVICE_URL}/analysis/alerts
```

Successful delivery changes the alert status to `forwarded`. A failed request
does not reject the accepted alert; it changes the stored status to `failed`
and adds an `alert_forward_failed` ingestion log.

## Configuration

Create `.env` from `.env.example` and provide:

- `DATABASE_URL`
- `AI_ANALYSIS_SERVICE_URL`
- `ENABLE_ANALYSIS_FORWARDING`
- `APP_ENV`
- `CORS_ORIGINS`
