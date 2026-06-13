import { Navigate, Route, Routes, useParams } from "react-router-dom";

import AppLayout from "../components/AppLayout";
import ProtectedRoute from "../components/ProtectedRoute";
import { useAuth } from "../context/AuthContext";
import { useProject } from "../context/ProjectContext";
import AdminMonitoringSourcesPage from "../pages/AdminMonitoringSourcesPage";
import AdminProjectsPage from "../pages/AdminProjectsPage";
import KnowledgeBasePage from "../pages/KnowledgeBasePage";
import LoginPage from "../pages/LoginPage";
import ProfilePage from "../pages/ProfilePage";
import ProjectDashboardPage from "../pages/ProjectDashboardPage";
import ProjectIncidentDetailPage from "../pages/ProjectIncidentDetailPage";
import ProjectIncidentsPage from "../pages/ProjectIncidentsPage";
import ProjectSelectPage from "../pages/ProjectSelectPage";

function HomeRedirect() {
  const { isAuthenticated } = useAuth();
  return (
    <Navigate to={isAuthenticated ? "/projects" : "/login"} replace />
  );
}

function LegacyProjectRedirect({ destination }) {
  const { selectedProjectId } = useProject();
  const { incidentId } = useParams();

  if (!selectedProjectId) {
    return <Navigate to="/projects" replace />;
  }
  if (destination === "incident" && incidentId) {
    return (
      <Navigate
        to={`/projects/${selectedProjectId}/incidents/${incidentId}`}
        replace
      />
    );
  }
  return (
    <Navigate
      to={`/projects/${selectedProjectId}/${destination}`}
      replace
    />
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/projects" element={<ProjectSelectPage />} />
          <Route
            path="/projects/:projectId/dashboard"
            element={<ProjectDashboardPage />}
          />
          <Route
            path="/projects/:projectId/incidents"
            element={<ProjectIncidentsPage />}
          />
          <Route
            path="/projects/:projectId/incidents/:incidentId"
            element={<ProjectIncidentDetailPage />}
          />
          <Route path="/knowledge-base" element={<KnowledgeBasePage />} />
          <Route path="/profile" element={<ProfilePage />} />

          <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
            <Route
              path="/admin/projects"
              element={<AdminProjectsPage />}
            />
            <Route
              path="/admin/projects/:projectId/sources"
              element={<AdminMonitoringSourcesPage />}
            />
          </Route>

          <Route
            path="/dashboard"
            element={<LegacyProjectRedirect destination="dashboard" />}
          />
          <Route
            path="/incidents"
            element={<LegacyProjectRedirect destination="incidents" />}
          />
          <Route
            path="/incidents/:incidentId"
            element={<LegacyProjectRedirect destination="incident" />}
          />
        </Route>
      </Route>

      <Route path="/" element={<HomeRedirect />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default AppRoutes;
