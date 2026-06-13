import { Navigate, Outlet, Route, Routes } from "react-router-dom";

import Navbar from "../components/Navbar";
import ProtectedRoute from "../components/ProtectedRoute";
import { useAuth } from "../context/AuthContext";
import DashboardPage from "../pages/DashboardPage";
import IncidentDetailPage from "../pages/IncidentDetailPage";
import IncidentsPage from "../pages/IncidentsPage";
import KnowledgeBasePage from "../pages/KnowledgeBasePage";
import LoginPage from "../pages/LoginPage";
import ProfilePage from "../pages/ProfilePage";

function ApplicationLayout() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="page-container">
        <Outlet />
      </main>
    </div>
  );
}

function HomeRedirect() {
  const { isAuthenticated } = useAuth();
  return (
    <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<ApplicationLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/incidents" element={<IncidentsPage />} />
          <Route
            path="/incidents/:incidentId"
            element={<IncidentDetailPage />}
          />
          <Route path="/knowledge-base" element={<KnowledgeBasePage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Route>
      </Route>
      <Route path="/" element={<HomeRedirect />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default AppRoutes;
