# OpsGPT - Phase 1 Microservices Application README

## 1. Project Name

**OpsGPT - AI First Responder for Production Incidents**

---

## 2. Project Overview

OpsGPT is an AI-powered incident management platform designed to help DevOps, SRE, Cloud Engineering, and Operations teams detect, analyze, investigate, and resolve infrastructure or application incidents faster.

Modern cloud and enterprise environments generate many alerts every day. Engineers often spend a lot of time identifying duplicate alerts, understanding whether alerts are related, determining the real impact, finding the possible root cause, and deciding the correct remediation steps.

OpsGPT addresses this problem by combining:

- Alert ingestion
- Alert correlation
- AI-powered incident summaries
- Root cause analysis
- Fix recommendations
- Incident management
- Knowledge base reuse
- Slack notifications

The application acts as an intelligent first responder for production incidents.

---

## 3. Problem Statement

Large cloud and infrastructure environments commonly face:

- Alert fatigue
- Duplicate alerts
- Multiple alerts for the same issue
- Slow incident triage
- Delayed root cause identification
- Knowledge silos
- Manual troubleshooting processes
- Slow communication between teams

These problems increase:

- **MTTD** - Mean Time To Detect
- **MTTR** - Mean Time To Resolve

OpsGPT is designed to reduce both.

---

## 4. Proposed Solution

OpsGPT provides a centralized incident management platform that can:

- Receive alerts from monitoring tools
- Validate and normalize alerts
- Group related alerts into a single incident
- Generate AI-based incident summaries
- Identify probable root causes
- Recommend immediate and long-term fixes
- Notify engineering teams through Slack
- Store resolved incidents in a knowledge base
- Help engineers find similar previous incidents

---

## 5. Business Goals

The primary goals of OpsGPT are:

- Reduce alert noise
- Improve operational visibility
- Accelerate incident response
- Reduce downtime
- Preserve organizational knowledge
- Improve engineering productivity
- Help junior and senior engineers investigate incidents faster
- Provide consistent troubleshooting guidance

---

## 6. Target Users

OpsGPT is an internal organization application intended for technical teams such as:

- Junior DevOps engineers
- Senior DevOps engineers
- Cloud engineers
- Site Reliability Engineers
- Operations engineers
- Platform engineers
- Admin users

---

## 7. Phase 1 Scope

Phase 1 focuses only on **local application development and testing**.

### Included in Phase 1

- Microservices-based application structure
- FastAPI backend services
- Basic React frontend
- Local authentication using JWT
- Role-based access control
- Alert ingestion APIs
- Manual alert submission
- Azure Monitor-style alert simulation
- Grafana-style alert simulation
- Alert validation and normalization
- Alert correlation
- AI incident summary generation using a real AI provider
- Root cause analysis generation using a real AI provider
- Fix recommendation generation using a real AI provider
- Incident dashboard APIs
- Incident detail APIs
- Knowledge base APIs
- Similar incident search logic
- Slack notification support
- Dockerfiles and Docker Compose support
- `.env`-based configuration

### Not Included in Phase 1

- Azure deployment
- Azure App Service
- Azure Service Bus
- Azure OpenAI integration
- Microsoft Entra ID integration
- Azure Monitor live integration
- Production-grade Kubernetes setup
- Advanced RAG/vector search
- Real-time WebSocket updates
- Complex notification preferences

Azure OpenAI and cloud integration are planned for later phases.

---

## 8. Architecture Style

OpsGPT follows a **lightweight event-driven microservices architecture**.

The application is intentionally limited to 5 services to avoid unnecessary complexity.

### Planned Services

1. Frontend Service
2. Core API Service
3. Alert Ingestion Service
4. AI Analysis Service
5. Notification Service

---

## 9. High-Level Architecture Flow

```text
Monitoring Tool / Manual Input
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
        +------------------> Notification Service ---> Slack
        |
        v
Frontend Service
```

### User-facing flow

```text
User Browser
    |
    v
Frontend Service
    |
    v
Core API Service
    |
    v
Core Database
```

### Alert processing flow

```text
Alert Source
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
Notification Service
```

---

## 10. Functional Requirements

## 10.1 Authentication and Authorization

### Features

- User login
- User profile management
- Role-Based Access Control
- Protected APIs
- Role-based frontend actions

### Roles

#### Junior Engineer

Junior engineers are read-only users.

Can:

- View incidents
- View AI summaries
- View RCA reports
- View recommended fixes
- View knowledge base
- View similar incidents

Cannot:

