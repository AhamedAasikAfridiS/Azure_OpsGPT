import {
  Activity,
  BookOpen,
  FolderKanban,
  LayoutDashboard,
  PanelLeftClose,
  PanelLeftOpen,
  Settings,
  User
} from "lucide-react";
import { NavLink } from "react-router-dom";

function navClass({ isActive }) {
  return `nav-link ${isActive ? "active" : ""}`;
}

function projectNavClass({ isActive }, disabled) {
  return `nav-link ${isActive ? "active" : ""} ${disabled ? "disabled" : ""}`;
}

export default function Sidebar({
  collapsed,
  isAdmin,
  mobileOpen,
  onCloseMobile,
  onToggleCollapsed,
  selectedProjectId
}) {
  const projectBase = selectedProjectId ? `/projects/${selectedProjectId}` : "/projects";

  return (
    <>
      <button
        aria-label="Close navigation overlay"
        className={`sidebar-scrim ${mobileOpen ? "visible" : ""}`}
        onClick={onCloseMobile}
        type="button"
      />
      <aside className={`sidebar ${mobileOpen ? "open" : ""}`} id="primary-sidebar">
        <div className="sidebar-top">
          <div className="brand">
            <div className="brand-mark" aria-hidden="true">
              O
            </div>
            <div className="brand-copy">
              <strong>OpsGPT</strong>
              <span>Phase 1</span>
            </div>
          </div>
          <button
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            className="icon-button"
            onClick={onToggleCollapsed}
            type="button"
          >
            {collapsed ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}
          </button>
        </div>

        <nav aria-label="Primary navigation" className="nav-list" onClick={onCloseMobile}>
          <NavLink className={navClass} end to="/projects">
            <FolderKanban size={18} />
            <span>Projects</span>
          </NavLink>
          <NavLink
            className={(state) => projectNavClass(state, !selectedProjectId)}
            to={`${projectBase}/dashboard`}
          >
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </NavLink>
          <NavLink
            className={(state) => projectNavClass(state, !selectedProjectId)}
            to={`${projectBase}/incidents`}
          >
            <Activity size={18} />
            <span>Incidents</span>
          </NavLink>
          <NavLink className={navClass} to="/knowledge-base">
            <BookOpen size={18} />
            <span>Knowledge</span>
          </NavLink>
          {isAdmin && (
            <NavLink className={navClass} to="/admin/projects">
              <Settings size={18} />
              <span>Admin</span>
            </NavLink>
          )}
          <NavLink className={navClass} to="/profile">
            <User size={18} />
            <span>Profile</span>
          </NavLink>
        </nav>
      </aside>
    </>
  );
}
