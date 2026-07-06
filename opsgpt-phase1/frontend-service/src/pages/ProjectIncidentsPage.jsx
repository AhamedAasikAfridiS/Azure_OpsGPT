import { AlertTriangle, CheckCircle2, Clock, LayoutGrid, List, RefreshCw, Search } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import api from "../api/client.js";
import StatusBadge from "../components/StatusBadge.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Table from "../components/ui/Table.jsx";
import { useProject } from "../context/ProjectContext.jsx";

export default function ProjectIncidentsPage() {
  const { projectId } = useParams();
  const { setSelectedProjectId } = useProject();
  const navigate = useNavigate();
  const [incidents, setIncidents] = useState([]);
  const [query, setQuery] = useState("");
  const [severity, setSeverity] = useState("all");
  const [status, setStatus] = useState("all");
  const [viewMode, setViewMode] = useState("table");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadIncidents() {
    setLoading(true);
    setError("");
    try {
      const response = await api.get(`/projects/${projectId}/incidents`);
      setIncidents(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not load incidents");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    setSelectedProjectId(projectId);
    loadIncidents();
  }, [projectId, setSelectedProjectId]);

  const filtered = useMemo(
    () =>
      incidents.filter((incident) => {
        const severityMatch = severity === "all" || incident.severity === severity;
        const statusMatch = status === "all" || incident.status === status;
        const term = query.trim().toLowerCase();
        const searchMatch =
          !term ||
          [incident.title, incident.incident_id, incident.service_name, incident.namespace, incident.cluster]
            .filter(Boolean)
            .some((value) => value.toLowerCase().includes(term));
        return severityMatch && statusMatch && searchMatch;
      }),
    [incidents, query, severity, status]
  );
  const openCount = incidents.filter((incident) => incident.status === "open").length;
  const criticalCount = incidents.filter((incident) => incident.severity === "critical").length;
  const resolvedCount = incidents.filter((incident) => incident.status === "resolved").length;

  return (
    <section className="page-stack">
      <PageHeader
        actions={
          <button className="secondary-button" onClick={loadIncidents} type="button">
            <RefreshCw size={16} aria-hidden="true" />
            Refresh
          </button>
        }
        breadcrumbs={[
          { label: "Projects", to: "/projects" },
          { label: projectId, to: `/projects/${projectId}/dashboard` },
          { label: "Incidents" }
        ]}
        description={projectId}
        title="Incidents"
      />

      <section className="incident-signal-strip" aria-label="Incident summary">
        <article>
          <Clock aria-hidden="true" />
          <span>Open queue</span>
          <strong>{openCount}</strong>
        </article>
        <article>
          <AlertTriangle aria-hidden="true" />
          <span>Critical pressure</span>
          <strong>{criticalCount}</strong>
        </article>
        <article>
          <CheckCircle2 aria-hidden="true" />
          <span>Resolved</span>
          <strong>{resolvedCount}</strong>
        </article>
      </section>

      <div className="filter-bar">
        <label>
          Search
          <div className="input-with-icon">
            <Search size={16} aria-hidden="true" />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Incident, service, namespace"
            />
          </div>
        </label>
        <label>
          Severity
          <select value={severity} onChange={(event) => setSeverity(event.target.value)}>
            <option value="all">All</option>
            <option value="critical">Critical</option>
            <option value="warning">Warning</option>
            <option value="informational">Informational</option>
          </select>
        </label>
        <label>
          Status
          <select value={status} onChange={(event) => setStatus(event.target.value)}>
            <option value="all">All</option>
            <option value="open">Open</option>
            <option value="investigating">Investigating</option>
            <option value="mitigated">Mitigated</option>
            <option value="resolved">Resolved</option>
          </select>
        </label>
        <div className="view-toggle" aria-label="Incident view mode">
          <button
            aria-pressed={viewMode === "table"}
            className={viewMode === "table" ? "active" : ""}
            onClick={() => setViewMode("table")}
            type="button"
          >
            <List size={16} aria-hidden="true" />
            Table
          </button>
          <button
            aria-pressed={viewMode === "cards"}
            className={viewMode === "cards" ? "active" : ""}
            onClick={() => setViewMode("cards")}
            type="button"
          >
            <LayoutGrid size={16} aria-hidden="true" />
            Cards
          </button>
        </div>
      </div>

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {!loading && !error && filtered.length === 0 && <EmptyState title="No matching incidents" />}
      {!loading && !error && filtered.length > 0 && viewMode === "cards" && (
        <div className="incident-card-grid">
          {filtered.map((incident) => (
            <article
              className="incident-card"
              key={incident.incident_id}
              onClick={() => navigate(`/projects/${projectId}/incidents/${incident.incident_id}`)}
              onKeyDown={(event) => {
                if (event.key === "Enter") navigate(`/projects/${projectId}/incidents/${incident.incident_id}`);
              }}
              tabIndex={0}
            >
              <div className="incident-card-top">
                <StatusBadge value={incident.severity} />
                <StatusBadge value={incident.status} />
              </div>
              <h2>{incident.title}</h2>
              <p>{incident.incident_id}</p>
              <dl className="meta-grid">
                <div>
                  <dt>Service</dt>
                  <dd>{incident.service_name}</dd>
                </div>
                <div>
                  <dt>Namespace</dt>
                  <dd>{incident.namespace || "-"}</dd>
                </div>
                <div>
                  <dt>Cluster</dt>
                  <dd>{incident.cluster || "-"}</dd>
                </div>
                <div>
                  <dt>Created</dt>
                  <dd>{new Date(incident.created_at).toLocaleString()}</dd>
                </div>
              </dl>
              <Link className="icon-text" to={`/projects/${projectId}/incidents/${incident.incident_id}`}>
                Open incident
              </Link>
            </article>
          ))}
        </div>
      )}
      {!loading && !error && filtered.length > 0 && viewMode === "table" && (
        <Table label="Project incidents">
            <thead>
              <tr>
                <th>Incident</th>
                <th>Service</th>
                <th>Namespace</th>
                <th>Cluster</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((incident) => (
                <tr
                  className="clickable-row"
                  key={incident.incident_id}
                  onClick={() => navigate(`/projects/${projectId}/incidents/${incident.incident_id}`)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") navigate(`/projects/${projectId}/incidents/${incident.incident_id}`);
                  }}
                  tabIndex={0}
                >
                  <td>
                    <Link to={`/projects/${projectId}/incidents/${incident.incident_id}`}>{incident.title}</Link>
                    <span className="subtle">{incident.incident_id}</span>
                  </td>
                  <td>{incident.service_name}</td>
                  <td>{incident.namespace || "-"}</td>
                  <td>{incident.cluster || "-"}</td>
                  <td>
                    <StatusBadge value={incident.severity} />
                  </td>
                  <td>
                    <StatusBadge value={incident.status} />
                  </td>
                  <td>{new Date(incident.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
        </Table>
      )}
    </section>
  );
}
