import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import { getProjects } from "../api/projectApi";
import { PROJECT_STORAGE_KEY } from "../utils/constants";
import { useAuth } from "./AuthContext";

const ProjectContext = createContext(null);

export function ProjectProvider({ children }) {
  const { isAuthenticated, user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(() =>
    localStorage.getItem(PROJECT_STORAGE_KEY),
  );
  const [isLoadingProjects, setIsLoadingProjects] = useState(false);

  const refreshProjects = useCallback(async () => {
    if (!isAuthenticated) {
      setProjects([]);
      return [];
    }
    setIsLoadingProjects(true);
    try {
      const result = await getProjects();
      setProjects(result);
      if (
        selectedProjectId &&
        !result.some((project) => project.project_id === selectedProjectId)
      ) {
        localStorage.removeItem(PROJECT_STORAGE_KEY);
        setSelectedProjectId(null);
      }
      return result;
    } finally {
      setIsLoadingProjects(false);
    }
  }, [isAuthenticated, selectedProjectId]);

  useEffect(() => {
    refreshProjects();
  }, [refreshProjects, user?.id]);

  const selectProject = useCallback((projectId) => {
    if (projectId) {
      localStorage.setItem(PROJECT_STORAGE_KEY, projectId);
      setSelectedProjectId(projectId);
    } else {
      localStorage.removeItem(PROJECT_STORAGE_KEY);
      setSelectedProjectId(null);
    }
  }, []);

  const selectedProject =
    projects.find((project) => project.project_id === selectedProjectId) ||
    null;

  const value = useMemo(
    () => ({
      projects,
      selectedProject,
      selectedProjectId,
      isLoadingProjects,
      selectProject,
      refreshProjects,
    }),
    [
      projects,
      selectedProject,
      selectedProjectId,
      isLoadingProjects,
      selectProject,
      refreshProjects,
    ],
  );

  return (
    <ProjectContext.Provider value={value}>
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject() {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error("useProject must be used inside ProjectProvider");
  }
  return context;
}
