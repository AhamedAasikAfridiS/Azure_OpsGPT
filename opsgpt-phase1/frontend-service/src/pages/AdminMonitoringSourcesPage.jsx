import { useEffect, useState } from "react";
import { Navigate, useParams } from "react-router-dom";

import api from "../api/client.js";
import BackButton from "../components/navigation/BackButton.jsx";
import MonitoringSourceCard from "../components/projects/MonitoringSourceCard.jsx";
import MonitoringSourceForm from "../components/projects/MonitoringSourceForm.jsx";
import ProjectMembersManager from "../components/projects/ProjectMembersManager.jsx";
import EmptyState from "../components/states/EmptyState.jsx";
import ErrorState from "../components/states/ErrorState.jsx";
import LoadingState from "../components/states/LoadingState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function AdminMonitoringSourcesPage() {
  const { isAdmin } = useAuth();
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [sources, setSources] = useState([]);
  const [members, setMembers] = useState([]);
  const [sourceForm, setSourceForm] = useState({
    source_type: "prometheus_alertmanager",
    source_name: "",
    prometheus_url: "",
    alertmanager_url: "",
    dashboard_url: "",
    description: ""
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  async function loadData() {
    setLoading(true);
    setError("");
    try {
      const [projectResponse, sourcesResponse, membersResponse] = await Promise.all([
        api.get(`/projects/${projectId}`),
        api.get(`/projects/${projectId}/monitoring-sources`),
        api.get(`/projects/${projectId}/members`)
      ]);
      setProject(projectResponse.data);
      setSources(sourcesResponse.data);
      setMembers(membersResponse.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not load project configuration");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [projectId]);

  if (!isAdmin) {
    return <Navigate to="/projects" replace />;
  }

  async function createSource(event) {
    event.preventDefault();
    setError("");
    setNotice("");
    try {
      await api.post(`/projects/${projectId}/monitoring-sources`, sourceForm);
      setSourceForm({
        source_type: "prometheus_alertmanager",
        source_name: "",
        prometheus_url: "",
        alertmanager_url: "",
        dashboard_url: "",
        description: ""
      });
      await loadData();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create monitoring source");
    }
  }

  if (loading) return <LoadingState />;

  return (
    <section className="page-stack">
      <BackButton to="/admin/projects" />
      <PageHeader
        breadcrumbs={[
          { label: "Admin", to: "/admin/projects" },
          { label: project?.name || projectId }
        ]}
        description={projectId}
        title={project?.name || "Project Configuration"}
      />

      {error && <ErrorState message={error} />}
      {notice && <div className="notice-state">{notice}</div>}

      <section className="section-block">
        <div className="section-heading">
          <h2>Monitoring sources</h2>
        </div>
        <MonitoringSourceForm form={sourceForm} onChange={setSourceForm} onSubmit={createSource} />

        {sources.length === 0 ? (
          <EmptyState title="No monitoring sources" />
        ) : (
          <div className="source-list">
            {sources.map((source) => <MonitoringSourceCard key={source.source_id} source={source} />)}
          </div>
        )}
      </section>

      <ProjectMembersManager members={members} onRefresh={loadData} projectId={projectId} />
    </section>
  );
}
