import clsx from "clsx";

export default function Button({ children, className = "", icon: Icon, type = "button", variant = "primary", ...props }) {
  return (
    <button className={clsx(`${variant}-button`, className)} type={type} {...props}>
      {Icon && <Icon size={16} aria-hidden="true" />}
      {children}
    </button>
  );
}
