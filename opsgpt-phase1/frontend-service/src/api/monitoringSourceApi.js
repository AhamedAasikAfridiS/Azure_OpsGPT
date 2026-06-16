import apiClient from "./apiClient";

export const getMonitoringSources = (projectId) =>
  apiClient.get(`/projects/${projectId}/monitoring-sources`);

export const getMonitoringSource = (projectId, sourceId) =>
  apiClient.get(`/projects/${projectId}/monitoring-sources/${sourceId}`);

export const createMonitoringSource = (projectId, payload) =>
  apiClient.post(`/projects/${projectId}/monitoring-sources`, payload);

export const updateMonitoringSource = (projectId, sourceId, payload) =>
  apiClient.patch(`/projects/${projectId}/monitoring-sources/${sourceId}`, payload);

export const deleteMonitoringSource = (projectId, sourceId) =>
  apiClient.delete(`/projects/${projectId}/monitoring-sources/${sourceId}`);

export default {
  getMonitoringSources,
  getMonitoringSource,
  createMonitoringSource,
  updateMonitoringSource,
  deleteMonitoringSource,
};
