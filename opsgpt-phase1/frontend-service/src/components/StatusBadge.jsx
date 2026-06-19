import Badge from "./ui/Badge.jsx";

export default function StatusBadge({ value }) {
  const normalized = (value || "unknown").toLowerCase();
  return <Badge tone={normalized}>{normalized.replace("_", " ")}</Badge>;
}
