# OpsGPT Phase 1 Architecture

## Architecture Style

OpsGPT Phase 1 uses a lightweight event-driven microservices architecture over
synchronous REST APIs.

"Event-driven" describes the business flow: a monitoring event triggers alert
processing, incident analysis, persistence, and notification. Phase 1 uses
direct HTTP calls between services rather than a message broker. A later phase
can replace selected HTTP handoffs with a queue without changing service data
ownership.

## High-Level Flow

```text
Azure Monitor / Grafana / Manual Submission
                    |
                    v
          Alert Ingestion Service
                    |
                    v
           AI Analysis Service
                    |
                    v
             Core API Service
              |            |
              v            v
      Frontend Service   Notification Service
                               |
                               v
                         Console or Slack
```

## Monitoring Integration

Grafana, Azure Monitor, and similar monitoring tools continuously observe
applications, infrastructure, metrics, logs, and health signals.

When a configured alert rule fires, the monitoring tool sends an HTTP webhook
to Alert Ingestion Service. OpsGPT processes that triggered payload.

OpsGPT does not:

- Scrape Grafana dashboards
- Poll Azure Monitor dashboards
- Read chart pixels
- Continuously query the monitoring user interface
- Replace the monitoring platform

The monitoring platform detects the condition. OpsGPT begins its work after it
receives the alert webhook.

## Processing Stages

### 1. Alert Reception

Alert Ingestion accepts Azure Monitor Common Alert Schema payloads, Grafana
webhooks, and manual alert requests. It stores the original JSON before
normalization so rejected payloads remain auditable.

### 2. Normalization

Source-specific parsers convert alerts into one common schema containing the
service, environment, alert type, severity, message, metrics, resource links,
and timestamps.

### 3. Correlation and AI Analysis

AI Analysis stores normalized alerts, detects duplicates, and groups related
alerts by:

- Service name
- Environment
- Correlation time window
- Related alert types
- Same or nearby severity

It then calls the configured real AI provider for structured JSON containing
the summary, root cause, evidence, confidence score, and recommendations.

### 4. Incident Ownership

AI Analysis never writes to the Core database. It calls Core API internal REST
endpoints using the shared `X-Internal-API-Key`.

Core API owns:

- Users and roles
- Incidents
- Status and resolution data
- Timelines
- Audit logs
- Knowledge-base entries

### 5. User Experience

The React frontend authenticates with Core API and displays dashboards,
incidents, AI analysis, timelines, knowledge entries, and profile information.
Senior engineers and admins receive incident editing controls. Junior
engineers receive a read-only interface.

### 6. Notification

When enabled, Core API sends complete event payloads to Notification Service.
Notification Service formats the event and delivers it through the configured
console or Slack channel. It stores both the notification and every delivery
attempt.

## Data Ownership

Each backend service owns one PostgreSQL database:

| Service | Database | Owned Data |
| --- | --- | --- |
| Core API | `core-db` | Users, incidents, status, timeline, notes, audits, knowledge base |
| Alert Ingestion | `alert-db` | Raw alerts, normalized alerts, ingestion logs |
| AI Analysis | `analysis-db` | Analysis alerts, correlation groups, results, analysis logs |
| Notification | `notification-db` | Notifications, attempts, template records |

Services communicate through APIs instead of reading another service's
database.

## Local Network

Docker Compose places every container on `opsgpt-network`. Docker DNS resolves
service names such as:

```text
core-api-service
alert-ingestion-service
ai-analysis-service
notification-service
core-db
alert-db
analysis-db
notification-db
```

Only application ports are published to the host. Database ports remain
internal.
