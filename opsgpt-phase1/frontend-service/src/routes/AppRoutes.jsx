import { Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "../components/ProtectedRoute.jsx";
import Layout from "../components/Layout.jsx";
import AdminMonitoringSourcesPage from "../pages/AdminMonitoringSourcesPage.jsx";
import AdminProjectsPage from "../pages/AdminProjectsPage.jsx";
import IncidentDetailPage from "../pages/IncidentDetailPage.jsx";
import KnowledgeBasePage from "../pages/KnowledgeBasePage.jsx";
import LoginPage from "../pages/LoginPage.jsx";
import NotFoundPage from "../pages/NotFoundPage.jsx";
import ProfilePage from "../pages/ProfilePage.jsx";
import ProjectDashboardPage from "../pages/ProjectDashboardPage.jsx";
import ProjectIncidentsPage from "../pages/ProjectIncidentsPage.jsx";
import ProjectsPage from "../pages/ProjectsPage.jsx";
import ProjectRedirect from "./ProjectRedirect.jsx";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/projects" replace />} />
          <Route path="/dashboard" element={<ProjectRedirect target="dashboard" />} />
          <Route path="/incidents" element={<ProjectRedirect target="incidents" />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/projects/:projectId/dashboard" element={<ProjectDashboardPage />} />
          <Route path="/projects/:projectId/incidents" element={<ProjectIncidentsPage />} />
          <Route path="/projects/:projectId/incidents/:incidentId" element={<IncidentDetailPage />} />
          <Route path="/admin/projects" element={<AdminProjectsPage />} />
          <Route path="/admin/projects/:projectId/sources" element={<AdminMonitoringSourcesPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/knowledge-base" element={<KnowledgeBasePage />} />
        </Route>
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
