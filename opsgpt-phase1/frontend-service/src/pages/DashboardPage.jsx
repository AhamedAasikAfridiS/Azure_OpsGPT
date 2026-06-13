import { useEffect, useState } from "react";

import {
  getDashboardSummary,
  getRecentIncidents,
  getSeverityCounts,
  getStatusCounts,
} from "../api/dashboardApi";
import DashboardCard from "../components/DashboardCard";
import ErrorMessage from "../components/ErrorMessage";
import IncidentCard from "../components/IncidentCard";
import LoadingSpinner from "../components/LoadingSpinner";

function DashboardPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;

    async function loadDashboard() {
      try {
        const [summary, severityCounts, statusCounts, recentIncidents] =
          await Promise.all([
            getDashboardSummary(),
            getSeverityCounts(),
            getStatusCounts(),
            getRecentIncidents(),
          ]);
        if (active) {
          setData({
            summary,
            severityCounts,
            statusCounts,
            recentIncidents,
          });
        }
      } catch (requestError) {
        if (active) {
          setError(requestError);
        }
      }
    }

    loadDashboard();
    return () => {
      active = false;
    };
  }, []);

  if (!data && !error) {
    return <LoadingSpinner message="Loading dashboard..." />;
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">Operational overview</span>
          <h1>Dashboard</h1>
        </div>
      </div>

      <ErrorMessage error={error} />

      {data && (
        <>
          <section className="dashboard-grid" aria-label="Incident summary">
            <DashboardCard
              label="Active Incidents"
              value={data.summary.active_incidents}
              tone="primary"
            />
            <DashboardCard
              label="Critical Incidents"
              value={data.summary.critical_incidents}
              tone="critical"
            />
            <DashboardCard
              label="In Progress Incidents"
              value={data.statusCounts.in_progress}
              tone="warning"
            />
            <DashboardCard
              label="Resolved Incidents"
              value={data.summary.resolved_incidents}
              tone="success"
            />
          </section>

          <section className="content-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Latest activity</span>
                <h2>Recent incidents</h2>
              </div>
              <span className="muted">
                Critical: {data.severityCounts.critical || 0}
              </span>
            </div>

            <div className="incident-card-grid">
              {data.recentIncidents.length ? (
                data.recentIncidents.map((incident) => (
                  <IncidentCard
                    incident={incident}
                    key={incident.incident_id}
                  />
                ))
              ) : (
                <div className="empty-state">No incidents have been created.</div>
              )}
            </div>
          </section>
        </>
      )}
    </div>
  );
}

export default DashboardPage;
