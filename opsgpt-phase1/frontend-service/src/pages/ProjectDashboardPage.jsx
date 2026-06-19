import { Activity, AlertTriangle, CheckCircle2, Clock } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import api from "../api/client.js";
import StatusBadge from "../components/StatusBadge.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Table from "../components/ui/Table.jsx";
import { useProject } from "../context/ProjectContext.jsx";

export default function ProjectDashboardPage() {
  const { projectId } = useParams();
  const { setSelectedProjectId } = useProject();
  const [summary, setSummary] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setSelectedProjectId(projectId);
    async function loadDashboard() {
      setLoading(true);
      setError("");
      try {
        const [summaryResponse, incidentsResponse] = await Promise.all([
          api.get(`/projects/${projectId}/dashboard/summary`),
          api.get(`/projects/${projectId}/incidents`)
        ]);
        setSummary(summaryResponse.data);
        setIncidents(incidentsResponse.data.slice(0, 6));
      } catch (err) {
        setError(err.response?.data?.detail || "Could not load dashboard");
      } finally {
        setLoading(false);
      }
    }
    loadDashboard();
  }, [projectId, setSelectedProjectId]);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} />;

  const metrics = [
    { label: "Total", value: summary?.total_incidents ?? 0, icon: Activity },
    { label: "Open", value: summary?.open_incidents ?? 0, icon: Clock },
    { label: "Critical", value: summary?.critical_incidents ?? 0, icon: AlertTriangle },
    { label: "Resolved", value: summary?.resolved_incidents ?? 0, icon: CheckCircle2 }
  ];

  return (
    <section className="page-stack">
      <PageHeader
        actions={
          <Link className="secondary-button link-button" to={`/projects/${projectId}/incidents`}>
            Incidents
          </Link>
        }
        breadcrumbs={[
          { label: "Projects", to: "/projects" },
          { label: projectId }
        ]}
        description={projectId}
        title="Project Dashboard"
      />

      <div className="metric-grid">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <article className="metric-card" key={metric.label}>
              <Icon size={22} />
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </article>
          );
        })}
      </div>

      <section className="section-block">
        <div className="section-heading">
          <h2>Recent incidents</h2>
        </div>
        {incidents.length === 0 ? (
          <EmptyState title="No incidents" detail="Project incidents will appear after Alertmanager sends alerts." />
        ) : (
          <Table label="Recent incidents">
              <thead>
                <tr>
                  <th>Incident</th>
                  <th>Service</th>
                  <th>Severity</th>
                  <th>Status</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {incidents.map((incident) => (
                  <tr key={incident.incident_id}>
                    <td>
                      <Link to={`/projects/${projectId}/incidents/${incident.incident_id}`}>{incident.title}</Link>
                    </td>
                    <td>{incident.service_name}</td>
                    <td>
                      <StatusBadge value={incident.severity} />
                    </td>
                    <td>
                      <StatusBadge value={incident.status} />
                    </td>
                    <td>{new Date(incident.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
          </Table>
        )}
      </section>
    </section>
  );
}
