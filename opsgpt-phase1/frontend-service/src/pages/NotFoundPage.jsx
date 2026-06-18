import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <main className="state-page">
      <h1>Page not found</h1>
      <Link className="primary-button link-button" to="/projects">
        Projects
      </Link>
    </main>
  );
}
