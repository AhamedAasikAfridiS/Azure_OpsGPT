import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_CORE_API_URL || "/api/core",
  timeout: 15000
});

let accessTokenProvider = null;

export function setAccessTokenProvider(provider) {
  accessTokenProvider = provider;
}

api.interceptors.request.use(async (config) => {
  const token = accessTokenProvider ? await accessTokenProvider() : localStorage.getItem("opsgpt_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
