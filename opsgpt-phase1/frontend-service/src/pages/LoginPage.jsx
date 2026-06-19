import { ShieldCheck } from "lucide-react";
import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import Input from "../components/ui/Input.jsx";

export default function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("admin@company.com");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/projects" replace />;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login(email, password);
      navigate("/projects", { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || "Sign in failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-panel">
        <div className="login-brand">
          <div className="brand-mark large">O</div>
          <div>
            <h1>OpsGPT</h1>
            <p>AI First Responder for Production Incidents</p>
          </div>
        </div>
        <form className="form" onSubmit={handleSubmit}>
          <Input
            autoComplete="email"
            id="email"
            label="Email"
            onChange={(event) => setEmail(event.target.value)}
            type="email"
            value={email}
          />
          <Input
            autoComplete="current-password"
            id="password"
            label="Password"
            onChange={(event) => setPassword(event.target.value)}
            type="password"
            value={password}
          />
          {error && <div className="form-error">{error}</div>}
          <button className="primary-button" disabled={loading} type="submit">
            <ShieldCheck size={18} />
            {loading ? "Signing in" : "Sign in"}
          </button>
        </form>
      </section>
    </main>
  );
}
