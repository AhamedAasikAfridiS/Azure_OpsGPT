import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { createMonitoringSource, deleteMonitoringSource, getMonitoringSources } from "../api/monitoringSourceApi";
import BackButton from "../components/BackButton";
import Button from "../components/Button";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import ErrorMessage from "../components/ErrorMessage";
import FormInput from "../components/FormInput";
import LoadingSpinner from "../components/LoadingSpinner";

const sourceTypes = [
  ["grafana", "Grafana"],
  ["azure_monitor", "Azure Monitor"],
  ["prometheus_alertmanager", "Prometheus Alertmanager"],
  ["datadog", "Datadog"],
  ["new_relic", "New Relic"],
  ["splunk", "Splunk"],
  ["elastic", "Elastic / Kibana"],
  ["sentry", "Sentry"],
  ["pagerduty", "PagerDuty"],
  ["aws_cloudwatch", "AWS CloudWatch"],
  ["google_cloud_monitoring", "Google Cloud Monitoring"],
  ["dynatrace", "Dynatrace"],
  ["appdynamics", "AppDynamics"],
  ["zabbix", "Zabbix"],
  ["nagios", "Nagios"],
  ["custom", "Custom Webhook"],
];

const initialForm = {
  source_type: "grafana",
  source_name: "",
  dashboard_url: "",
  alert_rule_url: "",
};

export default function AdminMonitoringSourcesPage() {
  const { projectId } = useParams();
  const [sources, setSources] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const loadSources = async () => {
    setLoading(true);
    setError("");
    try {
      const { data } = await getMonitoringSources(projectId);
      setSources(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load monitoring sources.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSources();
  }, [projectId]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await createMonitoringSource(projectId, form);
      setForm(initialForm);
      await loadSources();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to create monitoring source.");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (sourceId) => {
    setError("");
    try {
      await deleteMonitoringSource(projectId, sourceId);
      await loadSources();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete monitoring source.");
    }
  };

  const copyWebhookPath = async (path) => {
    if (!path) return;
    await navigator.clipboard?.writeText(path);
  };

  return (
    <div className="page-stack">
      <BackButton label="Back to Admin Projects" to="/admin/projects" />

      <div className="page-header">
        <div>
          <p className="eyebrow">Admin</p>
          <h1>Monitoring Sources</h1>
          <p className="muted">Register webhook-based observability sources for project {projectId}.</p>
        </div>
      </div>

      {error && <ErrorMessage message={error} />}

      <Card title="Add Source">
        <form className="form-grid" onSubmit={handleSubmit}>
          <label className="form-field">
            <span>Source Type</span>
            <select
              value={form.source_type}
              onChange={(event) => setForm({ ...form, source_type: event.target.value })}
            >
              {sourceTypes.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <FormInput
            label="Source Name"
            value={form.source_name}
            onChange={(event) => setForm({ ...form, source_name: event.target.value })}
            placeholder="Production Grafana"
            required
          />
          <FormInput
            label="Dashboard URL"
            value={form.dashboard_url}
            onChange={(event) => setForm({ ...form, dashboard_url: event.target.value })}
            placeholder="https://grafana.example.com/d/payment-api"
          />
          <FormInput
            label="Alert Rule URL"
            value={form.alert_rule_url}
            onChange={(event) => setForm({ ...form, alert_rule_url: event.target.value })}
            placeholder="https://grafana.example.com/alerting/rules/payment-api"
          />
          <div className="form-actions">
            <Button type="submit" disabled={saving}>
              {saving ? "Saving..." : "Add Source"}
            </Button>
          </div>
        </form>
      </Card>

      <Card title="Configured Sources">
        {loading ? (
          <LoadingSpinner />
        ) : sources.length === 0 ? (
          <EmptyState title="No monitoring sources yet" message="Add a source to generate a project-specific webhook path." />
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Webhook Path</th>
                  <th>Dashboard</th>
                  <th>Alert Rule</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {sources.map((source) => (
                  <tr key={source.source_id}>
                    <td>{source.source_name}</td>
                    <td>{sourceTypes.find(([value]) => value === source.source_type)?.[1] || source.source_type}</td>
                    <td>
                      <code>{source.webhook_path}</code>
                      <Button variant="secondary" onClick={() => copyWebhookPath(source.webhook_path)}>
                        Copy
                      </Button>
                    </td>
                    <td>{source.dashboard_url ? <a href={source.dashboard_url}>Open</a> : "N/A"}</td>
                    <td>{source.alert_rule_url ? <a href={source.alert_rule_url}>Open</a> : "N/A"}</td>
                    <td>
                      <Button variant="danger" onClick={() => handleDelete(source.source_id)}>
                        Delete
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
