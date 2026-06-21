import { ShieldCheck } from "lucide-react";
import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import Input from "../components/ui/Input.jsx";

export default function LoginPage() {
  const { authError, authProvider, isAuthenticated, isEntraConfigured, login, loginWithMicrosoft } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
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

  async function handleMicrosoftSignIn() {
    setLoading(true);
    setError("");
    try {
      await loginWithMicrosoft();
    } catch (err) {
      setError(err.message || "Microsoft Entra ID sign-in failed");
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
        {authProvider === "entra" ? (
          <div className="form">
            <p className="muted-text">Use your organization account to continue to OpsGPT.</p>
            {(error || authError) && <div className="form-error" role="alert">{error || authError}</div>}
            <button
              className="primary-button"
              disabled={loading || !isEntraConfigured}
              onClick={handleMicrosoftSignIn}
              type="button"
            >
              <ShieldCheck size={18} />
              {loading ? "Redirecting to Microsoft" : "Sign in with Microsoft"}
            </button>
          </div>
        ) : (
          <form className="form" onSubmit={handleSubmit}>
            <Input
              autoComplete="email"
              id="email"
              label="Email"
              onChange={(event) => setEmail(event.target.value)}
              required
              type="email"
              value={email}
            />
            <Input
              autoComplete="current-password"
              id="password"
              label="Password"
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              value={password}
            />
            {error && <div className="form-error" role="alert">{error}</div>}
            <button className="primary-button" disabled={loading} type="submit">
              <ShieldCheck size={18} />
              {loading ? "Signing in" : "Sign in"}
            </button>
          </form>
        )}
      </section>
    </main>
  );
}
