import { useAuth } from "../context/AuthContext.jsx";

export default function RoleGate({ roles, children }) {
  const { user } = useAuth();
  if (!roles.includes(user?.role)) {
    return null;
  }
  return children;
}
