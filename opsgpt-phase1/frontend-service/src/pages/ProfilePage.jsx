import { useState } from "react";

import ErrorMessage from "../components/ErrorMessage";
import { useAuth } from "../context/AuthContext";
import { formatDateTime, formatLabel } from "../utils/formatters";
import { isReadOnlyUser } from "../utils/roleUtils";

function ProfilePage() {
  const { user, refreshUser } = useAuth();
  const [error, setError] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  async function handleRefresh() {
    setError(null);
    setIsRefreshing(true);
    try {
      await refreshUser();
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsRefreshing(false);
    }
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">Account</span>
          <h1>Profile</h1>
        </div>
        <button
          className="button button--secondary"
          type="button"
          onClick={handleRefresh}
          disabled={isRefreshing}
        >
          {isRefreshing ? "Refreshing..." : "Refresh profile"}
        </button>
      </div>

      <ErrorMessage error={error} />

      <section className="profile-card">
        <div className="profile-avatar">
          {user?.name
            ?.split(" ")
            .map((part) => part[0])
            .join("")
            .slice(0, 2)
            .toUpperCase()}
        </div>
        <div className="profile-card__content">
          <h2>{user?.name}</h2>
          <p>{user?.email}</p>
          <dl className="definition-list">
            <div>
              <dt>Role</dt>
              <dd>{formatLabel(user?.role)}</dd>
            </div>
            <div>
              <dt>Access</dt>
              <dd>
                {isReadOnlyUser(user)
                  ? "Read-only incident access"
                  : "Incident editor and resolver"}
              </dd>
            </div>
            <div>
              <dt>Member since</dt>
              <dd>{formatDateTime(user?.created_at)}</dd>
            </div>
          </dl>
        </div>
      </section>
    </div>
  );
}

export default ProfilePage;
