import { ArrowRight, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, Navigate } from "react-router-dom";

import api from "../api/client.js";
import ProjectForm from "../components/projects/ProjectForm.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function AdminProjectsPage() {
  const { isAdmin } = useAuth();
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({ name: "", description: "", environment: "production", owner_team: "" });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

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

  if (!isAdmin) {
    return <Navigate to="/projects" replace />;
  }

  async function createProject(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await api.post("/projects", form);
      setForm({ name: "", description: "", environment: "production", owner_team: "" });
      await loadProjects();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create project");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="page-stack">
      <PageHeader
        actions={
          <button className="secondary-button" onClick={loadProjects} type="button">
            <RefreshCw size={16} aria-hidden="true" />
            Refresh
          </button>
        }
        description="Project and monitoring source administration"
        title="Admin Projects"
      />

      {error && <ErrorState message={error} />}

      <section className="section-block">
        <div className="section-heading">
          <h2>Create project</h2>
        </div>
        <ProjectForm form={form} onChange={setForm} onSubmit={createProject} saving={saving} />
      </section>

      {loading && <LoadingState />}
      {!loading && projects.length === 0 && <EmptyState title="No projects" />}
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
            <Link className="primary-button link-button" to={`/admin/projects/${project.project_id}/sources`}>
              Configure
              <ArrowRight size={16} />
            </Link>
          </article>
        ))}
      </div>
    </section>
  );
}
