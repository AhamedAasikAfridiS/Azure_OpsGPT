import { ArrowRight, Plus, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, Navigate } from "react-router-dom";

import api from "../api/client.js";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function AdminProjectsPage() {
  const { isAdmin } = useAuth();
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({ name: "", description: "", environment: "production", owner_team: "" });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  if (!isAdmin) {
    return <Navigate to="/projects" replace />;
  }

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
      <div className="page-header">
        <div>
          <h1>Admin Projects</h1>
          <p>Project and monitoring source administration</p>
        </div>
        <button className="secondary-button" onClick={loadProjects} type="button">
          <RefreshCw size={16} />
          Refresh
        </button>
      </div>

      {error && <ErrorState message={error} />}

      <section className="section-block">
        <div className="section-heading">
          <h2>Create project</h2>
        </div>
        <form className="form-grid" onSubmit={createProject}>
          <label>
            Name
            <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
          </label>
          <label>
            Environment
            <input
              value={form.environment}
              onChange={(event) => setForm({ ...form, environment: event.target.value })}
              required
            />
          </label>
          <label>
            Owner team
            <input value={form.owner_team} onChange={(event) => setForm({ ...form, owner_team: event.target.value })} />
          </label>
          <label className="full-span">
            Description
            <textarea
              value={form.description}
              onChange={(event) => setForm({ ...form, description: event.target.value })}
              rows="3"
            />
          </label>
          <button className="primary-button" disabled={saving || !form.name.trim()} type="submit">
            <Plus size={16} />
            Create
          </button>
        </form>
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
