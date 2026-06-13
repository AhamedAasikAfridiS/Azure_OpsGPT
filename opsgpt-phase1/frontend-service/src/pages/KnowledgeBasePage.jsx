import { useEffect, useState } from "react";

import { getKnowledgeBase } from "../api/knowledgeBaseApi";
import ErrorMessage from "../components/ErrorMessage";
import LoadingSpinner from "../components/LoadingSpinner";
import RecommendedFix from "../components/RecommendedFix";

function KnowledgeBasePage() {
  const [entries, setEntries] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadKnowledgeBase() {
      try {
        const data = await getKnowledgeBase();
        if (active) {
          setEntries(data);
        }
      } catch (requestError) {
        if (active) {
          setError(requestError);
        }
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    loadKnowledgeBase();
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">Operational memory</span>
          <h1>Knowledge Base</h1>
          <p className="muted">
            Resolved incidents, root causes, and reusable remediation guidance.
          </p>
        </div>
      </div>

      <ErrorMessage error={error} />

      {isLoading ? (
        <LoadingSpinner message="Loading knowledge base..." />
      ) : (
        <div className="knowledge-grid">
          {entries.length ? (
            entries.map((entry) => (
              <article className="knowledge-card" key={entry.id}>
                <div className="knowledge-card__header">
                  <span>{entry.service_name}</span>
                  <small>{entry.source_incident_id || "Manual entry"}</small>
                </div>
                <h2>{entry.title}</h2>
                <h3>Root Cause</h3>
                <p>{entry.root_cause || "Not provided"}</p>
                <h3>Summary</h3>
                <p>{entry.summary || "Not provided"}</p>
                <h3>Resolution Steps</h3>
                <RecommendedFix recommendation={entry.resolution_steps} />
              </article>
            ))
          ) : (
            <div className="empty-state">
              No knowledge base entries are available.
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default KnowledgeBasePage;
