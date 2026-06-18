import { ArrowRight, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/client.js";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useProject } from "../context/ProjectContext.jsx";

export default function ProjectsPage() {
  const { isAdmin } = useAuth();
  const { setSelectedProjectId } = useProject();
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadProjects() {
    setLoading(true);
    setError("");
    try {
      const response = await api.get("/projects");
      setProjects(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not load projects");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

  function openProject(project) {
    setSelectedProjectId(project.project_id);
    navigate(`/projects/${project.project_id}/dashboard`);
  }

  return (
    <section className="page-stack">
      <div className="page-header">
        <div>
          <h1>Projects</h1>
          <p>Assigned incident workspaces</p>
        </div>
        <div className="action-row">
          <button className="secondary-button" onClick={loadProjects} type="button">
            <RefreshCw size={16} />
            Refresh
          </button>
          {isAdmin && (
            <Link className="primary-button link-button" to="/admin/projects">
              Admin
              <ArrowRight size={16} />
            </Link>
          )}
        </div>
      </div>

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {!loading && !error && projects.length === 0 && (
        <EmptyState title="No projects yet" detail="An admin can create a project and assign members." />
      )}
      <div className="resource-grid">
        {projects.map((project) => (
          <article className="resource-card" key={project.project_id}>
            <div>
              <h2>{project.name}</h2>
              <p>{project.description || "No description"}</p>
            </div>
            <dl className="meta-grid">
              <div>
                <dt>Project ID</dt>
                <dd>{project.project_id}</dd>
              </div>
              <div>
                <dt>Environment</dt>
                <dd>{project.environment}</dd>
              </div>
              <div>
                <dt>Owner</dt>
                <dd>{project.owner_team || "Unassigned"}</dd>
              </div>
            </dl>
            <button className="primary-button" onClick={() => openProject(project)} type="button">
              Open
              <ArrowRight size={16} />
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}
