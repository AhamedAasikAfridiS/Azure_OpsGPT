import apiClient from "./apiClient";

function removeEmptyParams(params) {
  return Object.fromEntries(
    Object.entries(params).filter(
      ([, value]) => value !== "" && value !== null && value !== undefined,
    ),
  );
}

export async function getIncidents(filters = {}) {
  const response = await apiClient.get("/incidents", {
    params: removeEmptyParams(filters),
  });
  return response.data;
}

export async function getIncident(incidentId) {
  const response = await apiClient.get(`/incidents/${incidentId}`);
  return response.data;
}

export async function updateIncidentStatus(incidentId, status) {
  const response = await apiClient.patch(`/incidents/${incidentId}/status`, {
    status,
  });
  return response.data;
}

export async function addResolutionNote(incidentId, notes) {
  const response = await apiClient.post(
    `/incidents/${incidentId}/resolution-notes`,
    { notes },
  );
  return response.data;
}

export async function getIncidentTimeline(incidentId) {
  const response = await apiClient.get(`/incidents/${incidentId}/timeline`);
  return response.data;
}

export async function getSimilarIncidents(incidentId) {
  const response = await apiClient.get(`/incidents/${incidentId}/similar`);
  return response.data;
}

export async function getProjectIncident(projectId, incidentId) {
  const response = await apiClient.get(
    `/projects/${projectId}/incidents/${incidentId}`,
  );
  return response.data;
}
