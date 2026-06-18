export default function StatusBadge({ value }) {
  const normalized = (value || "unknown").toLowerCase();
  return <span className={`badge ${normalized}`}>{normalized}</span>;
}
