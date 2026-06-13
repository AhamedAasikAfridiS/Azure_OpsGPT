# AI Analysis Service

The AI Analysis Service receives normalized alerts, detects duplicates,
correlates related operational signals, uses a configured real AI provider,
and writes final incident data through Core API internal REST endpoints.

## Responsibilities

- Receive normalized alerts
- Detect duplicates and correlate related alerts
- Group alerts by service, environment, and time window
- Generate incident summaries, RCA, confidence, and fix recommendations
- Create or update incidents through Core API internal endpoints
- Perform simple rule-based similar incident matching

The service does not receive raw provider-specific webhooks, write directly to
the Core API database, manage users, or send notifications.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/analysis/alerts` | Process one normalized alert end to end |
| `POST` | `/analysis/correlate` | Correlate a supplied alert list without incident creation |
| `POST` | `/analysis/generate-summary` | Generate an AI incident summary |
| `POST` | `/analysis/generate-rca` | Generate AI RCA, evidence, and confidence |
| `POST` | `/analysis/generate-fix` | Generate AI remediation recommendations |
| `POST` | `/analysis/similar-incidents` | Score supplied historical incidents |
| `GET` | `/analysis/incidents/{incident_id}` | Inspect stored analysis and correlation data |
| `GET` | `/health` | Return service and selected-provider health metadata |

## AI Providers

Phase 1 providers are:

- `ollama`
- `gemini`
- `openai`

The selected provider's URL/model/key settings are validated during startup.
Missing or invalid configuration prevents startup. There is no mock provider
and no fake fallback response.

The `azure_openai` selection and client configuration are present as a
Phase 2-ready path. Azure OpenAI is not required for Phase 1.

Every provider is instructed to return JSON only. Invalid provider JSON is
treated as a controlled analysis failure and stored with
`analysis_status=failed`.

## Service Communication

Alert Ingestion calls:

```text
POST http://ai-analysis-service:8003/analysis/alerts
```

AI Analysis creates incidents through:

```text
POST {CORE_API_URL}/internal/incidents
```

It stores completed analysis through:

```text
PATCH {CORE_API_URL}/internal/incidents/{incident_id}/analysis
```

Both Core API calls include `X-Internal-API-Key`.
