import apiClient from "./apiClient";

export async function getDashboardSummary() {
  const response = await apiClient.get("/dashboard/summary");
  return response.data;
}

export async function getSeverityCounts() {
  const response = await apiClient.get("/dashboard/severity-counts");
  return response.data;
}

export async function getStatusCounts() {
  const response = await apiClient.get("/dashboard/status-counts");
  return response.data;
}

export async function getRecentIncidents(limit = 10) {
  const response = await apiClient.get("/dashboard/recent-incidents", {
    params: { limit },
  });
  return response.data;
}
