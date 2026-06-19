import { Plus } from "lucide-react";

import Input from "../ui/Input.jsx";
import Select from "../ui/Select.jsx";
import Textarea from "../ui/Textarea.jsx";

export default function MonitoringSourceForm({ form, onChange, onSubmit }) {
  function update(field, value) {
    onChange({ ...form, [field]: value });
  }

  return (
    <form className="form-grid form-card" onSubmit={onSubmit}>
      <Select id="source-type" label="Source type" onChange={(event) => update("source_type", event.target.value)} value={form.source_type}>
        <option value="prometheus_alertmanager">Prometheus Alertmanager</option>
      </Select>
      <Input
        id="source-name"
        label="Source name"
        onChange={(event) => update("source_name", event.target.value)}
        required
        value={form.source_name}
      />
      <Input
        id="prometheus-url"
        label="Prometheus URL"
        onChange={(event) => update("prometheus_url", event.target.value)}
        value={form.prometheus_url}
      />
      <Input
        id="alertmanager-url"
        label="Alertmanager URL"
        onChange={(event) => update("alertmanager_url", event.target.value)}
        value={form.alertmanager_url}
      />
      <Input
        id="dashboard-url"
        label="Dashboard URL"
        onChange={(event) => update("dashboard_url", event.target.value)}
        value={form.dashboard_url}
      />
      <Textarea
        className="full-span"
        id="source-description"
        label="Description"
        onChange={(event) => update("description", event.target.value)}
        rows="3"
        value={form.description}
      />
      <button className="primary-button" disabled={!form.source_name.trim()} type="submit">
        <Plus size={16} aria-hidden="true" />
        Create source
      </button>
    </form>
  );
}
