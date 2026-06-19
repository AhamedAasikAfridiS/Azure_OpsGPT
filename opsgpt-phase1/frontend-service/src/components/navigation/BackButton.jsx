import { ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

export default function BackButton({ to, label = "Back" }) {
  return (
    <Link className="back-link" to={to}>
      <ArrowLeft size={16} aria-hidden="true" />
      {label}
    </Link>
  );
}
