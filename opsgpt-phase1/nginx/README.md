# OpsGPT Nginx Routing

Nginx is the recommended single local/VM entry point for OpsGPT Phase 1.

External routes:

| Route | Target |
| --- | --- |
| `/` | `frontend-service:3000` |
| `/api/core/` | `core-api-service:8001/` |
| `/api/alerts/` | `alert-ingestion-service:8002/` |
| `/api/analysis/` | `ai-analysis-service:8003/` |
| `/api/notifications/` | `notification-service:8004/` |
| `/alerts/webhook/` | `alert-ingestion-service:8002/alerts/webhook/` |

Main app URL:

```text
http://<VM_IP>:8080
```

Project webhook URL:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

The frontend should use this relative API base in Nginx mode:

```env
VITE_CORE_API_URL=/api/core
```

CORS is open for Phase 1 development only. Production should restrict allowed origins.
