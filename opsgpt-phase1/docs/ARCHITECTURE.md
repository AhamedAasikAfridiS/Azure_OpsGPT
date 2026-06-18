# OpsGPT Architecture

OpsGPT Phase 1 is a local/VM, webhook-driven microservices application.

```text
Monitoring System / Manual Alert
        |
        | triggered webhook payload
        v
Nginx
        |
        v
Alert Ingestion Service
        |
        v
AI Analysis Service
        |
        v
Core API Service
        |
        v
Frontend Service

Core API Service -> Notification Service
```

OpsGPT does not scrape Grafana, Azure Monitor, or any monitoring dashboard. Monitoring systems continuously monitor infrastructure and send triggered webhook payloads to OpsGPT.

## Nginx Routing

Recommended local/VM entry point:

```text
http://<VM_IP>:8080
```

Routes:

```text
/                           -> frontend-service:3000
/api/core/                  -> core-api-service:8001
/api/alerts/                -> alert-ingestion-service:8002
/api/analysis/              -> ai-analysis-service:8003
/api/notifications/         -> notification-service:8004
/alerts/webhook/            -> alert-ingestion-service:8002/alerts/webhook/
```

The frontend uses:

```env
VITE_CORE_API_URL=/api/core
```

## Project Webhooks

Admins create projects and monitoring sources. OpsGPT returns a webhook path:

```text
/alerts/webhook/project/{project_id}/{webhook_token}
```

With Nginx:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

## AI Analysis

AI Analysis uses Microsoft Foundry / Azure AI Foundry. AI failures should be stored cleanly and should not crash the full incident pipeline.

## UI

The frontend uses a professional teal / teal-blue / white / dark slate theme and responsive layout patterns for desktop, laptop, and tablet usage.
