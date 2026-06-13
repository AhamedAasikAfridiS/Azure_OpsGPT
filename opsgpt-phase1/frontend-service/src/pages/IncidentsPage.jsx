import { useCallback, useEffect, useState } from "react";

import { getIncidents } from "../api/incidentApi";
import ErrorMessage from "../components/ErrorMessage";
import IncidentTable from "../components/IncidentTable";
import LoadingSpinner from "../components/LoadingSpinner";
import {
  INCIDENT_SEVERITIES,
  INCIDENT_STATUSES,
} from "../utils/constants";

const INITIAL_FILTERS = {
  status: "",
  severity: "",
  service_name: "",
  search: "",
};

function IncidentsPage() {
  const [filters, setFilters] = useState(INITIAL_FILTERS);
  const [appliedFilters, setAppliedFilters] = useState(INITIAL_FILTERS);
  const [incidents, setIncidents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadIncidents = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      setIncidents(await getIncidents(appliedFilters));
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsLoading(false);
    }
  }, [appliedFilters]);

  useEffect(() => {
    loadIncidents();
  }, [loadIncidents]);

  function updateFilter(event) {
    const { name, value } = event.target;
    setFilters((current) => ({ ...current, [name]: value }));
  }

  function applyFilters(event) {
    event.preventDefault();
    setAppliedFilters(filters);
  }

  function clearFilters() {
    setFilters(INITIAL_FILTERS);
    setAppliedFilters(INITIAL_FILTERS);
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">Incident operations</span>
          <h1>Incidents</h1>
        </div>
        <span className="result-count">{incidents.length} results</span>
      </div>

      <form className="filter-bar" onSubmit={applyFilters}>
        <input
          name="search"
          value={filters.search}
          onChange={updateFilter}
          placeholder="Search ID, title, or service"
        />
        <input
          name="service_name"
          value={filters.service_name}
          onChange={updateFilter}
          placeholder="Service name"
        />
        <select name="status" value={filters.status} onChange={updateFilter}>
          <option value="">All statuses</option>
          {INCIDENT_STATUSES.map((status) => (
            <option value={status.value} key={status.value}>
              {status.label}
            </option>
          ))}
        </select>
        <select
          name="severity"
          value={filters.severity}
          onChange={updateFilter}
        >
          <option value="">All severities</option>
          {INCIDENT_SEVERITIES.map((severity) => (
            <option value={severity.value} key={severity.value}>
              {severity.label}
            </option>
          ))}
        </select>
        <button className="button button--primary">Apply filters</button>
        <button
          type="button"
          className="button button--secondary"
          onClick={clearFilters}
        >
          Clear
        </button>
      </form>

      <ErrorMessage error={error} />
      {isLoading ? (
        <LoadingSpinner message="Loading incidents..." />
      ) : (
        <IncidentTable incidents={incidents} />
      )}
    </div>
  );
}

export default IncidentsPage;
