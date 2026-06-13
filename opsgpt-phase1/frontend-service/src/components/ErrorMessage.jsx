function normalizeError(error) {
  const detail = error?.response?.data?.detail;
  if (typeof detail === "string") {
    return detail;
  }
  if (detail) {
    return JSON.stringify(detail);
  }
  return error?.message || String(error || "An unexpected error occurred.");
}

function ErrorMessage({ error }) {
  if (!error) {
    return null;
  }
  return (
    <div className="error-message" role="alert">
      {normalizeError(error)}
    </div>
  );
}

export default ErrorMessage;
