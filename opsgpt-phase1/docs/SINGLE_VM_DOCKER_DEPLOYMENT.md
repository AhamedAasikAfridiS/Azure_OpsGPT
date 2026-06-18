# OpsGPT Phase 1 - Single VM Docker Deployment Guide

## Purpose

This guide explains how to run the complete OpsGPT Phase 1 application on one
publicly reachable Linux VM using Docker Compose.

This setup is intended only for development, demonstrations, and functional
testing. It is not production-ready because it uses:

- Public HTTP ports without TLS
- Wildcard CORS
- Local development accounts
- Docker Compose instead of an orchestrator
- Placeholder secrets unless you replace them
- Publicly reachable application APIs

Do not use this design for production workloads.

## Deployment Layout

```text
Developer Browser
        |
        | HTTP using VM public IP
        v
+------------------------------------------+
| Single Linux VM                          |
|                                          |
| Frontend Service               :3000     |
| Core API Service               :8001     |
| Alert Ingestion Service        :8002     |
| AI Analysis Service            :8003     |
| Notification Service           :8004     |
|                                          |
| Core PostgreSQL DB             internal  |
| Alert PostgreSQL DB            internal  |
| Analysis PostgreSQL DB         internal  |
| Notification PostgreSQL DB     internal  |
+------------------------------------------+
```

Only application ports are published. PostgreSQL ports remain inside the
Docker network.

## 1. VM Requirements

Recommended minimum for a functional test:

- Linux VM such as Ubuntu 22.04 or 24.04
- 4 virtual CPUs
- 8 GB RAM
- 30 GB free disk space
- Public IP address
- SSH access
- Outbound internet access for Docker images and optional hosted AI APIs

Running Ollama on the same VM may require more memory depending on the model.
For a smaller VM, use Gemini or OpenAI instead.

## 2. Allow Required Inbound Ports

Configure the VM provider's firewall or security group to allow:

| Port | Purpose | Recommended source |
| ---: | --- | --- |
| `22` | SSH | Your public IP only |
| `3000` | OpsGPT frontend | Your public IP for testing |
| `8001` | Core API | Your public IP for testing |
| `8002` | Alert webhook receiver | Your public IP and monitoring source |
| `8003` | AI Analysis API docs/debugging | Your public IP only |
| `8004` | Notification API docs/debugging | Your public IP only |
| `4000` | Optional Grafana | Your public IP only |

Do not expose PostgreSQL port `5432`.

Although this is a public VM test, restricting every port to your own public
IP is safer than allowing the entire internet.

## 3. Connect To The VM

Example:

```bash
ssh <vm-user>@<VM_PUBLIC_IP>
```

Replace:

- `<vm-user>` with the VM administrator username
- `<VM_PUBLIC_IP>` with the VM public IP address

## 4. Install Git And Docker

The following Ubuntu commands are documentation examples:

```bash
sudo apt-get update
sudo apt-get install -y git ca-certificates curl
```

Install Docker using the installation method recommended for the VM operating
system. Confirm that Docker and Compose are available:

```bash
docker --version
docker compose version
```

Allow the current user to run Docker without `sudo` if appropriate for the
test environment:

```bash
sudo usermod -aG docker "$USER"
```

Log out and reconnect after changing Docker group membership.

## 5. Copy The OpsGPT Repository

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>/opsgpt-phase1
```

Alternatively, transfer the project directory to the VM using your preferred
secure file-transfer method.

All remaining commands in this guide assume the current directory is:

```text
opsgpt-phase1
```

## 6. Identify The VM Address

Record the address that your browser will use:

```text
VM_PUBLIC_IP=<VM_PUBLIC_IP>
```

Examples:

```text
203.0.113.10
opsgpt-demo.example.com
```

The frontend runs in the user's browser. Therefore, frontend API URLs must use
the VM public IP or DNS name. They must not use `localhost` or Docker service
names.

## 7. Configure Docker Compose For The VM

In `docker-compose.yml`, update the frontend environment values:

```yaml
frontend-service:
  environment:
    VITE_CORE_API_URL: http://<VM_PUBLIC_IP>:8001
    VITE_ALERT_INGESTION_URL: http://<VM_PUBLIC_IP>:8002
```

Replace `<VM_PUBLIC_IP>` with the actual public IP or DNS name.

Example:

```yaml
frontend-service:
  environment:
    VITE_CORE_API_URL: http://203.0.113.10:8001
    VITE_ALERT_INGESTION_URL: http://203.0.113.10:8002
```

These variables are consumed by the Vite frontend when its development server
starts.

The backend services currently allow all CORS origins for Phase 1 testing:

```text
CORS_ORIGINS=*
```

The FastAPI middleware uses wildcard origins with credentials disabled. This
is not production-safe.

## 8. Create The Root Environment File

Create:

```text
opsgpt-phase1/.env
```

Use unique local testing secrets:

```env
JWT_SECRET_KEY=replace-with-a-long-random-development-secret
INTERNAL_API_KEY=replace-with-a-long-random-internal-key

