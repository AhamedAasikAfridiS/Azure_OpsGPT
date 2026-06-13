import { Link } from "react-router-dom";

import { formatDateTime } from "../utils/formatters";
import SeverityBadge from "./SeverityBadge";
import StatusBadge from "./StatusBadge";

function IncidentTable({ incidents, emptyMessage = "No incidents found." }) {
  if (!incidents.length) {
    return <div className="empty-state">{emptyMessage}</div>;
  }

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Incident ID</th>
            <th>Title</th>
            <th>Service</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map((incident) => (
            <tr key={incident.incident_id}>
              <td>
                <Link to={`/incidents/${incident.incident_id}`}>
                  {incident.incident_id}
                </Link>
              </td>
              <td>{incident.title}</td>
              <td>{incident.service_name}</td>
              <td>
                <SeverityBadge severity={incident.severity} />
              </td>
              <td>
                <StatusBadge status={incident.status} />
              </td>
              <td>{formatDateTime(incident.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default IncidentTable;
