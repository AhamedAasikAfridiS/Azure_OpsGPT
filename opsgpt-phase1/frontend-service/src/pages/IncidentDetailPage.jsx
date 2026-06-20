import { AlertTriangle, BrainCircuit, Check, CheckCircle2, CircleDot, Send } from "lucide-react";
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

function safeText(value) {
  if (typeof value === "string") return value.trim() || null;
  if (typeof value === "number") return String(value);
  if (value && typeof value === "object") {
    return safeText(value.text ?? value.message ?? value.description);
  }
  return null;
}

function parseMaybeJson(value) {
  if (typeof value !== "string") return value;
  const trimmed = value.trim();
  if (!trimmed) return null;

  try {
    return JSON.parse(trimmed);
  } catch {
    return value;
  }
}

function normalizeList(value) {
  const parsed = parseMaybeJson(value);
  const items = Array.isArray(parsed) ? parsed : [parsed];

  return items.flatMap((item) => {
    if (Array.isArray(item)) return normalizeList(item);
    const text = safeText(item);
    return text ? [text] : [];
  });
}

function normalizeRecommendedFix(value) {
  const normalized = {
    immediate_actions: [],
    long_term_actions: [],
    runbook_suggestions: [],
    rawText: null
  };
  const parsed = parseMaybeJson(value);

  if (!parsed) return normalized;
  if (typeof parsed === "string") {
    normalized.rawText = parsed.trim() || null;
    return normalized;
  }
  if (Array.isArray(parsed)) {
    normalized.immediate_actions = normalizeList(parsed);
    return normalized;
  }
  if (typeof parsed !== "object") return normalized;

  normalized.immediate_actions = normalizeList(
    parsed.immediate_actions ?? parsed.immediateActions
  );
  normalized.long_term_actions = normalizeList(
    parsed.long_term_actions ?? parsed.longTermActions
  );
  normalized.runbook_suggestions = normalizeList(
    parsed.runbook_suggestions ?? parsed.runbookSuggestions
  );
  return normalized;
}