- Modify incident status
- Resolve incidents
- Add resolution notes
- Update incident records

#### Senior Engineer

Senior engineers can investigate and manage incidents.

Can:

- Perform all junior engineer actions
- Update incident status
- Mark incidents as resolved
- Add resolution notes
- Update incident records

#### Admin

Admins can perform senior engineer actions and may manage users/roles in later phases.

Can:

- Perform all senior engineer actions
- Manage incident records
- Access audit logs
- Manage users/roles if implemented

---

## 10.2 Alert Ingestion

### Features

- Azure Monitor-style webhook endpoint
- Grafana-style webhook endpoint
- Manual alert submission
- Alert validation
- Alert parsing
- Alert normalization
- Raw alert storage
- Forwarding valid alerts to AI Analysis Service

### Supported Alert Types

- CPU alerts
- Memory alerts
- Application error alerts
- API latency alerts
- Database alerts
- Custom alerts

---

## 10.3 Incident Dashboard

### Features

- Active incidents
- Resolved incidents
- Critical incidents
- Incident timeline
- Severity view
- Status tracking
- Search and filters

### Filters

- Open
- In Progress
- Resolved
- Critical
- Warning
- Informational

---

## 10.4 Alert Correlation Engine

### Features

- Duplicate detection
- Similar alert grouping
- Alert noise reduction
- Automatic incident creation

### Phase 1 Correlation Rule

For Phase 1, correlation can be rule-based:

```text
same service_name + same environment + close time window = same incident group
```

Example:

```text
CPU alert + API latency alert + DB timeout alert + HTTP 500 alert
for payment-api within 10 minutes
= one correlated incident
```

---

## 10.5 AI Incident Summary

### Features

- Incident overview
- Business impact explanation
- Affected service identification
- Severity explanation

The summary should be generated using a real AI provider in Phase 1.

Supported Phase 1 AI provider options:

- Local Ollama model
- Gemini API
- OpenAI / ChatGPT API

Azure OpenAI is planned for Phase 2.

---

## 10.6 Root Cause Analysis Engine

### Features

- Probable root cause identification
- Supporting evidence collection
- Confidence scoring

Example output:

```text
Root Cause:
PostgreSQL connection pool exhaustion

Confidence:
92%

Supporting Evidence:
- Database timeout alerts
- API latency increase
- CPU spike
- Increased HTTP 500 errors
```

---

## 10.7 AI Fix Recommendation Engine

### Features

- Immediate remediation actions
- Long-term recommendations
- Runbook suggestions

Example output:

```text
Immediate Actions:
1. Restart payment-api service
2. Increase connection pool size
3. Review active database sessions

Long-Term Actions:
1. Optimize slow queries
2. Implement connection pooling
3. Configure autoscaling
```

---

## 10.8 Incident Detail Page

### Features

- Alert information
- AI summary
- Root cause analysis
- Recommended fixes
- Incident timeline
- Status management
- Resolution notes
- Similar incidents
- Historical resolutions

---

## 10.9 Incident Knowledge Base

### Features

- Historical incidents
- Previous RCA reports
- Resolution notes
- Runbooks
- Troubleshooting documentation

The knowledge base acts as the organization's operational memory.

When an incident is resolved, important information should be stored for future reference.

---

## 10.10 Similar Incident Search

### Features

- Incident similarity detection
- Similarity percentage
- Previous RCA comparison
- Previous fix suggestions

### Phase 1 Similarity Logic

For Phase 1, similarity can be simple and rule-based:

```text
+40 points if same service_name
+30 points if similar root cause
+20 points if same alert type
+10 points if same severity
```

Later, this can be replaced with vector search or RAG.

---

## 10.11 Slack Notification Service

### Features

- New incident notifications
- Critical incident alerts
- AI summary notifications
- RCA notifications
- Fix recommendation notifications
- Incident status update notifications
- Incident resolved notifications

---

# 11. Microservices Description

---

# 11.1 Frontend Service

## What It Is

The Frontend Service is the user-facing web application of OpsGPT.

It is built using basic React and provides screens for engineers to view, investigate, and manage incidents.

## Purpose

The purpose of the Frontend Service is to act as the control room for incident investigation.

Users can open OpsGPT in the browser and interact with the incident management system.

## Main Responsibilities

- Login page
- User profile page
- Dashboard page
- Incident list page
- Incident detail page
- Knowledge base page
- Similar incident view
- Role-based UI behavior
- Status update form
- Resolution notes form

## Browser Routes

```text
/login
/dashboard
/incidents
/incidents/:incidentId
/knowledge-base
/profile
```

