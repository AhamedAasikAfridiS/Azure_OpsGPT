function DashboardCard({ label, value, tone = "default" }) {
  return (
    <article className={`dashboard-card dashboard-card--${tone}`}>
      <span>{label}</span>
      <strong>{value ?? 0}</strong>
    </article>
  );
}

export default DashboardCard;
