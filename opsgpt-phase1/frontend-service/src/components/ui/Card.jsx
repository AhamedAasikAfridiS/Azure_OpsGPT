export default function Card({ children, className = "", title }) {
  return (
    <section className={`section-block ${className}`.trim()}>
      {title && (
        <div className="section-heading">
          <h2>{title}</h2>
        </div>
      )}
      {children}
    </section>
  );
}
