import { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";

import { useAuth } from "../../context/AuthContext.jsx";
import { useProject } from "../../context/ProjectContext.jsx";
import Header from "./Header.jsx";
import Sidebar from "./Sidebar.jsx";

function pageTitle(pathname) {
  if (pathname.includes("/admin/projects/")) return "Monitoring Source Setup";
  if (pathname === "/admin/projects") return "Admin Projects";
  if (pathname.includes("/incidents/")) return "Incident Detail";
  if (pathname.includes("/incidents")) return "Incidents";
  if (pathname.includes("/dashboard")) return "Dashboard";
  if (pathname.includes("/knowledge-base")) return "Knowledge Base";
  if (pathname.includes("/profile")) return "Profile";
  return "Projects";
}

export default function AppLayout() {
  const { user, logout, isAdmin } = useAuth();
  const { selectedProjectId, setSelectedProjectId } = useProject();
  const location = useLocation();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className={`app-shell ${sidebarCollapsed ? "sidebar-collapsed" : ""}`}>
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <Sidebar
        collapsed={sidebarCollapsed}
        isAdmin={isAdmin}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
        onToggleCollapsed={() => setSidebarCollapsed((value) => !value)}
        selectedProjectId={selectedProjectId}
      />
      <div className="workspace">
        <Header
          onMenuClick={() => setMobileOpen(true)}
          onLogout={logout}
          pageTitle={pageTitle(location.pathname)}
          selectedProjectId={selectedProjectId}
          setSelectedProjectId={setSelectedProjectId}
          user={user}
        />
        <main className="content" id="main-content" tabIndex={-1}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
