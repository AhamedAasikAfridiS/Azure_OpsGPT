import { Navigate } from "react-router-dom";

import { useProject } from "../context/ProjectContext.jsx";

export default function ProjectRedirect({ target }) {
  const { selectedProjectId } = useProject();
  if (!selectedProjectId) {
    return <Navigate to="/projects" replace />;
  }
  return <Navigate to={`/projects/${selectedProjectId}/${target}`} replace />;
}