## APIs Consumed

The Frontend Service mainly consumes APIs from the Core API Service.

```http
POST /auth/login
GET  /auth/me
GET  /dashboard/summary
GET  /incidents
GET  /incidents/{incident_id}
PATCH /incidents/{incident_id}/status
POST /incidents/{incident_id}/resolution-notes
GET  /knowledge-base
GET  /incidents/{incident_id}/similar
```

## Dependencies

The Frontend Service depends on:

```text
Core API Service
```

Correct dependency:

```text
Frontend Service -> Core API Service
```

The frontend should not directly call:

- Alert Ingestion Service
- AI Analysis Service
- Notification Service

## Role-Based UI Behavior

### Junior Engineer

Hide or disable:

- Mark as In Progress button
- Mark as Resolved button
- Add Resolution Notes form

### Senior Engineer and Admin

Show:

- Mark as In Progress button
- Mark as Resolved button
- Add Resolution Notes form

## Flexibility Requirement

The frontend should be flexible for future updates.

Recommended structure:

```text
frontend/
  src/
    api/
      authApi.js
      incidentApi.js
      dashboardApi.js
      knowledgeBaseApi.js
    components/
      Navbar.jsx
      IncidentCard.jsx
      SeverityBadge.jsx
      StatusBadge.jsx
      LoadingSpinner.jsx
    pages/
      LoginPage.jsx
      DashboardPage.jsx
      IncidentsPage.jsx
      IncidentDetailPage.jsx
      KnowledgeBasePage.jsx
      ProfilePage.jsx
    context/
      AuthContext.jsx
    routes/
      AppRoutes.jsx
      ProtectedRoute.jsx
    utils/
      constants.js
      roleUtils.js
    App.jsx
    main.jsx
```

## What This Service Should Not Do

The Frontend Service should not:

- Validate raw monitoring alerts
- Store raw alerts
- Correlate alerts
- Generate AI summaries
- Generate RCA
- Generate fix recommendations
- Send Slack notifications
- Directly update databases

---

# 11.2 Core API Service

## What It Is

The Core API Service is the main backend service of OpsGPT.

It manages user-facing application data and provides APIs for the frontend.

## Purpose

The purpose of the Core API Service is to provide a single clean backend API layer for the frontend.

It manages:

- Authentication
- User profiles
- RBAC
- Incidents
- Dashboard data
- Status updates
- Resolution notes
- Audit logs
- Knowledge base

## Main Responsibilities

- User authentication
- User profile management
- Role-Based Access Control
- Incident CRUD operations
- Incident status management
- Resolution notes
- Dashboard summary APIs
- Incident timeline
- Audit logging
- Knowledge base APIs
- Similar incident search API wrapper
- Internal APIs for AI Analysis Service
- Notification event trigger

## Public API Endpoints

### Authentication APIs

```http
POST /auth/login
GET  /auth/me
POST /auth/logout
```

### User APIs

```http
GET   /users/me
GET   /users
POST  /users
PATCH /users/{user_id}/role
```

### Dashboard APIs

```http
GET /dashboard/summary
GET /dashboard/severity-counts
GET /dashboard/status-counts
GET /dashboard/recent-incidents
```

### Incident APIs

```http
GET   /incidents
GET   /incidents/{incident_id}
PATCH /incidents/{incident_id}/status
POST  /incidents/{incident_id}/resolution-notes
GET   /incidents/{incident_id}/timeline
GET   /incidents/{incident_id}/similar
```

### Knowledge Base APIs

```http
GET  /knowledge-base
GET  /knowledge-base/{kb_id}
POST /knowledge-base
```

### Audit Log APIs

```http
GET /audit-logs
GET /audit-logs?incident_id=INC-2026-001
```

## Internal API Endpoints

These APIs are used by other microservices, not directly by frontend users.

```http
POST  /internal/incidents
PATCH /internal/incidents/{incident_id}/analysis
POST  /internal/incidents/{incident_id}/timeline
POST  /internal/notifications/events
```

## Data Owned By Core API Service

Recommended tables:

```text
users
roles
incidents
incident_status_history
incident_timeline
resolution_notes
audit_logs
knowledge_base
```

## Database Responsibility

The Core API Service owns the main incident management database.

It should be the source of truth for:

- Users
- Roles
- Incidents
- Incident status
- Resolution notes
- Timeline
- Audit logs
- Knowledge base

## Dependencies

The Core API Service depends on:

- Core database
- AI Analysis Service indirectly through internal APIs
- Notification Service for notification events

