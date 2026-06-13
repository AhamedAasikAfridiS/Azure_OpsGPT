import { formatLabel } from "../utils/formatters";

function SeverityBadge({ severity }) {
  return (
    <span className={`badge badge--severity-${severity || "unknown"}`}>
      {formatLabel(severity)}
    </span>
  );
}

export default SeverityBadge;
