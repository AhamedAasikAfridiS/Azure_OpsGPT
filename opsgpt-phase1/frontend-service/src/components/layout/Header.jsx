import { LogOut, Menu, User } from "lucide-react";
import { Link } from "react-router-dom";

import ProjectSelector from "../navigation/ProjectSelector.jsx";

export default function Header({ onLogout, onMenuClick, pageTitle, selectedProjectId, setSelectedProjectId, user }) {
  return (
    <header className="topbar">
      <div className="topbar-leading">
        <button aria-label="Open navigation menu" className="icon-button mobile-only" onClick={onMenuClick} type="button">
          <Menu size={20} />
        </button>
        <div>
          <span className="eyebrow">OpsGPT</span>
          <h1>{pageTitle}</h1>
        </div>
      </div>

      <div className="topbar-actions">
        <ProjectSelector selectedProjectId={selectedProjectId} setSelectedProjectId={setSelectedProjectId} />
        <Link className="profile-chip" to="/profile">
          <User size={18} aria-hidden="true" />
          <span>
            <strong>{user?.name || "User"}</strong>
            <small>{user?.role || "role"}</small>
          </span>
        </Link>
        <button className="secondary-button compact-button" onClick={onLogout} type="button">
          <LogOut size={16} aria-hidden="true" />
          Sign out
        </button>
      </div>
    </header>
  );
}
