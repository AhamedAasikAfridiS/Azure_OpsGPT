import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  createMonitoringSource,
  getMonitoringSources,
  updateMonitoringSource,
} from "../api/monitoringSourceApi";
import { getProject } from "../api/projectApi";
import Button from "../components/Button";
import BackButton from "../components/BackButton";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import ErrorMessage from "../components/ErrorMessage";
import FormInput from "../components/FormInput";

const EMPTY_SOURCE = {
  source_type: "grafana",
  source_name: "",
  dashboard_url: "",
  alert_rule_url: "",
  is_active: true,
};

function AdminMonitoringSourcesPage() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [sources, setSources] = useState([]);
  const [form, setForm] = useState(EMPTY_SOURCE);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState("");
  const ingestionBaseUrl =
    import.meta.env.VITE_ALERT_INGESTION_URL || "http://localhost:8002";

  async function load() {
    try {
      const [projectData, sourceData] = await Promise.all([
        getProject(projectId),
        getMonitoringSources(projectId),
      ]);
      setProject(projectData);
      setSources(sourceData);
    } catch (requestError) {
      setError(requestError);
    }
  }

  useEffect(() => {
    load();
  }, [projectId]);

  async function handleCreate(event) {
    event.preventDefault();
    setError(null);
    try {
      await createMonitoringSource(projectId, form);
      setForm(EMPTY_SOURCE);
      await load();
    } catch (requestError) {
      setError(requestError);
    }
  }

  async function toggleSource(source) {
    try {
      await updateMonitoringSource(projectId, source.source_id, {
        is_active: !source.is_active,
      });
      await load();
    } catch (requestError) {
      setError(requestError);
    }
  }

  async function copyWebhook(source) {
    const url = `${ingestionBaseUrl}${source.webhook_path}`;
    await navigator.clipboard.writeText(url);
    setCopied(source.source_id);
  }

  return (
    <div className="space-y-8">
      <div>
        <BackButton label="Back to Admin Projects" to="/admin/projects" />
        <p className="eyebrow">Monitoring configuration</p>
        <h2 className="page-title">
          {project?.name || "Monitoring sources"}
        </h2>
        <p className="mt-2 max-w-3xl text-slate-500">
          Store dashboard metadata and configure monitoring tools to send
          triggered alerts to the generated project webhook. OpsGPT does not
          scrape the linked dashboards.
        </p>
      </div>

      <ErrorMessage error={error} />

      <div className="grid gap-7 xl:grid-cols-[380px_1fr]">
        <Card>
          <h3 className="text-lg font-bold text-slate-900">Add source</h3>
          <form className="mt-5 grid gap-4" onSubmit={handleCreate}>
            <FormInput
              label="Source type"
              as="select"
              value={form.source_type}
              onChange={(event) =>
                setForm({ ...form, source_type: event.target.value })
              }
            >
              <option value="grafana">Grafana</option>
              <option value="azure_monitor">Azure Monitor</option>
              <option value="custom">Custom webhook</option>
            </FormInput>
            <FormInput
              label="Source name"
              value={form.source_name}
              onChange={(event) =>
                setForm({ ...form, source_name: event.target.value })
              }
              required
            />
            <FormInput
              label="Dashboard URL"
              type="url"
              value={form.dashboard_url}
              onChange={(event) =>
                setForm({ ...form, dashboard_url: event.target.value })
              }
            />
            <FormInput
              label="Alert rule URL"
              type="url"
              value={form.alert_rule_url}
              onChange={(event) =>
                setForm({ ...form, alert_rule_url: event.target.value })
              }
            />
            <Button type="submit">Generate webhook</Button>
          </form>
        </Card>

        <div className="space-y-5">
          {sources.length ? (
            sources.map((source) => {
              const webhookUrl = `${ingestionBaseUrl}${source.webhook_path}`;
              return (
                <Card key={source.source_id}>
                  <div className="flex flex-wrap items-start justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-3">
                        <h3 className="text-lg font-bold text-slate-900">
                          {source.source_name}
                        </h3>
                        <span className="rounded-full bg-brand-50 px-2.5 py-1 text-xs font-semibold text-brand-700">
                          {source.source_type}
                        </span>
                      </div>
                      <p className="mt-1 text-sm text-slate-500">
                        {source.source_id}
                      </p>
                    </div>
                    <Button
                      variant={source.is_active ? "danger" : "secondary"}
                      onClick={() => toggleSource(source)}
                    >
                      {source.is_active ? "Deactivate" : "Activate"}
                    </Button>
                  </div>

                  <div className="mt-5 rounded-xl bg-slate-950 p-4 text-slate-100">
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Project webhook URL
                    </p>
                    <code className="mt-2 block break-all text-sm">
                      {webhookUrl}
                    </code>
                    <Button
                      className="mt-4"
                      variant="secondary"
                      onClick={() => copyWebhook(source)}
                    >
                      {copied === source.source_id
                        ? "Copied"
                        : "Copy webhook URL"}
                    </Button>
                  </div>

                  <dl className="mt-5 grid gap-4 text-sm md:grid-cols-2">
                    <div>
                      <dt className="font-semibold text-slate-700">
                        Dashboard
                      </dt>
                      <dd className="mt-1 break-all text-slate-500">
                        {source.dashboard_url || "Not provided"}
                      </dd>
                    </div>
                    <div>
                      <dt className="font-semibold text-slate-700">
                        Alert rule
                      </dt>
                      <dd className="mt-1 break-all text-slate-500">
                        {source.alert_rule_url || "Not provided"}
                      </dd>
                    </div>
                  </dl>
                </Card>
              );
            })
          ) : (
            <EmptyState
              title="No monitoring sources"
              description="Add Grafana, Azure Monitor, or a custom webhook source."
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminMonitoringSourcesPage;
