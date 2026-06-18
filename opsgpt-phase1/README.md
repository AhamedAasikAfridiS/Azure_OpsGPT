# OpsGPT Phase 1

OpsGPT is an internal AI first responder for production incidents, built for DevOps, SRE, Cloud Engineering, and Operations teams.

Phase 1 is local/VM development and testing only. It uses five application services plus Nginx as the reverse-proxy/routing layer.

| Service | Port | Responsibility |
| --- | --- | --- |
| frontend-service | 3000 | React UI |
| core-api-service | 8001 | Auth, RBAC, projects, incidents, dashboard, knowledge base |
| alert-ingestion-service | 8002 | Webhook receiving, raw payload storage, parsing, normalization |
| ai-analysis-service | 8003 | Correlation and Microsoft Foundry AI analysis |
| notification-service | 8004 | Console/Slack notifications |
| nginx | 8080 | Local/VM routing entry point |

## Recommended Access

Use Nginx for local/VM testing:

```text
http://<VM_IP>:8080
```

Nginx routes:

```text
/                           -> frontend-service:3000
/api/core/                  -> core-api-service:8001
/api/alerts/                -> alert-ingestion-service:8002
/api/analysis/              -> ai-analysis-service:8003
/api/notifications/         -> notification-service:8004
/alerts/webhook/            -> alert-ingestion-service:8002/alerts/webhook/
```

Frontend API base in Nginx mode:

```env
VITE_CORE_API_URL=/api/core
```

Project webhook URL:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

## Workflow

1. Admin creates a project.
2. Admin adds a monitoring source.
3. OpsGPT generates a project-specific webhook path/token.
4. Admin configures that webhook URL in Grafana, Azure Monitor, or another webhook-capable monitoring system.
5. Alert Ingestion stores and normalizes triggered alert payloads.
6. AI Analysis correlates alerts and calls Microsoft Foundry / Azure AI Foundry.
7. Core API stores incidents.
8. Frontend displays project-scoped incidents.
9. Notification Service sends console/Slack notifications when enabled.

OpsGPT does not scrape monitoring dashboards. Dashboard URLs are metadata/reference links only.

## UI Theme

The frontend uses a professional teal, teal-blue, white, and dark slate theme with responsive layouts for desktop, laptop, and tablet usage.

## Documentation

- [Development Run Guide](docs/DEVELOPMENT_RUN_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Microservices](docs/MICROSERVICES.md)
- [API Overview](docs/API_OVERVIEW.md)
- [Local Development](docs/LOCAL_DEVELOPMENT.md)
- [Nginx Routing](nginx/README.md)
