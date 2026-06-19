export default function ErrorMessage({ message }) {
  return (
    <div className="error-state" role="alert">
      {message || "Something went wrong."}
    </div>
  );
}
