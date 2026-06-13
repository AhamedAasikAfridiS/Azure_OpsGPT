# Notification Service

The Notification Service receives complete incident events from Core API,
formats event-specific messages, delivers them through Slack or the local
console, and stores notification history and every delivery attempt.

## Responsibilities

- Receive complete notification events from Core API
- Deliver Slack webhook notifications
- Support console output for local development
- Store notification history and delivery status
- Track delivery attempts
- Retry failed delivery attempts

The service does not receive monitoring alerts, analyze incidents, manage
users, update incident state, or own resolution notes.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/notifications/events` | Format, store, and deliver an incident event |
| `POST` | `/notifications/slack/test` | Deliver and store a channel test message |
| `GET` | `/notifications` | List notification history with optional filters |
| `GET` | `/notifications/{notification_id}` | Get a notification and its delivery attempts |
| `GET` | `/notifications/incident/{incident_id}` | List notifications for one incident |
| `GET` | `/health` | Return service and channel health metadata |

## Channels

Set `NOTIFICATION_CHANNEL=console` for local development. Messages are written
to the service log and marked as sent.

Set `NOTIFICATION_CHANNEL=slack` to send:

```json
{
  "text": "formatted notification message"
}
```

to `SLACK_WEBHOOK_URL`. A missing Slack URL causes a clear configuration error
at startup.

## Retry Behavior

The service attempts delivery up to `NOTIFICATION_RETRY_COUNT` times. Every
attempt is stored in `notification_delivery_attempts`. Intermediate failures
set the notification to `retrying`; exhausted attempts set it to `failed`.

## Core API Connection

Core API sends complete event payloads to:

```text
POST http://notification-service:8004/notifications/events
```

Notification Service does not query or write the Core API database.
