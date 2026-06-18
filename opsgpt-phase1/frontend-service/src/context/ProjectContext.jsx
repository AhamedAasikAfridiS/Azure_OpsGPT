import { createContext, useCallback, useContext, useMemo, useState } from "react";

const ProjectContext = createContext(null);

export function ProjectProvider({ children }) {
  const [selectedProjectId, setSelectedProjectIdState] = useState(() =>
    localStorage.getItem("opsgpt_selected_project")
  );

  const setSelectedProjectId = useCallback((projectId) => {
    if (projectId) {
      localStorage.setItem("opsgpt_selected_project", projectId);
    } else {
      localStorage.removeItem("opsgpt_selected_project");
    }
    setSelectedProjectIdState(projectId);
  }, []);

  const value = useMemo(() => ({ selectedProjectId, setSelectedProjectId }), [selectedProjectId, setSelectedProjectId]);
  return <ProjectContext.Provider value={value}>{children}</ProjectContext.Provider>;
}

export function useProject() {
  return useContext(ProjectContext);
}