Recommended dependency flow:

```text
Frontend Service -> Core API Service
AI Analysis Service -> Core API Service
Core API Service -> Notification Service
```

## What This Service Should Not Do

The Core API Service should not:

- Receive raw Azure Monitor or Grafana alerts directly
- Parse monitoring payloads
- Normalize raw alerts
- Generate AI summaries
- Generate RCA
- Generate fix recommendations
- Send Slack messages directly
- Run long background AI jobs

---

# 11.3 Alert Ingestion Service

## What It Is

The Alert Ingestion Service is the entry point for monitoring alerts.

It receives alerts from monitoring tools or manual submissions.

## Purpose

The purpose of this service is to safely receive, validate, parse, normalize, store, and forward alert data for analysis.

It acts as the front gate for all alerts entering OpsGPT.

## Main Responsibilities

- Receive webhook alerts
- Receive manually submitted alerts
- Validate required fields
- Parse different alert formats
- Normalize alerts into one internal format
- Store raw alert payloads
- Store normalized alert records
- Reject invalid alerts
- Forward valid alerts to AI Analysis Service
- Track alert ingestion status

## API Endpoints

```http
POST /alerts/webhook/azure-monitor
POST /alerts/webhook/grafana
POST /alerts/manual
GET  /alerts
GET  /alerts/{alert_id}
GET  /alerts/{alert_id}/raw
GET  /health
```

## Example Normalized Alert Format

```json
{
  "alert_id": "ALT-2026-001",
  "source": "azure_monitor",
  "service_name": "payment-api",
  "alert_type": "cpu",
  "severity": "critical",
  "message": "CPU usage exceeded 95%",
  "metric_name": "CPU Percentage",
  "metric_value": 96,
  "environment": "production",
  "created_at": "2026-06-11T10:00:00"
}
```

## Validation Rules

Minimum required fields after parsing:

```text
service_name
severity
message
source
alert_type
```

Allowed severities:

```text
critical
warning
informational
```

Allowed alert types:

```text
cpu
memory
application_error
api_latency
database
custom
```

## Data Owned By Alert Ingestion Service

Recommended tables:

```text
raw_alerts
normalized_alerts
alert_ingestion_logs
```

## Dependencies

The Alert Ingestion Service depends on:

- Its own database
- AI Analysis Service

Recommended flow:

```text
Monitoring Tool / Manual Input
        |
        v
Alert Ingestion Service
        |
        v
AI Analysis Service
```

## What This Service Should Not Do

The Alert Ingestion Service should not:

- Create incidents directly
- Generate AI summaries
- Generate RCA
- Generate fix recommendations
- Send Slack notifications
- Manage users
- Manage RBAC
- Update incident status
- Store resolution notes

Its job is only:

```text
Receive -> Validate -> Parse -> Normalize -> Store -> Forward
```

## Recommended Folder Structure

```text
alert-ingestion-service/
  app/
    main.py
    api/
      routes/
        alert_routes.py
        health_routes.py
    core/
      config.py
    schemas/
      alert_schema.py
      azure_monitor_schema.py
      grafana_schema.py
      manual_alert_schema.py
    models/
      raw_alert.py
      normalized_alert.py
      ingestion_log.py
    services/
      alert_validation_service.py
      alert_normalization_service.py
      alert_forwarder_service.py
      alert_storage_service.py
    parsers/
      azure_monitor_parser.py
      grafana_parser.py
      manual_parser.py
    db/
      database.py
    utils/
      id_generator.py
      severity_mapper.py
      alert_type_mapper.py
```

---

# 11.4 AI Analysis Service

## What It Is

The AI Analysis Service is the intelligence layer of OpsGPT.

It receives normalized alerts from the Alert Ingestion Service and performs correlation, summary generation, root cause analysis, fix recommendation, and similar incident search logic.

## Purpose

The purpose of this service is to reduce manual investigation work for engineers.

It helps answer:

- Is this alert duplicate?
- Is this alert related to an existing incident?
- Should a new incident be created?
- What is the incident summary?
- What is the likely root cause?
- What is the confidence score?
- What fix should be recommended?
- Are there similar previous incidents?

## Main Responsibilities

- Receive normalized alerts from Alert Ingestion Service
- Store alerts for analysis
- Detect duplicate alerts
- Group related alerts
- Decide whether to create a new incident or update an existing incident
- Generate incident title
- Generate incident severity
- Generate AI incident summary
- Generate probable root cause
- Generate supporting evidence
- Generate confidence score
- Generate fix recommendations
- Search similar historical incidents
- Send final incident data to Core API Service

