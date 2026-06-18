# OpsGPT Phase 1 - Local Development Run Guide

This guide explains how to run and test OpsGPT locally or on a single VM.

## Scope

- Local/VM development only
- No Azure deployment files
- No Kubernetes
- Webhook-based alert ingestion
- Microsoft Foundry / Azure AI Foundry for AI Analysis
- Nginx for local/VM reverse proxy routing

## Recommended URL

Use Nginx as the main entry point:

```text
http://<VM_IP>:8080
```

Frontend API base:

```env
VITE_CORE_API_URL=/api/core
```

Do not use `localhost` in frontend API configuration when testing through Nginx on a VM.

## Services

| Service | Direct Port | Nginx Route |
| --- | --- | --- |
| frontend-service | 3000 | `/` |
| core-api-service | 8001 | `/api/core/` |
| alert-ingestion-service | 8002 | `/api/alerts/` |
| ai-analysis-service | 8003 | `/api/analysis/` |
| notification-service | 8004 | `/api/notifications/` |

## Project Webhook

Generated webhook path:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

Full Nginx URL:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

Admins should configure this URL in Grafana, Azure Monitor, or another webhook-capable monitoring system.

## Environment Setup

Copy `.env.example` files to `.env` files and configure values.

Important frontend value:

```env
VITE_CORE_API_URL=/api/core
```

Important AI Analysis values:

```env
AI_PROVIDER=foundry
FOUNDRY_ENDPOINT=
FOUNDRY_API_KEY=
FOUNDRY_MODEL_DEPLOYMENT=
FOUNDRY_API_VERSION=2024-02-15-preview
```

## CORS

CORS is open for Phase 1 development only.

Nginx and FastAPI services allow wildcard origins for local/VM testing. Production should restrict CORS origins to trusted domains.

## UI

The frontend theme uses teal, teal-blue, white, and dark slate colors. Layouts are responsive for desktop, laptop, and tablet use.
