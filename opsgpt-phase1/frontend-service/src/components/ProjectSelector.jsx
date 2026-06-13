import { useNavigate } from "react-router-dom";

import { useProject } from "../context/ProjectContext";

function ProjectSelector({ compact = false }) {
  const navigate = useNavigate();
  const {
    projects,
    selectedProjectId,
    selectProject,
    isLoadingProjects,
  } = useProject();

  function handleChange(event) {
    const projectId = event.target.value;
    selectProject(projectId || null);
    if (projectId) {
      navigate(`/projects/${projectId}/dashboard`);
    } else {
      navigate("/projects");
    }
  }

  return (
    <label className="grid gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500">
      {!compact && "Current project"}
      <select
        value={selectedProjectId || ""}
        onChange={handleChange}
        disabled={isLoadingProjects}
        className="min-w-48 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-medium normal-case tracking-normal text-slate-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
      >
        <option value="">Select a project</option>
        {projects
          .filter((project) => project.is_active)
          .map((project) => (
            <option value={project.project_id} key={project.project_id}>
              {project.name}
            </option>
          ))}
      </select>
    </label>
  );
}

export default ProjectSelector;
