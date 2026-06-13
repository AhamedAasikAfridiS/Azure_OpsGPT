import { formatDateTime, formatLabel } from "../utils/formatters";

function Timeline({ events }) {
  if (!events?.length) {
    return <div className="empty-state">No timeline events available.</div>;
  }

  return (
    <ol className="timeline">
      {events.map((event) => (
        <li key={event.id}>
          <span className="timeline__marker" aria-hidden="true" />
          <div className="timeline__content">
            <div className="timeline__heading">
              <strong>{formatLabel(event.event_type)}</strong>
              <time>{formatDateTime(event.created_at)}</time>
            </div>
            <p>{event.message}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}

export default Timeline;
