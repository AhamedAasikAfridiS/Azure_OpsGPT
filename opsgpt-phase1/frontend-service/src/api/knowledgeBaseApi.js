import apiClient from "./apiClient";

export async function getKnowledgeBase(params = {}) {
  const response = await apiClient.get("/knowledge-base", { params });
  return response.data;
}

export async function getKnowledgeBaseEntry(entryId) {
  const response = await apiClient.get(`/knowledge-base/${entryId}`);
  return response.data;
}
