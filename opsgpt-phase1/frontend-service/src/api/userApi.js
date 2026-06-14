import apiClient from "./apiClient";

export async function searchUsers(query, limit = 20) {
  const response = await apiClient.get("/users/search", {
    params: { query, limit },
  });
  return response.data;
}

export async function getUsers() {
  const response = await apiClient.get("/users");
  return response.data;
}
