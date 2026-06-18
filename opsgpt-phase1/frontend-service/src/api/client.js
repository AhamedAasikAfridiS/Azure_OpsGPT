import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_CORE_API_URL || "/api/core",
  timeout: 15000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("opsgpt_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
