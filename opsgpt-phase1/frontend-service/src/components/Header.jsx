import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import Button from "./Button";
import ProjectSelector from "./ProjectSelector";

function Header() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login", { replace: true });
  }

  return (
    <header className="flex min-h-20 items-center justify-between border-b border-slate-200 bg-white px-8">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-brand-600">
          Operations workspace
        </p>
        <h1 className="text-lg font-bold text-slate-900">
          Incident command center
        </h1>
      </div>
      <div className="flex items-end gap-4">
        <ProjectSelector compact />
        <Button variant="secondary" onClick={handleLogout}>
          Logout
        </Button>
      </div>
    </header>
  );
}

export default Header;
