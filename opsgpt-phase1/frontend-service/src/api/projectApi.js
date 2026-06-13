import apiClient from "./apiClient";

function removeEmptyParams(params) {
  return Object.fromEntries(
    Object.entries(params).filter(
      ([, value]) => value !== "" && value !== null && value !== undefined,
    ),
  );
}

export async function getProjects() {
  const response = await apiClient.get("/projects");
  return response.data;
}

export async function getProject(projectId) {
  const response = await apiClient.get(`/projects/${projectId}`);
  return response.data;
}

export async function createProject(payload) {
  const response = await apiClient.post("/projects", payload);
  return response.data;
}

export async function updateProject(projectId, payload) {
  const response = await apiClient.patch(`/projects/${projectId}`, payload);
  return response.data;
}

export async function deactivateProject(projectId) {
  await apiClient.delete(`/projects/${projectId}`);
}

export async function getProjectDashboardSummary(projectId) {
  const response = await apiClient.get(
    `/projects/${projectId}/dashboard/summary`,
  );
  return response.data;
}

export async function getProjectIncidents(projectId, filters = {}) {
  const response = await apiClient.get(`/projects/${projectId}/incidents`, {
    params: removeEmptyParams(filters),
  });
  return response.data;
}

export async function getProjectIncident(projectId, incidentId) {
  const response = await apiClient.get(
    `/projects/${projectId}/incidents/${incidentId}`,
  );
  return response.data;
}

export async function getProjectMembers(projectId) {
  const response = await apiClient.get(`/projects/${projectId}/members`);
  return response.data;
}

export async function addProjectMember(projectId, payload) {
  const response = await apiClient.post(
    `/projects/${projectId}/members`,
    payload,
  );
  return response.data;
}

export async function removeProjectMember(projectId, userId) {
  await apiClient.delete(`/projects/${projectId}/members/${userId}`);
}

export async function getUsers() {
  const response = await apiClient.get("/users");
  return response.data;
}
