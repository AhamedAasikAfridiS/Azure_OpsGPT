import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { isActiveNavItem } from "../utils/routeUtils";

export default function Sidebar() {
  const { pathname } = useLocation();
  const { user } = useAuth();
  const selectedProjectId = localStorage.getItem("selectedProjectId");
  const isAdmin = user?.role === "admin";

  const projectDashboardPath = selectedProjectId ? `/projects/${selectedProjectId}/dashboard` : "/projects";
  const projectIncidentsPath = selectedProjectId ? `/projects/${selectedProjectId}/incidents` : "/projects";

  const items = [
    { key: "projects", label: "Project Selector", to: "/projects" },
    { key: "dashboard", label: "Dashboard", to: projectDashboardPath },
    { key: "incidents", label: "Incidents", to: projectIncidentsPath },
    { key: "knowledgeBase", label: "Knowledge Base", to: "/knowledge-base" },
    { key: "profile", label: "Profile", to: "/profile" },
  ];

  if (isAdmin) {
    items.push({ key: "adminProjects", label: "Admin Projects", to: "/admin/projects" });
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span className="brand-mark">O</span>
        <div>
          <strong>OpsGPT</strong>
          <small>AI First Responder</small>
        </div>
      </div>

      <nav className="sidebar-nav" aria-label="Main navigation">
        {items.map((item) => (
          <Link
            key={item.key}
            to={item.to}
            className={`sidebar-link ${isActiveNavItem(item.key, pathname) ? "active" : ""}`}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
