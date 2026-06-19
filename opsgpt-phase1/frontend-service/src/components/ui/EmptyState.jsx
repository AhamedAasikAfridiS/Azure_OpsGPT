export default function EmptyState({ action, detail, title }) {
  return (
    <section className="empty-state" aria-live="polite">
      <h3>{title}</h3>
      {detail && <p>{detail}</p>}
      {action}
    </section>
  );
}
