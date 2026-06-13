import { Link } from "react-router-dom";

import { formatDateTime } from "../utils/formatters";
import SeverityBadge from "./SeverityBadge";
import StatusBadge from "./StatusBadge";

function IncidentCard({ incident }) {
  return (
    <article className="incident-card">
      <div className="incident-card__header">
        <Link to={`/incidents/${incident.incident_id}`}>
          {incident.incident_id}
        </Link>
        <SeverityBadge severity={incident.severity} />
      </div>
      <h3>{incident.title}</h3>
      <p className="muted">{incident.service_name}</p>
      <div className="incident-card__footer">
        <StatusBadge status={incident.status} />
        <time>{formatDateTime(incident.created_at)}</time>
      </div>
    </article>
  );
}

export default IncidentCard;