ENABLE_ANALYSIS_FORWARDING=true
ENABLE_NOTIFICATIONS=true

NOTIFICATION_CHANNEL=console
SLACK_WEBHOOK_URL=

AI_PROVIDER=gemini
GEMINI_API_KEY=replace-with-real-gemini-api-key
GEMINI_MODEL=gemini-1.5-flash

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1
```

The same `INTERNAL_API_KEY` is passed by Compose to:

- Core API
- Alert Ingestion
- AI Analysis

Do not commit the populated `.env` file.

## 9. Select An AI Provider

OpsGPT does not use mock AI output. One real provider must be available.

### Option A: Gemini

Recommended for a VM without enough memory for Ollama:

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=replace-with-real-key
GEMINI_MODEL=gemini-1.5-flash
```

### Option B: OpenAI

```env
AI_PROVIDER=openai
OPENAI_API_KEY=replace-with-real-key
OPENAI_MODEL=gpt-4o-mini
```

### Option C: Ollama On The Same VM

Install and start Ollama on the VM using the official Ollama instructions.
Make the Ollama server reachable from Docker containers.

Configure:

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1
```

The Compose configuration maps `host.docker.internal` to the Docker host.
Ensure Ollama listens on an address accessible from Docker, not only a
host-local loopback interface.

Azure OpenAI remains a Phase 2-ready path and is not required here.

## 10. Notification Mode

For initial testing:

```env
ENABLE_NOTIFICATIONS=true
NOTIFICATION_CHANNEL=console
```

Notification messages will appear in the Notification Service logs.

For Slack testing:

```env
ENABLE_NOTIFICATIONS=true
NOTIFICATION_CHANNEL=slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/replace-with-real-value
```

Never commit the Slack webhook URL.

## 11. Prepare A Clean Database

The project currently uses SQLAlchemy `create_all` rather than a migration
tool. If this VM has previously run an older OpsGPT schema, remove the old
local volumes before starting:

```bash
docker compose down -v
```

This deletes all existing OpsGPT data on that VM.

Skip this step for the first deployment.

## 12. Build The Application

```bash
docker compose build
```

The command builds:

- Frontend image
- Core API image
- Alert Ingestion image
- AI Analysis image
- Notification image

Docker also downloads the PostgreSQL image when required.

## 13. Start OpsGPT

Start in attached mode for the first run:

```bash
docker compose up
```

After reviewing startup output, use detached mode:

```bash
docker compose up -d
```

View service status:

```bash
docker compose ps
```

## 14. Open The Application

From your local browser:

```text
Frontend:
http://<VM_PUBLIC_IP>:3000

Core API documentation:
http://<VM_PUBLIC_IP>:8001/docs

Alert Ingestion documentation:
http://<VM_PUBLIC_IP>:8002/docs

AI Analysis documentation:
http://<VM_PUBLIC_IP>:8003/docs

Notification documentation:
http://<VM_PUBLIC_IP>:8004/docs
```

## 15. Login

Use the seeded administrator:

```text
Email: admin@company.com
Password: password123
```

These credentials are for development only.

## 16. Configure A Project

1. Open `Admin Projects`.
2. Create a project.
3. Select `Manage Members`.
4. Search for a junior or senior engineer.
5. Assign the engineer to the project.
6. Open `Monitoring Sources`.
7. Add a Grafana, Azure Monitor, or custom source.

Example source:

```text
Source Type: Grafana
Source Name: VM Grafana Test
Dashboard URL: http://<VM_PUBLIC_IP>:4000/d/<dashboard-id>
Alert Rule URL: http://<VM_PUBLIC_IP>:4000/alerting/grafana/<rule-id>/view
```

OpsGPT will display a webhook URL such as:

```text
http://<VM_PUBLIC_IP>:8002/alerts/webhook/project/PROJ-2026-000001/<token>
```

Dashboard and alert-rule URLs are metadata links. OpsGPT does not scrape them.

## 17. Optional Grafana On The Same VM

Grafana may run separately on the same VM and publish host port `4000`.

From a user's browser:

```text
http://<VM_PUBLIC_IP>:4000
```

If Grafana runs in its own Docker container and is not attached to the
OpsGPT Docker network, configure its webhook contact point with:

```text
http://host.docker.internal:8002/alerts/webhook/project/<PROJECT_ID>/<TOKEN>
```

On Linux, the Grafana container may need:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

If Grafana runs directly as a host process, it can use:

```text
http://localhost:8002/alerts/webhook/project/<PROJECT_ID>/<TOKEN>
```

If Grafana can reach the VM through its public or private address, it may use:

```text
http://<VM_IP>:8002/alerts/webhook/project/<PROJECT_ID>/<TOKEN>
```

## 18. Configure The Grafana Alert

In Grafana:

1. Open `Alerting`.
2. Create a webhook contact point.
3. Paste the generated OpsGPT project webhook URL.
4. Create an alert rule.
5. Attach the contact point through a notification policy.
6. Add labels required by OpsGPT.

Recommended labels:

```text
service=payment-api
severity=critical
environment=production
alert_type=api_latency
```

Recommended annotations:

```text
summary=Payment API latency is above threshold
description=p95 latency is greater than 5 seconds
runbook_url=http://<VM_PUBLIC_IP>:4000/<runbook-path>
```

For the first end-to-end test, use a critical alert. One critical alert is
enough to request incident creation.

## 19. Verify The End-To-End Flow

Expected flow:

```text
Grafana
  -> Alert Ingestion
  -> Core token validation
  -> AI Analysis
  -> Real AI provider
  -> Core incident storage
  -> Frontend project dashboard
  -> Notification Service
