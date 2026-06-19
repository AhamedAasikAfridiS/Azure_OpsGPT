import { ArrowRight } from "lucide-react";

export default function ProjectCard({ onOpen, project }) {
  return (
    <article className="resource-card">
      <div>
        <h2>{project.name}</h2>
        <p>{project.description || "No description provided"}</p>
      </div>
      <dl className="meta-grid">
        <div>
          <dt>Project ID</dt>
          <dd>{project.project_id}</dd>
        </div>
        <div>
          <dt>Environment</dt>
          <dd>{project.environment}</dd>
        </div>
        <div>
          <dt>Owner</dt>
          <dd>{project.owner_team || "Unassigned"}</dd>
        </div>
      </dl>
      {onOpen && (
        <button className="primary-button" onClick={() => onOpen(project)} type="button">
          Open
          <ArrowRight size={16} aria-hidden="true" />
        </button>
      )}
    </article>
  );
}
