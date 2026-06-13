import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import { formatLabel } from "../utils/formatters";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login", { replace: true });
  }

  return (
    <header className="navbar">
      <div className="navbar__brand">
        <span className="navbar__logo">OG</span>
        <div>
          <strong>OpsGPT</strong>
          <small>Incident Management</small>
        </div>
      </div>

      <nav className="navbar__links" aria-label="Primary navigation">
        <NavLink to="/dashboard">Dashboard</NavLink>
        <NavLink to="/incidents">Incidents</NavLink>
        <NavLink to="/knowledge-base">Knowledge Base</NavLink>
        <NavLink to="/profile">Profile</NavLink>
      </nav>

      <div className="navbar__user">
        <div>
          <strong>{user?.name}</strong>
          <small>{formatLabel(user?.role)}</small>
        </div>
        <button type="button" className="button button--secondary" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}

export default Navbar;
