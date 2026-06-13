import { Link } from "react-router-dom";

function SimilarIncidents({ incidents }) {
  if (!incidents?.length) {
    return <div className="empty-state">No similar incidents found.</div>;
  }

  return (
    <div className="similar-list">
      {incidents.map((incident) => (
        <article
          className="similar-item"
          key={`${incident.knowledge_base_id}-${incident.source_incident_id}`}
        >
          <div>
            <strong>{incident.title}</strong>
            <p>{incident.summary || incident.root_cause || "No summary available."}</p>
          </div>
          <div className="similar-item__meta">
            <span>{incident.similarity_percentage}% similar</span>
            {incident.source_incident_id && (
              <Link to={`/incidents/${incident.source_incident_id}`}>
                View source incident
              </Link>
            )}
          </div>
        </article>
      ))}
    </div>
  );
}

export default SimilarIncidents;
