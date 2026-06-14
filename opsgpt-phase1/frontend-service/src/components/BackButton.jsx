import { useNavigate } from "react-router-dom";

function BackButton({ label = "Back", to, fallbackTo = "/projects" }) {
  const navigate = useNavigate();

  function handleClick() {
    if (to) {
      navigate(to);
      return;
    }
    if (window.history.length > 1) {
      navigate(-1);
      return;
    }
    navigate(fallbackTo);
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className="mb-4 inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-600 shadow-sm transition hover:border-brand-200 hover:bg-brand-50 hover:text-brand-700"
    >
      <span aria-hidden="true">&larr;</span>
      {label}
    </button>
  );
}

export default BackButton;
