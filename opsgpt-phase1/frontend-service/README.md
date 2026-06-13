# Frontend Service

The Frontend Service is the React and Vite user interface for OpsGPT Phase 1.
It communicates with Core API for authentication, dashboards, incidents,
knowledge-base records, and profile data.

## Pages

- `/login`
- `/dashboard`
- `/incidents`
- `/incidents/:incidentId`
- `/knowledge-base`
- `/profile`

All routes except `/login` are protected by the authentication context.

## API Connection

Configure:

```env
VITE_CORE_API_URL=http://localhost:8001
```

The centralized Axios client attaches the JWT from local storage and clears
the session when Core API returns HTTP 401.

The frontend does not directly call Alert Ingestion, AI Analysis, or
Notification Service for normal user workflows.

## RBAC

- `junior_engineer` receives a complete read-only investigation interface.
- `senior_engineer` can update status and add resolution notes.
- `admin` can update status and add resolution notes.

Backend authorization remains authoritative; the frontend role utilities only
control which actions are displayed.