function safeErrorMessage(value) {
  const message = safeText(value);
  if (!message || /traceback|stack trace|at \w+ \(/i.test(message)) {
    return "The AI analysis could not be completed. Please review the service configuration and try again.";
  }
  return message.length > 280 ? `${message.slice(0, 277)}...` : message;
}

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

  const aiSummary = safeText(incident.ai_summary);
  const rootCause = safeText(incident.root_cause);
  const supportingEvidence = normalizeList(incident.supporting_evidence);
  const recommendedFix = normalizeRecommendedFix(incident.recommended_fix);
  const hasRecommendedFix = recommendedFix.rawText || Object.values(recommendedFix)
    .filter((value) => Array.isArray(value))
    .some((items) => items.length > 0);
  const hasAiContent = aiSummary || rootCause || supportingEvidence.length > 0 || hasRecommendedFix;
  const analysisFailed = incident.analysis_status === "failed" || Boolean(incident.error_message);
  const wrapStyle = { maxWidth: "100%", minWidth: 0, overflowWrap: "anywhere", wordBreak: "break-word" };
  const aiCardStyle = {
    ...wrapStyle,
    padding: "20px",
    border: "1px solid var(--border)",
    borderRadius: "8px",
    background: "rgba(248, 250, 252, 0.78)",
    boxShadow: "0 6px 18px rgba(15, 23, 42, 0.035)"
  };

  return (
    <section className="page-stack" style={{ maxWidth: "100%", minWidth: 0 }}>
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

      </div>

      <section
        aria-labelledby="ai-analysis-heading"
        className="section-block"
        style={{ ...wrapStyle, overflow: "hidden" }}
      >
        <div className="section-heading">
          <h2 id="ai-analysis-heading">
            <BrainCircuit aria-hidden="true" size={20} style={{ marginRight: "8px", verticalAlign: "text-bottom" }} />
            AI Analysis
          </h2>
        </div>

        {analysisFailed && (
          <div
            role="alert"
            style={{
              ...wrapStyle,
              display: "flex",
              gap: "10px",
              marginBottom: "16px",
              padding: "14px",
              border: "1px solid rgba(217, 119, 6, 0.28)",
              borderRadius: "8px",
              background: "rgba(217, 119, 6, 0.08)",
              color: "#92400e"
            }}
          >
            <AlertTriangle aria-hidden="true" size={20} style={{ flex: "0 0 auto" }} />
            <div style={wrapStyle}>
              <strong>AI analysis failed</strong>
              <p style={{ ...wrapStyle, margin: "4px 0 0" }}>{safeErrorMessage(incident.error_message)}</p>
            </div>
          </div>
        )}

        {!hasAiContent ? (
          <p className="muted" style={{ ...wrapStyle, margin: 0 }}>
            AI analysis is not available for this incident yet.
          </p>
        ) : (
          <div
            style={{
              ...wrapStyle,
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 320px), 1fr))",
              gap: "16px"
            }}
          >
            <article style={aiCardStyle}>
              <h3 style={{ margin: "0 0 10px", fontSize: "17px" }}>AI Summary</h3>
              <p style={{ ...wrapStyle, margin: 0, color: "var(--text)", fontSize: "16px", lineHeight: 1.7 }}>
                {aiSummary || "AI summary is not available yet."}
              </p>
            </article>

            <article style={aiCardStyle}>
              <h3 style={{ margin: "0 0 10px", fontSize: "17px" }}>Root Cause Analysis</h3>
              <p style={{ ...wrapStyle, margin: 0, color: "var(--text)", fontSize: "16px", lineHeight: 1.7 }}>
                {rootCause || "Root cause analysis is not available yet."}
              </p>
            </article>

            <article style={{ ...aiCardStyle, gridColumn: "1 / -1" }}>
              <h3 style={{ margin: "0 0 12px", fontSize: "17px" }}>Supporting Evidence</h3>
              {supportingEvidence.length === 0 ? (
                <p className="muted" style={{ ...wrapStyle, margin: 0 }}>No supporting evidence is available yet.</p>
              ) : (
                <ul style={{ ...wrapStyle, display: "grid", gap: "10px", margin: 0, padding: 0, listStyle: "none" }}>
                  {supportingEvidence.map((item, index) => (
                    <li
                      key={`${item}-${index}`}
                      style={{
                        ...wrapStyle,
                        display: "flex",
                        alignItems: "flex-start",
                        gap: "10px",
                        padding: "12px 14px",
                        border: "1px solid var(--border)",
                        borderRadius: "8px",
                        background: "white",
                        fontSize: "15px",
                        lineHeight: 1.65
                      }}
                    >
                      <CircleDot aria-hidden="true" color="var(--accent)" size={17} style={{ flex: "0 0 auto", marginTop: "3px" }} />
                      <span style={wrapStyle}>{item}</span>
                    </li>
                  ))}
                </ul>
              )}
            </article>

            <article style={{ ...aiCardStyle, gridColumn: "1 / -1" }}>
              <h3 style={{ margin: "0 0 14px", fontSize: "17px" }}>Recommended Fix</h3>
              {recommendedFix.rawText ? (
                <p style={{ ...wrapStyle, margin: 0, color: "var(--text)", fontSize: "16px", lineHeight: 1.7 }}>
                  {recommendedFix.rawText}
                </p>
              ) : !hasRecommendedFix ? (
                <p className="muted" style={{ ...wrapStyle, margin: 0 }}>No fix recommendation is available yet.</p>
              ) : (
                <div style={{ ...wrapStyle, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 240px), 1fr))", gap: "14px" }}>
                  {[
                    ["Immediate Actions", recommendedFix.immediate_actions],
                    ["Long-Term Actions", recommendedFix.long_term_actions],
                    ["Runbook Suggestions", recommendedFix.runbook_suggestions]
                  ].map(([title, actions]) => actions.length > 0 && (
                    <section
                      key={title}
                      style={{
                        ...wrapStyle,
                        padding: "16px",
                        border: "1px solid var(--border)",
                        borderRadius: "8px",
                        background: "white"
                      }}
                    >
                      <h4 style={{ margin: "0 0 10px", fontSize: "15px" }}>{title}</h4>
                      <ul style={{ ...wrapStyle, display: "grid", gap: "10px", margin: 0, padding: 0, listStyle: "none" }}>
                        {actions.map((action, index) => (
                          <li key={`${action}-${index}`} style={{ ...wrapStyle, display: "flex", gap: "8px", alignItems: "flex-start", lineHeight: 1.6 }}>
                            <CheckCircle2 aria-hidden="true" color="var(--success)" size={16} style={{ flex: "0 0 auto", marginTop: "3px" }} />
                            <span style={wrapStyle}>{action}</span>
                          </li>
                        ))}
                      </ul>
                    </section>
                  ))}
                </div>
              )}
            </article>
          </div>
        )}
      </section>

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
