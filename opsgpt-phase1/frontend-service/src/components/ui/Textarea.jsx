export default function Textarea({ className = "", error, id, label, ...props }) {
  const errorId = error ? `${id}-error` : undefined;

  return (
    <label className={className} htmlFor={id}>
      {label}
      <textarea aria-describedby={errorId} aria-invalid={Boolean(error)} id={id} {...props} />
      {error && (
        <span className="field-error" id={errorId}>
          {error}
        </span>
      )}
    </label>
  );
}
