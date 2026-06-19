import { ArrowRight, RefreshCw, Search } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/client.js";
import ProjectCard from "../components/projects/ProjectCard.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useProject } from "../context/ProjectContext.jsx";

export default function ProjectsPage() {
  const { isAdmin } = useAuth();
  const { setSelectedProjectId } = useProject();
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [query, setQuery] = useState("");
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

  const filteredProjects = projects.filter((project) => {
    const term = query.trim().toLowerCase();
    if (!term) return true;
    return [project.name, project.project_id, project.environment, project.owner_team]
      .filter(Boolean)
      .some((value) => value.toLowerCase().includes(term));
  });

  return (
    <section className="page-stack">
      <PageHeader
        actions={
          <>
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
          </>
        }
        description="Assigned incident workspaces"
        title="Projects"
      />

      <div className="filter-bar">
        <label>
          Search projects
          <div className="input-with-icon">
            <Search size={16} aria-hidden="true" />
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Name, ID, team" />
          </div>
        </label>
      </div>

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}
      {!loading && !error && projects.length === 0 && (
        <EmptyState
          action={
            isAdmin ? (
              <Link className="primary-button link-button" to="/admin/projects">
                Create project
              </Link>
            ) : null
          }
          title="No projects yet"
          detail="No assigned projects are available."
        />
      )}
      <div className="resource-grid">
        {filteredProjects.map((project) => (
          <ProjectCard key={project.project_id} onOpen={openProject} project={project} />
        ))}
      </div>
      {!loading && !error && projects.length > 0 && filteredProjects.length === 0 && <EmptyState title="No matching projects" />}
    </section>
  );
}
