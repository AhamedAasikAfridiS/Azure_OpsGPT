import { Copy, Plus, Search, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Navigate, useParams } from "react-router-dom";

import api from "../api/client.js";
import BackButton from "../components/navigation/BackButton.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function AdminMonitoringSourcesPage() {
  const { isAdmin } = useAuth();
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [sources, setSources] = useState([]);
  const [members, setMembers] = useState([]);
  const [userResults, setUserResults] = useState([]);
  const [query, setQuery] = useState("");
  const [sourceForm, setSourceForm] = useState({
    source_type: "prometheus_alertmanager",
    source_name: "",
    prometheus_url: "",
    alertmanager_url: "",
    dashboard_url: "",
    description: ""
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  async function loadData() {
    setLoading(true);
    setError("");
    try {
      const [projectResponse, sourcesResponse, membersResponse] = await Promise.all([
        api.get(`/projects/${projectId}`),
        api.get(`/projects/${projectId}/monitoring-sources`),
        api.get(`/projects/${projectId}/members`)
      ]);
      setProject(projectResponse.data);
      setSources(sourcesResponse.data);
      setMembers(membersResponse.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not load project configuration");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [projectId]);

  if (!isAdmin) {
    return <Navigate to="/projects" replace />;
  }

  async function createSource(event) {
    event.preventDefault();
    setError("");
    setNotice("");
    try {
      await api.post(`/projects/${projectId}/monitoring-sources`, sourceForm);
      setSourceForm({
        source_type: "prometheus_alertmanager",
        source_name: "",
        prometheus_url: "",
        alertmanager_url: "",
        dashboard_url: "",
        description: ""
      });
      await loadData();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create monitoring source");
    }
  }

  async function copyWebhook(path) {
    const url = `${window.location.origin}${path}`;
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(url);
        setNotice("Webhook URL copied");
      } else {
        setNotice(url);
      }
    } catch {
      setNotice(url);
    }
  }

  async function searchUsers(event) {
    event.preventDefault();
    setError("");
    try {
      const response = await api.get("/users/search", { params: { query } });
      setUserResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not search users");
    }
  }

  async function assignUser(userId) {
    setError("");
    try {
      await api.post(`/projects/${projectId}/members`, { user_id: userId });
      await loadData();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not assign member");
    }
  }

  async function removeUser(userId) {
    setError("");
    try {
      await api.delete(`/projects/${projectId}/members/${userId}`);
      await loadData();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not remove member");
    }
  }

  if (loading) return <LoadingState />;

  const receiverWebhookUrl = sources[0]
    ? `${window.location.origin}${sources[0].webhook_path}`
    : "http://<VM_IP>:8080/alerts/webhook/project/{project_id}/{webhook_token}";

  return (
    <section className="page-stack">
      <BackButton to="/admin/projects" />
      <PageHeader
        breadcrumbs={[
          { label: "Admin", to: "/admin/projects" },
          { label: project?.name || projectId }
        ]}
        description={projectId}
        title={project?.name || "Project Configuration"}
      />

      {error && <ErrorState message={error} />}
      {notice && <div className="notice-state">{notice}</div>}

      <section className="section-block">
        <div className="section-heading">
          <h2>Monitoring sources</h2>
        </div>
        <form className="form-grid" onSubmit={createSource}>
          <label>
            Source type
            <select
              value={sourceForm.source_type}
              onChange={(event) => setSourceForm({ ...sourceForm, source_type: event.target.value })}
            >
              <option value="prometheus_alertmanager">Prometheus Alertmanager</option>
            </select>
          </label>
          <label>
            Source name
            <input
              value={sourceForm.source_name}
              onChange={(event) => setSourceForm({ ...sourceForm, source_name: event.target.value })}
              required
            />
          </label>
          <label>
            Prometheus URL
            <input
              value={sourceForm.prometheus_url}
              onChange={(event) => setSourceForm({ ...sourceForm, prometheus_url: event.target.value })}
            />
          </label>
          <label>
            Alertmanager URL
            <input
              value={sourceForm.alertmanager_url}
              onChange={(event) => setSourceForm({ ...sourceForm, alertmanager_url: event.target.value })}
            />
          </label>
          <label>
            Dashboard URL
            <input
              value={sourceForm.dashboard_url}
              onChange={(event) => setSourceForm({ ...sourceForm, dashboard_url: event.target.value })}
            />
          </label>
          <label className="full-span">
            Description
            <textarea
              value={sourceForm.description}
              onChange={(event) => setSourceForm({ ...sourceForm, description: event.target.value })}
              rows="3"
            />
          </label>
          <button className="primary-button" disabled={!sourceForm.source_name.trim()} type="submit">
            <Plus size={16} />
            Create
          </button>
        </form>

        {sources.length === 0 ? (
          <EmptyState title="No monitoring sources" />
        ) : (
          <div className="source-list">
            {sources.map((source) => (
              <article className="source-row" key={source.source_id}>
                <div>
                  <strong>{source.source_name}</strong>
                  <span>{source.source_type}</span>
                  <code>{`${window.location.origin}${source.webhook_path}`}</code>
                </div>
                <button className="secondary-button" onClick={() => copyWebhook(source.webhook_path)} type="button">
                  <Copy size={16} />
                  Copy
                </button>
              </article>
            ))}
          </div>
        )}
        <div className="receiver-example">
          <h3>Alertmanager receiver example</h3>
          <pre>{`receivers:
  - name: opsgpt-webhook
    webhook_configs:
      - url: '${receiverWebhookUrl}'
        send_resolved: true`}</pre>
        </div>
      </section>

      <section className="section-block">
        <div className="section-heading">
          <h2>Members</h2>
        </div>
        <form className="search-row" onSubmit={searchUsers}>
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Name, email, or role" />
          <button className="secondary-button" type="submit">
            <Search size={16} />
            Search
          </button>
        </form>
        {userResults.length > 0 && (
          <div className="result-list">
            {userResults.map((item) => (
              <div className="result-row" key={item.id}>
                <div>
                  <strong>{item.name}</strong>
                  <span>{item.email}</span>
                  <span>{item.role}</span>
                </div>
                <button className="primary-button" onClick={() => assignUser(item.id)} type="button">
                  <Plus size={16} />
                  Assign
                </button>
              </div>
            ))}
          </div>
        )}
        {members.length === 0 ? (
          <EmptyState title="No assigned members" />
        ) : (
          <div className="result-list">
            {members.map((member) => (
              <div className="result-row" key={member.id}>
                <div>
                  <strong>{member.user.name}</strong>
                  <span>{member.user.email}</span>
                  <span>{member.user.role}</span>
                </div>
                <button className="danger-button" onClick={() => removeUser(member.user_id)} type="button">
                  <Trash2 size={16} />
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </section>
    </section>
  );
}
