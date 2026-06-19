export default function Select({ children, className = "", error, id, label, ...props }) {
  const errorId = error ? `${id}-error` : undefined;

  return (
    <label className={className} htmlFor={id}>
      {label}
      <select aria-describedby={errorId} aria-invalid={Boolean(error)} id={id} {...props}>
        {children}
      </select>
      {error && (
        <span className="field-error" id={errorId}>
          {error}
        </span>
      )}
    </label>
  );
}
