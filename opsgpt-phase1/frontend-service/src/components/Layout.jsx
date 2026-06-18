import { Activity, BookOpen, FolderKanban, LayoutDashboard, LogOut, Settings, User } from "lucide-react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { useProject } from "../context/ProjectContext.jsx";

export default function Layout() {
  const { user, logout, isAdmin } = useAuth();
  const { selectedProjectId } = useProject();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  const projectBase = selectedProjectId ? `/projects/${selectedProjectId}` : "/projects";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">O</div>
          <div>
            <strong>OpsGPT</strong>
            <span>Phase 1</span>
          </div>
        </div>

        <nav className="nav-list">
          <NavLink to="/projects" end className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
            <FolderKanban size={18} />
            Projects
          </NavLink>
          <NavLink
            to={`${projectBase}/dashboard`}
            className={({ isActive }) => `nav-link ${isActive ? "active" : ""} ${!selectedProjectId ? "disabled" : ""}`}
          >
            <LayoutDashboard size={18} />
            Dashboard
          </NavLink>
          <NavLink
            to={`${projectBase}/incidents`}
            className={({ isActive }) => `nav-link ${isActive ? "active" : ""} ${!selectedProjectId ? "disabled" : ""}`}
          >
            <Activity size={18} />
            Incidents
          </NavLink>
          <NavLink to="/knowledge-base" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
            <BookOpen size={18} />
            Knowledge
          </NavLink>
          {isAdmin && (
            <NavLink to="/admin/projects" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              <Settings size={18} />
              Admin
            </NavLink>
          )}
        </nav>

        <button className="icon-text sidebar-button" onClick={handleLogout} type="button">
          <LogOut size={18} />
          Sign out
        </button>
      </aside>

      <div className="workspace">
        <header className="topbar">
          <div className="project-context">
            <span className="eyebrow">Selected project</span>
            <strong>{selectedProjectId || "None selected"}</strong>
          </div>
          <NavLink to="/profile" className="profile-chip">
            <User size={18} />
            <span>
              <strong>{user?.name}</strong>
              <small>{user?.role}</small>
            </span>
          </NavLink>
        </header>
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
