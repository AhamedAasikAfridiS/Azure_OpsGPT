import { Check, Send } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import api from "../api/client.js";
import StatusBadge from "../components/StatusBadge.jsx";
import BackButton from "../components/navigation/BackButton.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useProject } from "../context/ProjectContext.jsx";

export default function IncidentDetailPage() {
  const { projectId, incidentId } = useParams();
  const { canEditIncidents } = useAuth();
  const { setSelectedProjectId } = useProject();
  const [incident, setIncident] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [similar, setSimilar] = useState([]);
  const [newStatus, setNewStatus] = useState("investigating");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");

  async function loadIncident() {
    setLoading(true);
    setError("");
    try {
      const [incidentResponse, timelineResponse, similarResponse] = await Promise.all([
        api.get(`/projects/${projectId}/incidents/${incidentId}`),
        api.get(`/incidents/${incidentId}/timeline`),
        api.get(`/incidents/${incidentId}/similar`)
      ]);
      setIncident(incidentResponse.data);
      setNewStatus(incidentResponse.data.status);
      setTimeline(timelineResponse.data);
      setSimilar(similarResponse.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not load incident");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    setSelectedProjectId(projectId);
    loadIncident();
  }, [projectId, incidentId, setSelectedProjectId]);

  async function updateStatus() {
    setActionError("");
    try {
      await api.patch(`/incidents/${incidentId}/status`, { status: newStatus });
      await loadIncident();
    } catch (err) {
      setActionError(err.response?.data?.detail || "Could not update status");
    }
  }

  async function addNote(event) {
    event.preventDefault();
    setActionError("");
    try {
      await api.post(`/incidents/${incidentId}/resolution-notes`, { notes });
      setNotes("");
      await loadIncident();
    } catch (err) {
      setActionError(err.response?.data?.detail || "Could not add note");
    }
  }

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} />;
  if (!incident) return <EmptyState title="Incident not found" />;

  return (
    <section className="page-stack">
      <BackButton to={`/projects/${projectId}/incidents`} />
      <PageHeader
        actions={
          <div className="badge-row" aria-label="Incident state">
            <StatusBadge value={incident.severity} />
            <StatusBadge value={incident.status} />
          </div>
        }
        breadcrumbs={[
          { label: "Projects", to: "/projects" },
          { label: projectId, to: `/projects/${projectId}/dashboard` },
          { label: "Incidents", to: `/projects/${projectId}/incidents` },
          { label: incident.incident_id }
        ]}
        description={incident.incident_id}
        title={incident.title}
      />

      {actionError && <ErrorState message={actionError} />}

      <div className="detail-grid">
        <section className="section-block">
          <div className="section-heading">
            <h2>Overview</h2>
          </div>
          <dl className="meta-grid wide">
            <div>
              <dt>Service</dt>
              <dd>{incident.service_name}</dd>
            </div>
            <div>
              <dt>Project</dt>
              <dd>{incident.project_id || "-"}</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{incident.status}</dd>
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
        </section>

        <section className="section-block">
          <div className="section-heading">
            <h2>Prometheus Alert Details</h2>
          </div>
          <dl className="meta-grid wide">
            <div>
              <dt>Source</dt>
              <dd>{incident.source_type}</dd>
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
              <dt>Alert count</dt>
              <dd>{incident.related_alert_ids?.length || 0}</dd>
            </div>
          </dl>
          <div className="related-alerts">
            <h3>Related alerts</h3>
            {(incident.related_alert_ids || []).length === 0 ? (
              <p className="muted">No related alert IDs recorded.</p>
            ) : (
              <div className="chip-row">
                {incident.related_alert_ids.map((alertId) => (
                  <span className="code-chip" key={alertId}>
                    {alertId}
                  </span>
                ))}
              </div>
            )}
          </div>
        </section>

        <section className="section-block">
          <div className="section-heading">
            <h2>AI Summary</h2>
          </div>
          {incident.ai_summary || incident.root_cause || incident.recommended_fix ? (
            <div className="analysis-stack">
              <article>
                <h3>Summary</h3>
                <p>{incident.ai_summary || "AI analysis is not available for this incident yet."}</p>
              </article>
              <article>
                <h3>Root Cause Analysis</h3>
                <p>{incident.root_cause || "AI analysis is not available for this incident yet."}</p>
              </article>
              <article>
                <h3>Recommended Fix</h3>
                {incident.recommended_fix ? (
                  <pre>{JSON.stringify(incident.recommended_fix, null, 2)}</pre>
                ) : (
                  <p>AI analysis is not available for this incident yet.</p>
                )}
              </article>
              {incident.supporting_evidence?.length > 0 && (
                <article>
                  <h3>Supporting Evidence</h3>
                  <ul className="plain-list">
                    {incident.supporting_evidence.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </article>
              )}
            </div>
          ) : (
            <EmptyState title="AI analysis is not available for this incident yet." />
          )}
        </section>
      </div>

      {canEditIncidents && (
        <section className="section-block">
          <div className="section-heading">
            <h2>Actions</h2>
          </div>
          <div className="action-panel">
            <label>
              Status
              <select value={newStatus} onChange={(event) => setNewStatus(event.target.value)}>
                <option value="open">Open</option>
                <option value="investigating">Investigating</option>
                <option value="mitigated">Mitigated</option>
                <option value="resolved">Resolved</option>
              </select>
            </label>
            <button className="primary-button" onClick={updateStatus} type="button">
              <Check size={16} />
              Update
            </button>
          </div>
          <form className="note-form" onSubmit={addNote}>
            <label>
              Resolution notes
              <textarea value={notes} onChange={(event) => setNotes(event.target.value)} rows="4" />
            </label>
            <button className="secondary-button" disabled={!notes.trim()} type="submit">
              <Send size={16} />
              Add note
            </button>
          </form>
        </section>
      )}

      <div className="detail-grid">
        <section className="section-block">
          <div className="section-heading">
            <h2>Timeline</h2>
          </div>
          {timeline.length === 0 ? (
            <EmptyState title="No timeline events" />
          ) : (
            <ol className="timeline">
              {timeline.map((event) => (
                <li key={event.id}>
                  <strong>{event.event_type}</strong>
                  <span>{event.message}</span>
                  <time>{new Date(event.created_at).toLocaleString()}</time>
                </li>
              ))}
            </ol>
          )}
        </section>

        <section className="section-block">
          <div className="section-heading">
            <h2>Similar incidents</h2>
          </div>
          {similar.length === 0 ? (
            <EmptyState title="No similar incidents" />
          ) : (
            <ul className="plain-list">
              {similar.map((item) => (
                <li key={item.incident_id}>
                  <Link to={`/projects/${projectId}/incidents/${item.incident_id}`}>{item.title}</Link>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </section>
  );
}
