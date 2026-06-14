import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { getProjectIncidents } from "../api/projectApi";
import ErrorMessage from "../components/ErrorMessage";
import BackButton from "../components/BackButton";
import IncidentTable from "../components/IncidentTable";
import LoadingSpinner from "../components/LoadingSpinner";
import { useProject } from "../context/ProjectContext";
import {
  INCIDENT_SEVERITIES,
  INCIDENT_STATUSES,
} from "../utils/constants";

const EMPTY_FILTERS = {
  status: "",
  severity: "",
  service_name: "",
  search: "",
};

function ProjectIncidentsPage() {
  const { projectId } = useParams();
  const { projects, selectProject } = useProject();
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [appliedFilters, setAppliedFilters] = useState(EMPTY_FILTERS);
  const [incidents, setIncidents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      setIncidents(await getProjectIncidents(projectId, appliedFilters));
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsLoading(false);
    }
  }, [projectId, appliedFilters]);

  useEffect(() => {
    selectProject(projectId);
    load();
  }, [projectId, selectProject, load]);

  const project = projects.find((item) => item.project_id === projectId);

  return (
    <div className="space-y-7">
      <div>
        <BackButton
          label="Back to Project Dashboard"
          to={`/projects/${projectId}/dashboard`}
        />
        <p className="eyebrow">{project?.name || "Project"}</p>
        <h2 className="page-title">Incidents</h2>
        <p className="mt-2 text-slate-500">
          Investigate alerts and incident response for this project.
        </p>
      </div>

      <form
        className="filter-bar"
        onSubmit={(event) => {
          event.preventDefault();
          setAppliedFilters(filters);
        }}
      >
        <input
          name="search"
          value={filters.search}
          onChange={(event) =>
            setFilters({ ...filters, search: event.target.value })
          }
          placeholder="Search incidents"
        />
        <input
          name="service_name"
          value={filters.service_name}
          onChange={(event) =>
            setFilters({ ...filters, service_name: event.target.value })
          }
          placeholder="Service name"
        />
        <select
          value={filters.status}
          onChange={(event) =>
            setFilters({ ...filters, status: event.target.value })
          }
        >
          <option value="">All statuses</option>
          {INCIDENT_STATUSES.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>
        <select
          value={filters.severity}
          onChange={(event) =>
            setFilters({ ...filters, severity: event.target.value })
          }
        >
          <option value="">All severities</option>
          {INCIDENT_SEVERITIES.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>
        <button className="button button--primary">Apply</button>
        <button
          type="button"
          className="button button--secondary"
          onClick={() => {
            setFilters(EMPTY_FILTERS);
            setAppliedFilters(EMPTY_FILTERS);
          }}
        >
          Clear
        </button>
      </form>

      <ErrorMessage error={error} />
      {isLoading ? (
        <LoadingSpinner message="Loading project incidents..." />
      ) : (
        <IncidentTable incidents={incidents} projectId={projectId} />
      )}
    </div>
  );
}

export default ProjectIncidentsPage;
