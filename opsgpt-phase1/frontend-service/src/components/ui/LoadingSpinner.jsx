export default function LoadingSpinner({ label = "Loading", fullPage = false }) {
  return (
    <div className={fullPage ? "state-page" : "state-box"} role="status" aria-live="polite">
      <div className="spinner" aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}
