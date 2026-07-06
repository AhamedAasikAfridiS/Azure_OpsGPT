import { Activity, AlertTriangle, CheckCircle2, Clock } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Bar, BarChart, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import api from "../api/client.js";
import StatusBadge from "../components/StatusBadge.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Table from "../components/ui/Table.jsx";
import { useProject } from "../context/ProjectContext.jsx";

const chartColors = {
  critical: "#DC2626",
  warning: "#D97706",
  informational: "#0891B2",
  open: "#DC2626",
  investigating: "#D97706",
  mitigated: "#0891B2",
  resolved: "#059669"
};

function countBy(items, field, expectedValues) {
  return expectedValues.map((value) => ({
    name: value,
    value: items.filter((item) => item[field] === value).length
  }));
}

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
        setIncidents(incidentsResponse.data);
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
    { label: "Total", value: summary?.total_incidents ?? 0, icon: Activity, tone: "neutral" },
    { label: "Open", value: summary?.open_incidents ?? 0, icon: Clock, tone: "danger" },
    { label: "Critical", value: summary?.critical_incidents ?? 0, icon: AlertTriangle, tone: "warning" },
    { label: "Resolved", value: summary?.resolved_incidents ?? 0, icon: CheckCircle2, tone: "success" }
  ];
  const recentIncidents = incidents.slice(0, 6);
  const severityData = countBy(incidents, "severity", ["critical", "warning", "informational"]);
  const statusData = countBy(incidents, "status", ["open", "investigating", "mitigated", "resolved"]);
  const hasIncidentData = incidents.length > 0;
  const activeWork = (summary?.open_incidents ?? 0) + (statusData.find((item) => item.name === "investigating")?.value ?? 0);

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

      <section className="command-panel" aria-label="Project operations summary">
        <div className="command-panel-copy">
          <span className="eyebrow">Ops signal</span>
          <h2>Live incident command center</h2>
          <p>
            Track active production pressure, severity distribution, and resolution flow for this project in one
            cockpit-style view.
          </p>
          <div className="signal-chip-row">
            <span className="signal-chip">Project: {projectId}</span>
            <span className="signal-chip">Alert source: Prometheus Alertmanager</span>
            <span className="signal-chip">AI first response enabled</span>
          </div>
        </div>
        <div className="signal-dial" aria-hidden="true">
          <span>{activeWork}</span>
          <small>active</small>
        </div>
      </section>

      <div className="metric-grid">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <article className={`metric-card metric-card-${metric.tone}`} key={metric.label}>
              <Icon size={22} />
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
              <div className="metric-spark" aria-hidden="true">
                <i />
                <i />
                <i />
                <i />
              </div>
            </article>
          );
        })}
      </div>

      <div className="dashboard-grid">
        <section className="section-block chart-card">
          <div className="section-heading">
            <div>
              <h2>Severity radar</h2>
              <p className="muted">Distribution of current project incidents</p>
            </div>
          </div>
          {!hasIncidentData ? (
            <EmptyState title="No severity data" detail="Chart data appears after incidents are created." />
          ) : (
            <div className="chart-frame">
              <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                  <Pie data={severityData} dataKey="value" innerRadius={68} outerRadius={96} paddingAngle={4}>
                    {severityData.map((entry) => (
                      <Cell fill={chartColors[entry.name]} key={entry.name} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ borderColor: "#E2E8F0", borderRadius: 8 }}
                    formatter={(value, name) => [value, name]}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="chart-legend">
                {severityData.map((entry) => (
                  <span key={entry.name}>
                    <i style={{ background: chartColors[entry.name] }} />
                    {entry.name}: {entry.value}
                  </span>
                ))}
              </div>
            </div>
          )}
        </section>

        <section className="section-block chart-card">
          <div className="section-heading">
            <div>
              <h2>Status flow</h2>
              <p className="muted">Open to resolved incident movement</p>
            </div>
          </div>
          {!hasIncidentData ? (
            <EmptyState title="No status data" detail="Status flow appears after alerts create incidents." />
          ) : (
            <div className="chart-frame">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={statusData} margin={{ left: -28, right: 8, top: 16, bottom: 0 }}>
                  <XAxis dataKey="name" tick={{ fill: "#64748B", fontSize: 12 }} tickLine={false} axisLine={false} />
                  <YAxis allowDecimals={false} tick={{ fill: "#64748B", fontSize: 12 }} tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ borderColor: "#E2E8F0", borderRadius: 8 }} />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                    {statusData.map((entry) => (
                      <Cell fill={chartColors[entry.name]} key={entry.name} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </section>
      </div>

      <section className="section-block">
        <div className="section-heading">
          <h2>Recent incidents</h2>
          <Link className="icon-text" to={`/projects/${projectId}/incidents`}>
            View all
          </Link>
        </div>
        {recentIncidents.length === 0 ? (
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
                {recentIncidents.map((incident) => (
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
