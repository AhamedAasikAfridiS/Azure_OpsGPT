import { formatLabel } from "../utils/formatters";

function StatusBadge({ status }) {
  return (
    <span className={`badge badge--status-${status || "unknown"}`}>
      {formatLabel(status)}
    </span>
  );
}

export default StatusBadge;
