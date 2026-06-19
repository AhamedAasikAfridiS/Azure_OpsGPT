# OpsGPT Nginx Reverse Proxy

Nginx is the single Phase 1 entry point.

- Main UI: `http://<VM_IP>:8080`
- Core API: `/api/core/`
- Alert Ingestion API: `/api/alerts/`
- AI Analysis API: `/api/analysis/`
- Notification API: `/api/notifications/`
- Project webhook: `/alerts/webhook/project/{project_id}/{webhook_token}`

The frontend uses `VITE_CORE_API_URL=/api/core`, so browser traffic goes through Nginx instead of calling backend containers directly.

## Container Runtime

The reverse-proxy image is built from `nginx/Dockerfile` and runs as the built-in unprivileged `nginx` user. It listens on container port `8080`, while Docker Compose continues to expose `http://<VM_IP>:8080` externally. The upstream paths and service targets are unchanged.

The frontend service now serves its Vite production build through a separate non-root Nginx runtime on internal port `3000`. Its history fallback returns `index.html`, so React Router refreshes continue to work.

All runtime secrets remain Compose environment values; no `.env` file is copied into any application image.

Phase 1 CORS is intentionally permissive:

- `Access-Control-Allow-Origin: *`
- No credentials
- OPTIONS requests return `204`

Webhook example:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```
