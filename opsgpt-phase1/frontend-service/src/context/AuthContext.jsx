import { createContext, useContext, useEffect, useMemo, useState } from "react";

import api, { setAccessTokenProvider } from "../api/client.js";
import { authProvider, isEntraConfigured } from "../auth/msalConfig.js";
import {
  getMicrosoftAccessToken,
  initializeMicrosoftAuth,
  signInWithMicrosoft,
  signOutFromMicrosoft
} from "../auth/msalInstance.js";

const AuthContext = createContext(null);

function getApiErrorMessage(error, fallback) {
  return error.response?.data?.detail || fallback;
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() =>
    authProvider === "local" ? localStorage.getItem("opsgpt_token") : null
  );
  const [user, setUser] = useState(() => {
    if (authProvider !== "local") {
      return null;
    }
    const raw = localStorage.getItem("opsgpt_user");
    return raw ? JSON.parse(raw) : null;
  });
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState("");

  useEffect(() => {
    let active = true;

    async function restoreSession() {
      setLoading(true);
      setAuthError("");

      if (authProvider === "entra") {
        if (!isEntraConfigured) {
          if (active) {
            setUser(null);
            setAuthError("Microsoft Entra ID configuration is incomplete.");
            setLoading(false);
          }
          return;
        }

        try {
          const account = await initializeMicrosoftAuth();
          if (!account) {
            if (active) {
              setUser(null);
              setLoading(false);
            }
            return;
          }

          setAccessTokenProvider(getMicrosoftAccessToken);
          const accessToken = await getMicrosoftAccessToken();
          if (!accessToken) {
            if (active) {
              setUser(null);
              setLoading(false);
            }
            return;
          }

          const response = await api.get("/auth/me");
          if (active) {
            setUser(response.data);
          }
        } catch (error) {
          if (active) {
            setUser(null);
            setAuthError(getApiErrorMessage(error, "Microsoft Entra ID sign-in could not be completed."));
          }
        } finally {
          if (active) {
            setLoading(false);
          }
        }
        return;
      }

      setAccessTokenProvider(null);
      if (!token) {
        if (active) {
          setUser(null);
          setLoading(false);
        }
        return;
      }

      try {
        const response = await api.get("/auth/me");
        if (active) {
          setUser(response.data);
          localStorage.setItem("opsgpt_user", JSON.stringify(response.data));
        }
      } catch {
        localStorage.removeItem("opsgpt_token");
        localStorage.removeItem("opsgpt_user");
        if (active) {
          setToken(null);
          setUser(null);
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    restoreSession();
    return () => {
      active = false;
    };
  }, [token]);

  async function login(email, password) {
    if (authProvider === "entra") {
      throw new Error("Local login is disabled. Use Microsoft Entra ID sign-in.");
    }

    const response = await api.post("/auth/login", { email, password });
    localStorage.setItem("opsgpt_token", response.data.access_token);
    localStorage.setItem("opsgpt_user", JSON.stringify(response.data.user));
    setToken(response.data.access_token);
    setUser(response.data.user);
    return response.data.user;
  }

  async function loginWithMicrosoft() {
    setAuthError("");
    await signInWithMicrosoft();
  }

  async function logout() {
    localStorage.removeItem("opsgpt_token");
    localStorage.removeItem("opsgpt_user");
    localStorage.removeItem("opsgpt_selected_project");
    setAccessTokenProvider(null);
    setToken(null);
    setUser(null);
    setAuthError("");

    if (authProvider === "entra") {
      await signOutFromMicrosoft();
    }
  }

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      authError,
      authProvider,
      isEntraConfigured,
      isAuthenticated: Boolean(user),
      login,
      loginWithMicrosoft,
      logout,
      isAdmin: user?.role === "admin",
      canEditIncidents: user?.role === "senior_engineer" || user?.role === "admin"
    }),
    [token, user, loading, authError]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
