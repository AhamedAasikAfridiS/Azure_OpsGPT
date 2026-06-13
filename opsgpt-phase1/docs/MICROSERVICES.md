# OpsGPT Microservices

## Frontend Service

Technology: React, Vite, React Router, Axios

Responsibilities:

- User login and logout
- Protected routes
- Dashboard
- Project selector and project-scoped navigation
- Incident list and filters
- Incident detail and AI analysis display
- Status updates and resolution-note forms
- Similar incidents
- Knowledge base
- User profile
- Role-aware controls
- Admin project, membership, and monitoring source screens

Boundaries:

- Calls Core API for normal user workflows
- Does not call monitoring, AI, or notification services directly
- Does not implement correlation, RCA, recommendations, or Slack delivery
- UI permissions do not replace backend RBAC

## Core API Service

Technology: FastAPI, SQLAlchemy, PostgreSQL, JWT

Responsibilities:

- Authentication and local users
- Role-based access control
- Project and membership ownership
- Monitoring source metadata and webhook token generation
- Incident data and status
- Resolution notes
- Dashboard aggregates
- Timelines and audit logs
- Knowledge base
- Internal incident endpoints for AI Analysis
- Optional notification event handoff

Boundaries:

- Does not receive raw monitoring alerts
- Does not parse Azure Monitor or Grafana payloads
- Does not generate AI analysis
- Does not send Slack messages directly

## Alert Ingestion Service

Technology: FastAPI, SQLAlchemy, PostgreSQL, Pydantic, HTTPX

Responsibilities:

- Azure Monitor-style webhook reception
- Grafana-style webhook reception
- Project-specific webhook reception and Core token validation
- Manual alert submission
- Raw payload storage
- Source-specific parsing
- Normalization and validation
- Ingestion logs
- Optional forwarding to AI Analysis

Boundaries:

- Does not create incidents
- Does not correlate alerts
- Does not generate AI output
- Does not manage users or notifications

## AI Analysis Service

Technology: FastAPI, SQLAlchemy, PostgreSQL, Pydantic, HTTPX

Responsibilities:

- Store normalized alerts
- Duplicate detection
- Project-aware rule-based correlation
- Correlation-group management
- Real AI provider calls
- Structured JSON validation
- Incident creation and analysis updates through Core API
- Rule-based similar-incident scoring

Supported providers:

- Ollama
- Gemini
- OpenAI
- Azure OpenAI Phase 2 configuration path

Boundaries:

- Does not receive raw monitoring webhooks
- Does not parse source-specific payloads
- Does not own users, status changes, or resolution notes
- Does not write directly to the Core database
- Does not send notifications
- Does not provide mock AI output

## Notification Service

Technology: FastAPI, SQLAlchemy, PostgreSQL, Pydantic, HTTPX

Responsibilities:

- Receive complete incident events from Core API
- Format event-specific messages
- Console delivery
- Slack Incoming Webhook delivery
- Retry failed delivery
- Store notifications and delivery attempts

Boundaries:

- Does not receive or normalize alerts
- Does not correlate incidents
- Does not generate AI output
- Does not manage users, incidents, status, or resolution data

## Service Communication

```text
Browser -> Frontend -> Core API

Monitoring Tool -> Alert Ingestion -> AI Analysis -> Core API

Core API -> Notification Service -> Console or Slack
```

All service-to-service communication uses REST in Phase 1.
