function ListSection({ title, items }) {
  if (!items || items.length === 0) return null;
  return (
    <div className="fix-section">
      <h4>{title}</h4>
      <ul>
        {items.map((item, index) => (
          <li key={`${title}-${index}`}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default function RecommendedFix({ recommendedFix }) {
  if (!recommendedFix || Object.keys(recommendedFix).length === 0) {
    return <p className="muted">AI analysis is not available for this incident yet.</p>;
  }

  return (
    <div className="recommended-fix">
      <ListSection title="Immediate Actions" items={recommendedFix.immediate_actions} />
      <ListSection title="Long Term Actions" items={recommendedFix.long_term_actions} />
      <ListSection title="Runbook Suggestions" items={recommendedFix.runbook_suggestions} />
    </div>
  );
}
