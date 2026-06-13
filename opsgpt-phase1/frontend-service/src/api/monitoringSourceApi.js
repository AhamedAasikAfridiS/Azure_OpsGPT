import apiClient from "./apiClient";

export async function getMonitoringSources(projectId) {
  const response = await apiClient.get(
    `/projects/${projectId}/monitoring-sources`,
  );
  return response.data;
}

export async function createMonitoringSource(projectId, payload) {
  const response = await apiClient.post(
    `/projects/${projectId}/monitoring-sources`,
    payload,
  );
  return response.data;
}

export async function updateMonitoringSource(projectId, sourceId, payload) {
  const response = await apiClient.patch(
    `/projects/${projectId}/monitoring-sources/${sourceId}`,
    payload,
  );
  return response.data;
}

export async function deactivateMonitoringSource(projectId, sourceId) {
  await apiClient.delete(
    `/projects/${projectId}/monitoring-sources/${sourceId}`,
  );
}