```

In the frontend:

1. Select the configured project.
2. Open `Incidents`.
3. Open the new incident.
4. Confirm the AI summary, root cause, evidence, confidence, and recommended
   fix.

## 20. View Logs

All services:

```bash
docker compose logs -f
```

Individual services:

```bash
docker compose logs -f frontend-service
docker compose logs -f core-api-service
docker compose logs -f alert-ingestion-service
docker compose logs -f ai-analysis-service
docker compose logs -f notification-service
```

Console notifications appear in:

```bash
docker compose logs -f notification-service
```

## 21. Restart After Configuration Changes

After changing root `.env` values:

```bash
docker compose down
docker compose up -d
```

After changing frontend environment values or application code:

```bash
docker compose down
docker compose up -d --build
```

Vite environment variables are loaded when the frontend process starts.

## 22. Stop Or Remove The Deployment

Stop containers while preserving database data:

```bash
docker compose down
```

Stop containers and delete all local database data:

```bash
docker compose down -v
```

Remove unused built images only when intentionally cleaning the VM.

## 23. Troubleshooting

### Frontend Loads But API Calls Use Localhost

The frontend was started with local URLs. Set:

```yaml
VITE_CORE_API_URL: http://<VM_PUBLIC_IP>:8001
VITE_ALERT_INGESTION_URL: http://<VM_PUBLIC_IP>:8002
```

Then rebuild the frontend container.

### Browser Reports CORS Errors

Confirm all backend containers were rebuilt after the wildcard CORS change.
Phase 1 middleware allows:

```text
allow_origins=["*"]
allow_credentials=False
allow_methods=["*"]
allow_headers=["*"]
```

Also verify that the API is reachable. Browser network failures are sometimes
reported in a way that resembles CORS errors.

### API Port Is Not Reachable

Check:

- VM provider firewall or security group
- Linux host firewall
- Docker container status
- Correct VM public IP
- Correct published port

### Alert Is Stored But No Incident Is Created

Check:

```env
ENABLE_ANALYSIS_FORWARDING=true
```

Then inspect Alert Ingestion and AI Analysis logs.

### AI Analysis Fails

Check:

- `AI_PROVIDER`
- API key or Ollama connectivity
- Configured model
- VM outbound internet access
- Provider quota

### Project Webhook Returns 401

Check:

- The full generated token was copied
- The project is active
- The monitoring source is active
- `INTERNAL_API_KEY` is consistent across services

### No Notification Appears

Check:

```env
ENABLE_NOTIFICATIONS=true
NOTIFICATION_CHANNEL=console
```

Then inspect Notification Service logs.

## 24. Test Deployment Checklist

- [ ] VM created and reachable through SSH
- [ ] Docker and Docker Compose installed
- [ ] Repository copied to the VM
- [ ] VM firewall ports restricted and opened as required
- [ ] Frontend Compose URLs changed to the VM IP or DNS name
- [ ] Root `.env` created
- [ ] JWT and internal API secrets replaced
- [ ] AI provider configured
- [ ] Analysis forwarding enabled
- [ ] Notifications enabled
- [ ] Docker images built
- [ ] Containers started
- [ ] Frontend reachable on port `3000`
- [ ] Core API reachable on port `8001`
- [ ] Admin login successful
- [ ] Project created
- [ ] Engineer assigned
- [ ] Monitoring source created
- [ ] Project webhook copied
- [ ] Grafana webhook configured
- [ ] Test alert fired
- [ ] Incident visible in the project dashboard
- [ ] AI analysis visible
- [ ] Console or Slack notification delivered
# Current AI and Webhook Note

OpsGPT Phase 1 now uses Microsoft Foundry / Azure AI Foundry only for AI Analysis. Configure `AI_PROVIDER=foundry`, `FOUNDRY_ENDPOINT`, `FOUNDRY_API_KEY`, and `FOUNDRY_MODEL_DEPLOYMENT` before starting the full pipeline.

Project webhooks remain event-driven. With the included Nginx reverse proxy, use:

```text
http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}
```

OpsGPT does not scrape monitoring dashboards. Grafana, Azure Monitor, Datadog, Prometheus Alertmanager, and other tools should send triggered alert webhook payloads.
