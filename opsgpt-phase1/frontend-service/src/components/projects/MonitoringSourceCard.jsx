import CopyButton from "../ui/CopyButton.jsx";

export default function MonitoringSourceCard({ source }) {
  const fullWebhookUrl = `${window.location.origin}${source.webhook_path}`;

  return (
    <article className="source-row">
      <div>
        <strong>{source.source_name}</strong>
        <span>Prometheus Alertmanager</span>
        <label className="webhook-display">
          Webhook URL
          <code>{fullWebhookUrl}</code>
        </label>
      </div>
      <CopyButton text={fullWebhookUrl} />
    </article>
  );
}