## Important AI Provider Decision

The AI Analysis Service should **not use mock AI providers**.

Phase 1 should use a real configurable AI provider.

Supported Phase 1 options:

- Local Ollama model
- Gemini API
- OpenAI / ChatGPT API

Phase 2 target:

- Azure OpenAI

## AI Provider Configuration

The active AI provider should be controlled using environment variables.

Example:

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# or

AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-model-name

# or

AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-model-name
```

## Recommended AI Client Structure

```text
ai_clients/
  base_ai_client.py
  ollama_client.py
  gemini_client.py
  openai_client.py
  azure_openai_client.py
```

`azure_openai_client.py` can be kept migration-ready for Phase 2.

## API Endpoints

```http
POST /analysis/alerts
POST /analysis/correlate
POST /analysis/generate-summary
POST /analysis/generate-rca
POST /analysis/generate-fix
POST /analysis/similar-incidents
GET  /analysis/incidents/{incident_id}
GET  /analysis/health
```

## Main Endpoint: Receive Alert

```http
POST /analysis/alerts
```

This endpoint is called by the Alert Ingestion Service.

## Correlation Logic

For Phase 1, correlation can be rule-based.

Recommended rule:

```text
Group alerts together if:
1. Same service_name
2. Same environment
3. Similar time window
4. Related alert types
5. Same or close severity
```

Example:

```text
payment-api CPU alert
payment-api API latency alert
payment-api database timeout alert
payment-api HTTP 500 alert
```

These should be grouped into one incident:

```text
Incident: Payment API degraded performance
Severity: Critical
Status: Open
```

## AI Analysis Workflow

```text
1. Alert Ingestion sends normalized alert.
2. AI Analysis stores the alert.
3. AI Analysis correlates related alerts.
4. AI Analysis prepares structured prompt.
5. AI Analysis sends prompt to selected real AI provider.
6. AI provider returns summary, RCA, confidence score, and fixes.
7. AI Analysis validates and cleans AI output.
8. AI Analysis sends final incident result to Core API.
```

## Data Owned By AI Analysis Service

Recommended tables:

```text
analysis_alerts
correlation_groups
analysis_results
```

## Dependencies

The AI Analysis Service depends on:

- Alert Ingestion Service
- Core API Service
- Its own database
- Configured AI provider

Recommended dependency flow:

```text
Alert Ingestion Service -> AI Analysis Service -> Core API Service
```

The AI Analysis Service should not directly write to the Core API database.

Correct:

```text
AI Analysis Service -> Core API internal API -> Core Database
```

Avoid:

```text
AI Analysis Service -> Core Database directly
```

## Similar Incident Search Responsibility

For Phase 1:

```text
Core API owns knowledge base data.
AI Analysis performs similarity logic.
```

Flow:

```text
Frontend asks Core API:
GET /incidents/{incident_id}/similar

Core API asks AI Analysis:
POST /analysis/similar-incidents

AI Analysis compares current incident with historical incidents.
Core API returns result to frontend.
```

## What This Service Should Not Do

The AI Analysis Service should not:

- Receive raw Azure Monitor or Grafana alerts directly
- Parse source-specific webhook payloads
- Manage login
- Manage RBAC
- Update incident status from frontend
- Store resolution notes
- Own dashboard APIs
- Send Slack messages directly
- Directly modify Core API database

Its job is:

```text
Analyze alerts -> correlate -> summarize -> identify RCA -> recommend fix -> send result to Core API
```

## Recommended Folder Structure

```text
ai-analysis-service/
  app/
    main.py
    api/
      routes/
        analysis_routes.py
        health_routes.py
    core/
      config.py
    schemas/
      alert_schema.py
      correlation_schema.py
      analysis_schema.py
      incident_schema.py
    models/
      analysis_alert.py
      correlation_group.py
      analysis_result.py
    services/
      correlation_service.py
      summary_service.py
      rca_service.py
      fix_recommendation_service.py
      similar_incident_service.py
      core_api_client.py
    ai_clients/
      base_ai_client.py
      ollama_client.py
      gemini_client.py
      openai_client.py
      azure_openai_client.py
    rules/
      rca_rules.py
      fix_rules.py
      severity_rules.py
    db/
      database.py
    utils/
      id_generator.py
      time_window.py
