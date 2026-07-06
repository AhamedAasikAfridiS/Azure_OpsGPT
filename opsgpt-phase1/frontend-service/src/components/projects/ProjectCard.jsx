import { ArrowRight, FolderKanban, ServerCog, ShieldCheck, Users } from "lucide-react";

export default function ProjectCard({ onOpen, project }) {
  return (
    <article className="resource-card project-card">
      <div className="project-card-glow" aria-hidden="true" />
      <div className="project-card-header">
        <div className="project-card-icon" aria-hidden="true">
          <FolderKanban size={22} />
        </div>
        <span className="badge informational">{project.environment}</span>
      </div>
      <div className="project-card-copy">
        <h2>{project.name}</h2>
        <p>{project.description || "No description provided"}</p>
      </div>
      <dl className="meta-grid project-meta-grid">
        <div>
          <dt>
            <ShieldCheck size={13} aria-hidden="true" />
            Project ID
          </dt>
          <dd>{project.project_id}</dd>
        </div>
        <div>
          <dt>
            <ServerCog size={13} aria-hidden="true" />
            Environment
          </dt>
          <dd>{project.environment}</dd>
        </div>
        <div>
          <dt>
            <Users size={13} aria-hidden="true" />
            Owner
          </dt>
          <dd>{project.owner_team || "Unassigned"}</dd>
        </div>
      </dl>
      {onOpen && (
        <button className="primary-button project-open-button" onClick={() => onOpen(project)} type="button">
          Open command center
          <ArrowRight size={16} aria-hidden="true" />
        </button>
      )}
    </article>
  );
}
