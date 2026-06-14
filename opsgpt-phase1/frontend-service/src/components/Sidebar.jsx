import { Link, useLocation } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import { useProject } from "../context/ProjectContext";
import { isActiveNavItem } from "../utils/routeUtils";

function SidebarLink({ itemKey, to, children }) {
  const { pathname } = useLocation();
  const active = isActiveNavItem(itemKey, pathname);

  return (
    <Link
      to={to}
      aria-current={active ? "page" : undefined}
      className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
        active
          ? "bg-brand-600 text-white shadow-lg shadow-brand-600/20"
          : "text-slate-300 hover:bg-slate-800 hover:text-white"
      }`}
    >
      {children}
    </Link>
  );
}

function Sidebar() {
  const { user } = useAuth();
  const { selectedProjectId } = useProject();
  const projectBase = selectedProjectId
    ? `/projects/${selectedProjectId}`
    : "/projects";

  return (
    <aside className="flex min-h-screen w-64 shrink-0 flex-col bg-slate-950 px-4 py-6 text-white">
      <div className="flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 font-black">
          OG
        </div>
        <div>
          <div className="font-bold">OpsGPT</div>
          <div className="text-xs text-slate-400">Incident intelligence</div>
        </div>
      </div>

      <nav className="mt-10 grid gap-2">
        <SidebarLink itemKey="projects" to="/projects">
          Project selector
        </SidebarLink>
        <SidebarLink
          itemKey="dashboard"
          to={
            selectedProjectId ? `${projectBase}/dashboard` : "/projects"
          }
        >
          Dashboard
        </SidebarLink>
        <SidebarLink
          itemKey="incidents"
          to={
            selectedProjectId ? `${projectBase}/incidents` : "/projects"
          }
        >
          Incidents
        </SidebarLink>
        <SidebarLink itemKey="knowledgeBase" to="/knowledge-base">
          Knowledge base
        </SidebarLink>
        <SidebarLink itemKey="profile" to="/profile">
          Profile
        </SidebarLink>
        {user?.role === "admin" && (
          <SidebarLink itemKey="adminProjects" to="/admin/projects">
            Admin projects
          </SidebarLink>
        )}
      </nav>

      <div className="mt-auto rounded-xl border border-slate-800 bg-slate-900 p-3">
        <p className="text-xs uppercase tracking-wide text-slate-500">
          Signed in as
        </p>
        <p className="mt-1 truncate text-sm font-semibold">{user?.name}</p>
        <p className="truncate text-xs text-slate-400">{user?.email}</p>
      </div>
    </aside>
  );
}

export default Sidebar;
