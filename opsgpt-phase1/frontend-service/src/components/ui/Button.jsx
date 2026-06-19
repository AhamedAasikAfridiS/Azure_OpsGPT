export default function Button({ children, className = "", icon: Icon, type = "button", variant = "primary", ...props }) {
  return (
    <button className={`${variant}-button ${className}`.trim()} type={type} {...props}>
      {Icon && <Icon size={16} aria-hidden="true" />}
      {children}
    </button>
  );
}
