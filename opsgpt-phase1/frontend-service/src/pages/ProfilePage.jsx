import { useAuth } from "../context/AuthContext.jsx";

export default function ProfilePage() {
  const { user } = useAuth();

  return (
    <section className="page-stack">
      <div className="page-header">
        <div>
          <h1>Profile</h1>
          <p>{user?.email}</p>
        </div>
      </div>
      <section className="section-block">
        <dl className="meta-grid wide">
          <div>
            <dt>Name</dt>
            <dd>{user?.name}</dd>
          </div>
          <div>
            <dt>Email</dt>
            <dd>{user?.email}</dd>
          </div>
          <div>
            <dt>Role</dt>
            <dd>{user?.role}</dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>{user?.is_active ? "Active" : "Inactive"}</dd>
          </div>
        </dl>
      </section>
    </section>
  );
}