```

---

# 11.5 Notification Service

## What It Is

The Notification Service is responsible for sending incident updates to engineering teams.

In Phase 1, the main notification channel is Slack.

## Purpose

The purpose of this service is to make sure engineers are informed quickly when important incident events happen.

Example events:

- Incident created
- Critical incident detected
- AI analysis completed
- RCA generated
- Fix recommendation generated
- Incident status updated
- Incident resolved

## Main Responsibilities

- Receive notification events from Core API Service
- Format Slack messages
- Send Slack notifications
- Store notification history
- Track delivery status
- Retry failed notifications
- Support multiple notification event types
- Keep future support ready for Teams/email

## API Endpoints

```http
POST /notifications/events
POST /notifications/slack/test
GET  /notifications
GET  /notifications/{notification_id}
GET  /notifications/incident/{incident_id}
GET  /health
```

## Main Endpoint

```http
POST /notifications/events
```

This endpoint is called by the Core API Service.

Example event:

```json
{
  "event_type": "incident_created",
  "incident_id": "INC-2026-001",
  "service_name": "payment-api",
  "severity": "critical",
  "status": "open",
  "title": "Payment API degraded performance",
  "ai_summary": "Payment API is experiencing degraded performance due to database connectivity issues.",
  "root_cause": "PostgreSQL connection pool exhaustion",
  "confidence_score": 92
}
```

## Notification Event Types

Recommended event types:

```text
incident_created
critical_incident_created
ai_analysis_completed
incident_status_updated
incident_resolved
resolution_notes_added
```

For Phase 1, start with:

```text
incident_created
ai_analysis_completed
incident_status_updated
incident_resolved
```

## Slack Message Example

```text
🚨 Critical Incident Detected

Incident ID: INC-2026-001
Service: payment-api
Severity: Critical
Likely Root Cause: PostgreSQL connection pool exhaustion
Confidence: 92%

Recommended Fix:
Increase connection pool size and restart payment-api service.
```

## Slack Configuration

Example `.env`:

```env
NOTIFICATION_CHANNEL=slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
NOTIFICATION_RETRY_COUNT=3
NOTIFICATION_TIMEOUT_SECONDS=10
```

For local testing, support console mode:

```env
NOTIFICATION_CHANNEL=console
```

## Data Owned By Notification Service

Recommended tables:

```text
notifications
notification_delivery_attempts
notification_templates
```

## Dependencies

The Notification Service depends on:

- Core API Service
- Slack webhook
- Its own database

Recommended dependency:

```text
Core API Service -> Notification Service -> Slack
```

The Notification Service should receive complete event payloads from Core API.

Good design:

```text
Core API sends complete notification event.
Notification Service formats and sends message.
```

Avoid:

```text
Core API sends only incident_id.
Notification Service calls Core API again for every detail.
```

## What This Service Should Not Do

The Notification Service should not:

- Receive raw monitoring alerts
- Validate Azure Monitor or Grafana payloads
- Correlate alerts
- Generate AI summaries
- Generate RCA
- Generate fix recommendations
- Manage user login
- Manage RBAC
- Update incident status
- Store resolution notes as source of truth

Its job is:

```text
Receive notification event -> format message -> send notification -> store delivery status
```

## Recommended Folder Structure

```text
notification-service/
  app/
    main.py
    api/
      routes/
        notification_routes.py
        health_routes.py
    core/
      config.py
    schemas/
      notification_schema.py
      slack_schema.py
    models/
      notification.py
      delivery_attempt.py
    services/
      notification_service.py
      template_service.py
      retry_service.py
    channels/
      base_channel.py
      slack_channel.py
      console_channel.py
    db/
      database.py
    utils/
      id_generator.py
      message_formatter.py
```

---

# 12. End-to-End Incident Scenario

## Scenario

A critical issue occurs in the organization's Payment API service.

The application begins experiencing:

- High CPU utilization
- Increased API latency
- Database connection failures
- HTTP 500 errors

Monitoring tools detect these abnormal conditions and send alerts to OpsGPT.

---

## Step 1 - Alert Detection

Monitoring tools generate alerts:

```text
Alert 1: CPU Usage > 95%
Alert 2: API Response Time > 5 Seconds
Alert 3: Database Connection Timeout
Alert 4: HTTP 500 Error Rate Increased
```

---

## Step 2 - Alert Ingestion

The Alert Ingestion Service receives the alerts.

It performs:

- Payload validation
- Alert parsing
- Alert normalization
- Raw alert storage
- Forwarding to AI Analysis Service

---

## Step 3 - Alert Correlation

The AI Analysis Service receives normalized alerts.

It identifies that all alerts belong to the same service:

```text
payment-api
```

Instead of creating four incidents, OpsGPT creates one incident:

```text
Incident ID: INC-2026-001
Severity: Critical
Status: Open
```

---

## Step 4 - AI Incident Summary

The configured AI provider generates an incident summary.

Example:

```text
Payment API is experiencing degraded performance due to database connectivity issues. Multiple alerts indicate elevated latency, increased error rates, and resource exhaustion.
```

---

## Step 5 - Root Cause Analysis

OpsGPT performs RCA generation.

Example:

```text
Likely Root Cause:
PostgreSQL connection pool exhaustion

