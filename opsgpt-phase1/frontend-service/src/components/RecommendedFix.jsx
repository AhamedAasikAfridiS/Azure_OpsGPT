import { formatLabel, toDisplayList } from "../utils/formatters";

function RecommendedFix({ recommendation }) {
  if (!recommendation) {
    return <p className="muted">No recommended fix is available.</p>;
  }

  if (Array.isArray(recommendation)) {
    return (
      <ul className="detail-list">
        {toDisplayList(recommendation).map((item, index) => (
          <li key={`${item}-${index}`}>{item}</li>
        ))}
      </ul>
    );
  }

  if (typeof recommendation !== "object") {
    return <p>{String(recommendation)}</p>;
  }

  return (
    <div className="recommendation-grid">
      {Object.entries(recommendation).map(([section, actions]) => (
        <section key={section}>
          <h4>{formatLabel(section)}</h4>
          <ul className="detail-list">
            {toDisplayList(actions).map((action, index) => (
              <li key={`${action}-${index}`}>{action}</li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}

export default RecommendedFix;
