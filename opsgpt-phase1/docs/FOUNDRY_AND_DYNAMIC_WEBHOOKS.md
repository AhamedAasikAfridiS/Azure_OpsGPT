# Foundry AI and Dynamic Webhooks

OpsGPT Phase 1 now uses Microsoft Foundry / Azure AI Foundry as the only AI provider for incident analysis.

Required AI Analysis configuration:

```env
AI_PROVIDER=foundry
FOUNDRY_ENDPOINT=
FOUNDRY_API_KEY=
FOUNDRY_MODEL_DEPLOYMENT=
FOUNDRY_API_VERSION=2024-02-15-preview
FOUNDRY_TIMEOUT_SECONDS=60
FOUNDRY_MAX_RETRIES=2
FOUNDRY_CHAT_COMPLETIONS_PATH=/openai/deployments/{deployment}/chat/completions?api-version={api_version}
```

OpsGPT remains webhook-driven. Admins create a project, add a monitoring source, and configure the generated webhook URL in the monitoring tool:

```text
http://<host>:8002/alerts/webhook/project/{project_id}/{webhook_token}
```

With the included Nginx reverse proxy on port `8080`, use:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

The Nginx configuration is in `nginx/nginx.conf`.

Supported webhook sources include Grafana, Azure Monitor, Prometheus Alertmanager, Datadog, New Relic, Splunk, Elastic / Kibana, Sentry, PagerDuty, AWS CloudWatch, Google Cloud Monitoring, Dynatrace, AppDynamics, Zabbix, Nagios, and Custom Webhook.

Vendor parsers are best-effort in Phase 1. The universal parser stores the full raw payload and extracts normalized fields using recursive alias matching.