Supporting Evidence:
- Database timeout alerts
- API latency increase
- CPU spike
- Increased HTTP 500 errors

Confidence Score:
92%
```

---

## Step 6 - Fix Recommendation

OpsGPT generates remediation guidance.

Example:

```text
Immediate Actions:
1. Restart payment-api service
2. Increase connection pool size
3. Review active database sessions

Long-Term Actions:
1. Optimize slow queries
2. Implement connection pooling
3. Configure autoscaling
```

---

## Step 7 - Incident Storage

The AI Analysis Service sends final incident information to the Core API Service.

The Core API Service stores:

- Incident details
- Related alerts
- AI summary
- Root cause
- Confidence score
- Recommended fixes
- Timeline events

---

## Step 8 - Slack Notification

The Core API Service sends a notification event to the Notification Service.

The Notification Service sends a Slack message:

```text
🚨 Critical Incident Detected

Incident ID: INC-2026-001
Service: payment-api
Severity: Critical
Likely Root Cause: PostgreSQL connection pool exhaustion
Confidence: 92%
Recommended Fix: Increase connection pool and restart service
```

---

## Step 9 - Engineer Investigation

An engineer receives the Slack notification and opens OpsGPT.

The dashboard displays:

- Active incident count
- Critical incident count
- Incident timeline
- Severity information

The engineer selects:

```text
INC-2026-001
```

---

## Step 10 - Incident Detail View

The Incident Detail Page displays:

- Alert information
- AI summary
- Root cause analysis
- Recommended fixes
- Similar incidents
- Historical resolutions
- Timeline
- Status

The engineer reviews the information and applies the recommended fix.

---

## Step 11 - Incident Resolution

After remediation:

- Database connections recover
- API latency returns to normal
- Error rates decrease

A senior engineer or admin marks the incident as resolved.

The Core API records:

- Resolution timestamp
- Resolution notes
- User information
- Audit log entry
- Timeline event

---

## Step 12 - Knowledge Base Update

The resolved incident is stored in the Incident Knowledge Base.

Stored information:

- Incident summary
- Root cause
- Resolution notes
- Fix recommendations
- Timeline

Future incidents can reuse this knowledge through Similar Incident Search.

---

# 13. Service Dependency Summary

| Service | Depends On | Should Not Depend On |
|---|---|---|
| Frontend Service | Core API Service | Alert Ingestion, AI Analysis, Notification directly |
| Core API Service | Core DB, Notification Service | Raw alert sources |
| Alert Ingestion Service | Ingestion DB, AI Analysis Service | Core API for incident creation, Notification Service |
| AI Analysis Service | Analysis DB, AI Provider, Core API Service | Frontend, Core DB directly, Notification directly |
| Notification Service | Notification DB, Slack webhook | Raw alerts, AI provider, frontend |

---

# 14. Data Ownership Summary

| Service | Owns Data |
|---|---|
| Frontend Service | No database; UI state only |
| Core API Service | Users, roles, incidents, status history, timeline, resolution notes, audit logs, knowledge base |
| Alert Ingestion Service | Raw alerts, normalized alerts, ingestion logs |
| AI Analysis Service | Analysis alerts, correlation groups, analysis results |
| Notification Service | Notifications, delivery attempts, templates |

---

# 15. Recommended Technology Stack

## Frontend

- React
- React Router
- Axios or Fetch
- Basic CSS or Tailwind CSS

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- JWT authentication for Phase 1

## AI Provider Options

- Ollama for local model inference
- Gemini API
- OpenAI / ChatGPT API
- Azure OpenAI in Phase 2

## Notification

- Slack webhook
- Console notification mode for local testing

## Development and Containerization

- Docker
- Docker Compose
- `.env` files for secrets and configuration

---

# 16. Recommended Repository Structure

```text
opsgpt/
  frontend/
  core-api-service/
  alert-ingestion-service/
  ai-analysis-service/
  notification-service/
  docker-compose.yml
  README.md
  .env.example
