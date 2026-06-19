import { useEffect, useState } from "react";

import api from "../api/client.js";
import StatusBadge from "../components/StatusBadge.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function ProfilePage() {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/projects")
      .then((response) => setProjects(response.data || []))
      .catch((err) => setError(err.response?.data?.detail || "Could not load assigned projects"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <section className="page-stack">
      <PageHeader description={user?.email} title="Profile" />
      <section className="section-block">
        <dl className="meta-grid wide">
          <div>
            <dt>Name</dt>
            <dd>{user?.name}</dd>
          </div>
          <div>
            <dt>Email</dt>
            <dd>{user?.email}</dd>
          </div>
          <div>
            <dt>Role</dt>
            <dd>
              <StatusBadge value={user?.role} />
            </dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>{user?.is_active ? "Active" : "Inactive"}</dd>
          </div>
        </dl>
      </section>
      <section className="section-block">
        <div className="section-heading">
          <h2>Assigned Projects</h2>
        </div>
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}
        {!loading && !error && projects.length === 0 && <EmptyState title="No assigned projects" />}
        {!loading && !error && projects.length > 0 && (
          <div className="resource-grid compact-grid">
            {projects.map((project) => (
              <article className="resource-card" key={project.project_id}>
                <div>
                  <h2>{project.name}</h2>
                  <p>{project.project_id}</p>
                </div>
                <dl className="meta-grid">
                  <div>
                    <dt>Environment</dt>
                    <dd>{project.environment}</dd>
                  </div>
                  <div>
                    <dt>Owner</dt>
                    <dd>{project.owner_team || "Unassigned"}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>
        )}
      </section>
    </section>
  );
}
