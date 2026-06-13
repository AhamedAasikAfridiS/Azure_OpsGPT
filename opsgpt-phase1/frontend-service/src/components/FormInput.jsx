function FormInput({ label, as = "input", className = "", ...props }) {
  const Component = as;
  return (
    <label className="grid gap-2 text-sm font-medium text-slate-700">
      {label}
      <Component
        className={`rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-2 focus:ring-brand-100 ${className}`}
        {...props}
      />
    </label>
  );
}

export default FormInput;
