import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  addResolutionNote,
  getIncident,
  getProjectIncident,
  getIncidentTimeline,
  getSimilarIncidents,
  updateIncidentStatus,
} from "../api/incidentApi";
import ErrorMessage from "../components/ErrorMessage";
import BackButton from "../components/BackButton";
import LoadingSpinner from "../components/LoadingSpinner";
import RecommendedFix from "../components/RecommendedFix";
import SeverityBadge from "../components/SeverityBadge";
import SimilarIncidents from "../components/SimilarIncidents";
import StatusBadge from "../components/StatusBadge";
import Timeline from "../components/Timeline";
import { useAuth } from "../context/AuthContext";
import { INCIDENT_STATUSES } from "../utils/constants";
import { formatDateTime, formatLabel, toDisplayList } from "../utils/formatters";
import { canEditIncident } from "../utils/roleUtils";

function IncidentDetailPage({ projectScoped = false }) {
  const { incidentId, projectId } = useParams();
  const { user } = useAuth();
  const [incident, setIncident] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [similarIncidents, setSimilarIncidents] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState("");
  const [resolutionNotes, setResolutionNotes] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");

  const loadIncident = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [incidentData, timelineData, similarData] = await Promise.all([
        projectScoped
          ? getProjectIncident(projectId, incidentId)
          : getIncident(incidentId),
        getIncidentTimeline(incidentId),
        getSimilarIncidents(incidentId),
      ]);
      setIncident(incidentData);
      setTimeline(timelineData);
      setSimilarIncidents(similarData);
      setSelectedStatus(incidentData.status);
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsLoading(false);
    }
  }, [incidentId, projectId, projectScoped]);

  useEffect(() => {
    loadIncident();
  }, [loadIncident]);

  async function handleStatusUpdate(event) {
    event.preventDefault();
    setIsSaving(true);
    setError(null);
    setSuccessMessage("");
    try {
      await updateIncidentStatus(incidentId, selectedStatus);
      setSuccessMessage("Incident status updated.");
      await loadIncident();
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsSaving(false);
    }
  }

  async function handleResolutionNote(event) {
    event.preventDefault();
    setIsSaving(true);
    setError(null);
    setSuccessMessage("");
    try {
      await addResolutionNote(incidentId, resolutionNotes);
      setResolutionNotes("");
      setSuccessMessage("Resolution note added.");
      await loadIncident();
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsSaving(false);
    }
  }

  if (isLoading && !incident) {
    return <LoadingSpinner message="Loading incident details..." />;
  }

  if (!incident) {
    return (
      <div className="page-stack">
        <ErrorMessage error={error || new Error("Incident not found.")} />
        <BackButton
          label={
            projectScoped
              ? "Back to Project Incidents"
              : "Back to Incidents"
          }
          to={
            projectScoped
              ? `/projects/${projectId}/incidents`
              : "/incidents"
          }
        />
      </div>
    );
  }

  const supportingEvidence = toDisplayList(incident.supporting_evidence);
  const relatedAlertIds = toDisplayList(incident.related_alert_ids);
  const editable = canEditIncident(user);

  return (
    <div className="page-stack">
      <div className="page-heading page-heading--detail">
        <div>
          <BackButton
            label={
              projectScoped
                ? "Back to Project Incidents"
                : "Back to Incidents"
            }
            to={
              projectScoped
                ? `/projects/${projectId}/incidents`
                : "/incidents"
            }
          />
          <span className="eyebrow">{incident.incident_id}</span>
          <h1>{incident.title}</h1>
          <p className="muted">{incident.service_name}</p>
        </div>
        <div className="badge-group">
          <SeverityBadge severity={incident.severity} />
          <StatusBadge status={incident.status} />
        </div>
      </div>

      <ErrorMessage error={error} />
      {successMessage && <div className="success-message">{successMessage}</div>}

      <section className="detail-grid">
        <article className="content-section detail-grid__wide">
          <h2>AI Incident Summary</h2>
          <p>{incident.ai_summary || "AI summary is not available yet."}</p>
        </article>

        <article className="content-section">
          <h2>Incident Information</h2>
          <dl className="definition-list">
            <div>
              <dt>Created</dt>
              <dd>{formatDateTime(incident.created_at)}</dd>
            </div>
            <div>
              <dt>Updated</dt>
              <dd>{formatDateTime(incident.updated_at)}</dd>
            </div>
            <div>
              <dt>Confidence</dt>
              <dd>
                {incident.confidence_score === null
                  ? "Not available"
                  : `${incident.confidence_score}%`}
              </dd>
            </div>
            <div>
              <dt>Resolved</dt>
              <dd>{formatDateTime(incident.resolved_at)}</dd>
            </div>
          </dl>
        </article>

        <article className="content-section">
          <h2>Root Cause</h2>
          <p>{incident.root_cause || "Root cause is not available yet."}</p>
        </article>

        <article className="content-section">
          <h2>Supporting Evidence</h2>
          {supportingEvidence.length ? (
            <ul className="detail-list">
              {supportingEvidence.map((item, index) => (
                <li key={`${item}-${index}`}>{item}</li>
              ))}
            </ul>
          ) : (
            <p className="muted">No supporting evidence is available.</p>
          )}
        </article>

        <article className="content-section">
          <h2>Related Alert IDs</h2>
          {relatedAlertIds.length ? (
            <ul className="tag-list">
              {relatedAlertIds.map((alertId) => (
                <li key={alertId}>{alertId}</li>
              ))}
            </ul>
          ) : (
            <p className="muted">No related alert IDs are available.</p>
          )}
        </article>

        <article className="content-section detail-grid__wide">
          <h2>Recommended Fix</h2>
          <RecommendedFix recommendation={incident.recommended_fix} />
        </article>
      </section>

      {editable && (
        <section className="editor-grid">
          <form className="content-section" onSubmit={handleStatusUpdate}>
            <span className="eyebrow">Senior and admin control</span>
            <h2>Update Status</h2>
            <label>
              Incident status
              <select
                value={selectedStatus}
                onChange={(event) => setSelectedStatus(event.target.value)}
              >
                {INCIDENT_STATUSES.map((status) => (
                  <option value={status.value} key={status.value}>
                    {status.label}
                  </option>
                ))}
              </select>
            </label>
            <button className="button button--primary" disabled={isSaving}>
              Save status
            </button>
          </form>

          <form className="content-section" onSubmit={handleResolutionNote}>
            <span className="eyebrow">Senior and admin control</span>
            <h2>Add Resolution Note</h2>
            <label>
              Resolution details
              <textarea
                value={resolutionNotes}
                onChange={(event) => setResolutionNotes(event.target.value)}
                rows="5"
                required
              />
            </label>
            <button className="button button--primary" disabled={isSaving}>
              Add note
            </button>
          </form>
        </section>
      )}

      {incident.resolution_notes?.length > 0 && (
        <section className="content-section">
          <h2>Resolution Notes</h2>
          <div className="note-list">
            {incident.resolution_notes.map((note) => (
              <article key={note.id}>
                <p>{note.notes}</p>
                <small>
                  User {note.created_by} | {formatDateTime(note.created_at)}
                </small>
              </article>
            ))}
          </div>
        </section>
      )}

      <section className="content-section">
        <h2>Timeline</h2>
        <Timeline events={timeline} />
      </section>

      <section className="content-section">
        <h2>Similar Incidents</h2>
        <SimilarIncidents incidents={similarIncidents} />
      </section>

      {!editable && (
        <p className="read-only-notice">
          Your {formatLabel(user?.role)} role has read-only incident access.
        </p>
      )}
    </div>
  );
}

export default IncidentDetailPage;
