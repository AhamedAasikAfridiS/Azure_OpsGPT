# OpsGPT Nginx Reverse Proxy

Nginx is the single Phase 1 entry point.

- Main UI: `http://<VM_IP>:8080`
- Core API: `/api/core/`
- Alert Ingestion API: `/api/alerts/`
- AI Analysis API: `/api/analysis/`
- Notification API: `/api/notifications/`
- Project webhook: `/alerts/webhook/project/{project_id}/{webhook_token}`

The frontend uses `VITE_CORE_API_URL=/api/core`, so browser traffic goes through Nginx instead of calling backend containers directly.

Phase 1 CORS is intentionally permissive:

- `Access-Control-Allow-Origin: *`
- No credentials
- OPTIONS requests return `204`

Webhook example:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```
