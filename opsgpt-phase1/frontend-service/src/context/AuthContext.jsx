import { createContext, useContext, useEffect, useMemo, useState } from "react";

import api from "../api/client.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("opsgpt_token"));
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("opsgpt_user");
    return raw ? JSON.parse(raw) : null;
  });
  const [loading, setLoading] = useState(Boolean(token));

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }
    api
      .get("/auth/me")
      .then((response) => {
        setUser(response.data);
        localStorage.setItem("opsgpt_user", JSON.stringify(response.data));
      })
      .catch(() => {
        localStorage.removeItem("opsgpt_token");
        localStorage.removeItem("opsgpt_user");
        setToken(null);
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, [token]);

  async function login(email, password) {
    const response = await api.post("/auth/login", { email, password });
    localStorage.setItem("opsgpt_token", response.data.access_token);
    localStorage.setItem("opsgpt_user", JSON.stringify(response.data.user));
    setToken(response.data.access_token);
    setUser(response.data.user);
    return response.data.user;
  }

  function logout() {
    localStorage.removeItem("opsgpt_token");
    localStorage.removeItem("opsgpt_user");
    localStorage.removeItem("opsgpt_selected_project");
    setToken(null);
    setUser(null);
  }

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      isAuthenticated: Boolean(token && user),
      login,
      logout,
      isAdmin: user?.role === "admin",
      canEditIncidents: user?.role === "senior_engineer" || user?.role === "admin"
    }),
    [token, user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
