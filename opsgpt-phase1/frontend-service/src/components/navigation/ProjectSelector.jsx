import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../api/client.js";

export default function ProjectSelector({ selectedProjectId, setSelectedProjectId }) {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    let ignore = false;
    api
      .get("/projects")
      .then((response) => {
        if (!ignore) setProjects(response.data || []);
      })
      .catch(() => {
        if (!ignore) setProjects([]);
      });
    return () => {
      ignore = true;
    };
  }, []);

  function handleChange(event) {
    const projectId = event.target.value;
    setSelectedProjectId(projectId || null);
    if (projectId) {
      navigate(`/projects/${projectId}/dashboard`);
    }
  }

  return (
    <label className="project-selector">
      <span>Project</span>
      <select aria-label="Selected project" onChange={handleChange} value={selectedProjectId || ""}>
        <option value="">Select project</option>
        {projects.map((project) => (
          <option key={project.project_id} value={project.project_id}>
            {project.name}
          </option>
        ))}
      </select>
    </label>
  );
}
