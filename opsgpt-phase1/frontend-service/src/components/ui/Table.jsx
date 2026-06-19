export default function Table({ children, label }) {
  return (
    <div className="table-wrap" role="region" aria-label={label || "Scrollable table"} tabIndex={0}>
      <table>{children}</table>
    </div>
  );
}
