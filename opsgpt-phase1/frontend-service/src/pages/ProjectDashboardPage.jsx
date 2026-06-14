import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getProjectDashboardSummary,
  getProjectIncidents,
} from "../api/projectApi";
import DashboardCard from "../components/DashboardCard";
import BackButton from "../components/BackButton";
import ErrorMessage from "../components/ErrorMessage";
import IncidentTable from "../components/IncidentTable";
import LoadingSpinner from "../components/LoadingSpinner";
import { useProject } from "../context/ProjectContext";

function ProjectDashboardPage() {
  const { projectId } = useParams();
  const { projects, selectProject } = useProject();
  const [summary, setSummary] = useState(null);
  const [recent, setRecent] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    selectProject(projectId);
    let active = true;
    async function load() {
      try {
        const [summaryData, incidents] = await Promise.all([
          getProjectDashboardSummary(projectId),
          getProjectIncidents(projectId, { limit: 8 }),
        ]);
        if (active) {
          setSummary(summaryData);
          setRecent(incidents);
        }
      } catch (requestError) {
        if (active) setError(requestError);
      }
    }
    load();
    return () => {
      active = false;
    };
  }, [projectId, selectProject]);

  if (!summary && !error) {
    return <LoadingSpinner message="Loading project dashboard..." />;
  }

  const project = projects.find((item) => item.project_id === projectId);

  return (
    <div className="space-y-8">
      <div>
        <BackButton label="Back to Project Selection" to="/projects" />
        <p className="eyebrow">{project?.environment || "Project"}</p>
        <h2 className="page-title">{project?.name || "Project dashboard"}</h2>
        <p className="mt-2 text-slate-500">
          Project-scoped incident health and recent operational activity.
        </p>
      </div>

      <ErrorMessage error={error} />

      {summary && (
        <div className="dashboard-grid">
          <DashboardCard
            label="Active Incidents"
            value={summary.active_incidents}
            tone="primary"
          />
          <DashboardCard
            label="Critical Incidents"
            value={summary.critical_incidents}
            tone="critical"
          />
          <DashboardCard
            label="Resolved Incidents"
            value={summary.resolved_incidents}
            tone="success"
          />
          <DashboardCard
            label="Total Incidents"
            value={summary.total_incidents}
          />
        </div>
      )}

      <section className="content-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Latest activity</p>
            <h3 className="text-xl font-bold text-slate-900">
              Recent incidents
            </h3>
          </div>
        </div>
        <IncidentTable
          incidents={recent}
          projectId={projectId}
          emptyMessage="No incidents have been created for this project."
        />
      </section>
    </div>
  );
}

export default ProjectDashboardPage;
