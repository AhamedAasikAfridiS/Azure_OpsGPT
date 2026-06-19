import { useEffect, useState } from "react";

import api from "../api/client.js";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";

export default function KnowledgeBasePage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/knowledge-base")
      .then((response) => setItems(response.data))
      .catch((err) => setError(err.response?.data?.detail || "Could not load knowledge base"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <section className="page-stack">
      <PageHeader description="Incident learnings" title="Knowledge Base" />
      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {!loading && !error && items.length === 0 && <EmptyState title="No knowledge base entries" />}
      <div className="resource-grid">
        {items.map((item) => (
          <article className="resource-card" key={item.id}>
            <div>
              <h2>{item.title}</h2>
              <p>{item.summary}</p>
            </div>
            <dl className="meta-grid">
              <div>
                <dt>Service</dt>
                <dd>{item.service_name}</dd>
              </div>
              <div>
                <dt>Project</dt>
                <dd>{item.project_id || "Global"}</dd>
              </div>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}
