import Breadcrumbs from "../navigation/Breadcrumbs.jsx";

export default function PageHeader({ actions, breadcrumbs, description, title }) {
  return (
    <section className="page-header" aria-labelledby="page-title">
      <div>
        <Breadcrumbs items={breadcrumbs} />
        <h1 id="page-title">{title}</h1>
        {description && <p>{description}</p>}
      </div>
      {actions && <div className="action-row">{actions}</div>}
    </section>
  );
}
