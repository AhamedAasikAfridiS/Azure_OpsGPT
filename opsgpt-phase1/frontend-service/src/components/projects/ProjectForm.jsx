import { Plus } from "lucide-react";

import Input from "../ui/Input.jsx";
import Select from "../ui/Select.jsx";
import Textarea from "../ui/Textarea.jsx";

export default function ProjectForm({ form, onChange, onSubmit, saving }) {
  function update(field, value) {
    onChange({ ...form, [field]: value });
  }

  return (
    <form className="form-grid form-card" onSubmit={onSubmit}>
      <Input id="project-name" label="Name" onChange={(event) => update("name", event.target.value)} required value={form.name} />
      <Select
        id="project-environment"
        label="Environment"
        onChange={(event) => update("environment", event.target.value)}
        value={form.environment || "production"}
      >
        <option value="development">Development</option>
        <option value="staging">Staging</option>
        <option value="production">Production</option>
      </Select>
      <Input
        id="project-owner-team"
        label="Owner team"
        onChange={(event) => update("owner_team", event.target.value)}
        value={form.owner_team}
      />
      <Textarea
        className="full-span"
        id="project-description"
        label="Description"
        onChange={(event) => update("description", event.target.value)}
        rows="3"
        value={form.description}
      />
      <button className="primary-button" disabled={saving || !form.name.trim()} type="submit">
        <Plus size={16} aria-hidden="true" />
        Create project
      </button>
    </form>
  );
}
