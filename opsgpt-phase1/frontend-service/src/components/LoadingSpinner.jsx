function LoadingSpinner({ message = "Loading...", fullPage = false }) {
  return (
    <div className={`loading-state ${fullPage ? "loading-state--full" : ""}`}>
      <span className="spinner" aria-hidden="true" />
      <span>{message}</span>
    </div>
  );
}

export default LoadingSpinner;
