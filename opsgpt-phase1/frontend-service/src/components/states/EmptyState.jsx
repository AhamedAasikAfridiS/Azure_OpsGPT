export default function EmptyState({ title, detail }) {
  return (
    <div className="empty-state">
      <h3>{title}</h3>
      {detail && <p>{detail}</p>}
    </div>
  );
}
