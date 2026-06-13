import { useNavigate } from "react-router-dom";

import Button from "../components/Button";
import EmptyState from "../components/EmptyState";
import ErrorMessage from "../components/ErrorMessage";
import LoadingSpinner from "../components/LoadingSpinner";
import { useAuth } from "../context/AuthContext";
import { useProject } from "../context/ProjectContext";
import { formatLabel } from "../utils/formatters";

function ProjectSelectPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const {
    projects,
    selectProject,
    isLoadingProjects,
    refreshProjects,
  } = useProject();

  function openProject(projectId) {
    selectProject(projectId);
    navigate(`/projects/${projectId}/dashboard`);
  }

  if (isLoadingProjects) {
    return <LoadingSpinner message="Loading your projects..." />;
  }

  const activeProjects = projects.filter((project) => project.is_active);

  return (
    <div className="space-y-8">
      <div className="flex items-end justify-between">
        <div>
          <p className="eyebrow">Project workspace</p>
          <h2 className="page-title">Select a project</h2>
          <p className="mt-2 text-slate-500">
            Incidents, dashboards, and webhook sources are isolated by
            project.
          </p>
        </div>
        <Button variant="secondary" onClick={refreshProjects}>
          Refresh
        </Button>
      </div>

      <ErrorMessage />

      {activeProjects.length ? (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {activeProjects.map((project) => (
            <button
              type="button"
              key={project.project_id}
              onClick={() => openProject(project.project_id)}
              className="group rounded-2xl border border-slate-200 bg-white p-6 text-left shadow-panel transition hover:-translate-y-1 hover:border-brand-300"
            >
              <div className="flex items-center justify-between">
                <span className="rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
                  {formatLabel(project.environment)}
                </span>
                <span className="text-slate-400 transition group-hover:text-brand-600">
                  Open project
                </span>
              </div>
              <h3 className="mt-5 text-xl font-bold text-slate-900">
                {project.name}
              </h3>
              <p className="mt-2 line-clamp-2 text-sm text-slate-500">
                {project.description || "No project description provided."}
              </p>
              <p className="mt-5 text-xs font-semibold uppercase tracking-wide text-slate-400">
                {project.owner_team || "No owner team"}
              </p>
            </button>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No projects available"
          description={
            user?.role === "admin"
              ? "Create the first project from Admin Projects."
              : "Ask an administrator to assign you to a project."
          }
          action={
            user?.role === "admin" ? (
              <Button onClick={() => navigate("/admin/projects")}>
                Create project
              </Button>
            ) : null
          }
        />
      )}
    </div>
  );
}

export default ProjectSelectPage;
