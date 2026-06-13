import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import { getCurrentUser, loginUser, logoutUser } from "../api/authApi";
import { TOKEN_STORAGE_KEY, USER_STORAGE_KEY } from "../utils/constants";

const AuthContext = createContext(null);

function readStoredUser() {
  const storedUser = localStorage.getItem(USER_STORAGE_KEY);
  if (!storedUser) {
    return null;
  }

  try {
    return JSON.parse(storedUser);
  } catch {
    localStorage.removeItem(USER_STORAGE_KEY);
    return null;
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() =>
    localStorage.getItem(TOKEN_STORAGE_KEY),
  );
  const [user, setUser] = useState(readStoredUser);
  const [isLoading, setIsLoading] = useState(Boolean(token));

  const clearAuthentication = useCallback(() => {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
    setToken(null);
    setUser(null);
  }, []);

  const refreshUser = useCallback(async () => {
    if (!localStorage.getItem(TOKEN_STORAGE_KEY)) {
      clearAuthentication();
      return null;
    }

    const currentUser = await getCurrentUser();
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(currentUser));
    setUser(currentUser);
    return currentUser;
  }, [clearAuthentication]);

  useEffect(() => {
    let active = true;

    async function initializeAuthentication() {
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const currentUser = await getCurrentUser();
        if (active) {
          localStorage.setItem(
            USER_STORAGE_KEY,
            JSON.stringify(currentUser),
          );
          setUser(currentUser);
        }
      } catch {
        if (active) {
          clearAuthentication();
        }
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    initializeAuthentication();
    return () => {
      active = false;
    };
  }, [token, clearAuthentication]);

  const login = useCallback(async (email, password) => {
    const result = await loginUser({ email, password });
    localStorage.setItem(TOKEN_STORAGE_KEY, result.access_token);
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(result.user));
    setToken(result.access_token);
    setUser(result.user);
    return result.user;
  }, []);

  const logout = useCallback(async () => {
    try {
      if (localStorage.getItem(TOKEN_STORAGE_KEY)) {
        await logoutUser();
      }
    } finally {
      clearAuthentication();
    }
  }, [clearAuthentication]);

  const value = useMemo(
    () => ({
      user,
      token,
      isLoading,
      isAuthenticated: Boolean(token && user),
      login,
      logout,
      refreshUser,
    }),
    [user, token, isLoading, login, logout, refreshUser],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
