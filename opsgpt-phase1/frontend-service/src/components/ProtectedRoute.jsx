import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import LoadingState from "./states/LoadingState.jsx";

export default function ProtectedRoute() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingState label="Loading" fullPage />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