```

Each backend microservice should have its own:

```text
app/
requirements.txt
Dockerfile
.env.example
README.md
```

---

# 17. Phase 1 Communication Style

Since Phase 1 avoids cloud integration, use simple local service communication.

Recommended communication:

```text
Frontend -> Core API: REST API
Alert Ingestion -> AI Analysis: REST API
AI Analysis -> Core API: Internal REST API
Core API -> Notification Service: REST API
Notification Service -> Slack: Webhook
```

In later phases, some internal communication can be moved to Azure Service Bus.

---

# 18. Environment Configuration Plan

Use `.env` files for secrets and service configuration.

Example root `.env` values:

```env
# General
ENVIRONMENT=development

# Core API
CORE_API_PORT=8000
CORE_DATABASE_URL=postgresql://user:password@core-db:5432/core_db
JWT_SECRET_KEY=change-this-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Alert Ingestion
ALERT_INGESTION_PORT=8001
ALERT_DATABASE_URL=postgresql://user:password@alert-db:5432/alert_db
AI_ANALYSIS_SERVICE_URL=http://ai-analysis-service:8002

# AI Analysis
AI_ANALYSIS_PORT=8002
ANALYSIS_DATABASE_URL=postgresql://user:password@analysis-db:5432/analysis_db
CORE_API_INTERNAL_URL=http://core-api-service:8000
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1

# Notification
NOTIFICATION_PORT=8003
NOTIFICATION_DATABASE_URL=postgresql://user:password@notification-db:5432/notification_db
NOTIFICATION_CHANNEL=slack
SLACK_WEBHOOK_URL=your-slack-webhook-url
```

Secrets should not be hardcoded in source code.

---

# 19. Development Principles

The codebase should be:

- Easy to understand
- Easy to maintain
- Easy to test
- Easy to extend
- Microservice boundaries should be clear
- Each service should own its own responsibility
- APIs should use clean request and response schemas
- Business logic should stay inside service classes
- Routes should remain thin
- Configuration should come from environment variables
- Future cloud migration should be possible without rewriting the full application

---

# 20. Important Design Rules

## Rule 1: Frontend talks only to Core API

```text
Frontend -> Core API
```

The frontend should not directly call all backend microservices.

## Rule 2: Alert Ingestion does not create incidents

```text
Alert Ingestion -> AI Analysis
```

Alert Ingestion only receives, validates, normalizes, stores, and forwards alerts.

## Rule 3: AI Analysis does not directly write to Core DB

```text
AI Analysis -> Core API internal APIs -> Core DB
```

Core API owns incident data.

## Rule 4: Notification Service only sends notifications

```text
Core API -> Notification Service -> Slack
```

Notification Service should not manage incidents or AI logic.

## Rule 5: Use real AI providers in Phase 1

Do not use mock AI providers.

Allowed Phase 1 providers:

- Ollama
- Gemini
- OpenAI / ChatGPT API

Phase 2 target:

- Azure OpenAI

---

# 21. Final Phase 1 Application Understanding

OpsGPT Phase 1 is a local microservices-based incident management application.

The application receives monitoring alerts, validates and normalizes them, analyzes them using AI, creates meaningful incidents, shows them in a dashboard, recommends fixes, notifies engineers, and stores resolved incidents in a knowledge base.

The system is designed with 5 microservices only:

```text
1. Frontend Service
2. Core API Service
3. Alert Ingestion Service
4. AI Analysis Service
5. Notification Service
```

Each service has a clear responsibility.

The main objective of Phase 1 is to build a working, maintainable, and testable application before moving into cloud deployment and Azure integrations.

---

# 22. Future Enhancements

Possible future enhancements:

- Microsoft Entra ID authentication
- Azure OpenAI integration
- Azure Service Bus event-driven communication
- Azure Monitor live webhook integration
- Microsoft Teams notification
- Email notification
- RAG-based knowledge retrieval
- Vector database for similar incident search
- Automated runbook execution
- Multi-cloud alert integration
- Predictive incident detection
- AI agent assisted troubleshooting
- Kubernetes deployment
- Azure App Service deployment
- Private networking and production cloud architecture

---

# 23. Final Outcome

Without OpsGPT:

```text
Engineers manually investigate multiple alerts, determine relationships, identify root causes, and communicate findings.
```

With OpsGPT:

```text
The platform automatically receives alerts, correlates related issues, creates incidents, generates AI analysis, recommends fixes, notifies engineers, and stores the resolution for future reuse.
```

This helps teams reduce MTTD and MTTR while improving operational reliability.
