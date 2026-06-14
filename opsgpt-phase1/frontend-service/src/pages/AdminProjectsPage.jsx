import { useState } from "react";
import { Link } from "react-router-dom";

import {
  createProject,
  updateProject,
} from "../api/projectApi";
import Button from "../components/Button";
import Card from "../components/Card";
import EmptyState from "../components/EmptyState";
import ErrorMessage from "../components/ErrorMessage";
import FormInput from "../components/FormInput";
import ProjectMembersManager from "../components/ProjectMembersManager";
import { useProject } from "../context/ProjectContext";

const EMPTY_PROJECT = {
  name: "",
  description: "",
  environment: "production",
  owner_team: "",
  is_active: true,
};

function AdminProjectsPage() {
  const { projects, refreshProjects } = useProject();
  const [form, setForm] = useState(EMPTY_PROJECT);
  const [editingProjectId, setEditingProjectId] = useState(null);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [error, setError] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  async function handleSave(event) {
    event.preventDefault();
    setIsSaving(true);
    setError(null);
    try {
      if (editingProjectId) {
        await updateProject(editingProjectId, form);
      } else {
        await createProject(form);
      }
      setForm(EMPTY_PROJECT);
      setEditingProjectId(null);
      await refreshProjects();
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsSaving(false);
    }
  }

  async function toggleProject(project) {
    setError(null);
    try {
      await updateProject(project.project_id, {
        is_active: !project.is_active,
      });
      await refreshProjects();
    } catch (requestError) {
      setError(requestError);
    }
  }

  function editProject(project) {
    setEditingProjectId(project.project_id);
    setForm({
      name: project.name,
      description: project.description || "",
      environment: project.environment,
      owner_team: project.owner_team || "",
      is_active: project.is_active,
    });
  }

  const selectedProject = projects.find(
    (project) => project.project_id === selectedProjectId,
  );

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Administration</p>
        <h2 className="page-title">Projects and access</h2>
        <p className="mt-2 text-slate-500">
          Create operational boundaries and assign engineers to them.
        </p>
      </div>

      <ErrorMessage error={error} />

      <div className="grid gap-7 xl:grid-cols-[380px_1fr]">
        <Card>
          <h3 className="text-lg font-bold text-slate-900">
            {editingProjectId ? "Edit project" : "Create project"}
          </h3>
          <form className="mt-5 grid gap-4" onSubmit={handleSave}>
            <FormInput
              label="Project name"
              value={form.name}
              onChange={(event) =>
                setForm({ ...form, name: event.target.value })
              }
              required
            />
            <FormInput
              label="Description"
              as="textarea"
              rows="4"
              value={form.description}
              onChange={(event) =>
                setForm({ ...form, description: event.target.value })
              }
            />
            <FormInput
              label="Environment"
              as="select"
              value={form.environment}
              onChange={(event) =>
                setForm({ ...form, environment: event.target.value })
              }
            >
              <option value="production">Production</option>
              <option value="staging">Staging</option>
              <option value="development">Development</option>
            </FormInput>
            <FormInput
              label="Owner team"
              value={form.owner_team}
              onChange={(event) =>
                setForm({ ...form, owner_team: event.target.value })
              }
            />
            <Button type="submit" disabled={isSaving}>
              {isSaving
                ? "Saving..."
                : editingProjectId
                  ? "Save changes"
                  : "Create project"}
            </Button>
            {editingProjectId && (
              <Button
                variant="secondary"
                onClick={() => {
                  setEditingProjectId(null);
                  setForm(EMPTY_PROJECT);
                }}
              >
                Cancel edit
              </Button>
            )}
          </form>
        </Card>

        <div className="space-y-5">
          {projects.length ? (
            projects.map((project) => (
              <Card key={project.project_id} className="p-5">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-bold text-slate-900">
                        {project.name}
                      </h3>
                      <span
                        className={`rounded-full px-2.5 py-1 text-xs font-semibold ${
                          project.is_active
                            ? "bg-emerald-50 text-emerald-700"
                            : "bg-slate-100 text-slate-500"
                        }`}
                      >
                        {project.is_active ? "Active" : "Inactive"}
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-slate-500">
                      {project.project_id} | {project.owner_team || "No owner"}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Button
                      variant="secondary"
                      onClick={() => editProject(project)}
                    >
                      Edit details
                    </Button>
                    <Button
                      variant="secondary"
                      onClick={() => setSelectedProjectId(project.project_id)}
                    >
                      Manage members
                    </Button>
                    <Link
                      className="button button--secondary"
                      to={`/admin/projects/${project.project_id}/sources`}
                    >
                      Monitoring sources
                    </Link>
                    <Button
                      variant={project.is_active ? "danger" : "secondary"}
                      onClick={() => toggleProject(project)}
                    >
                      {project.is_active ? "Deactivate" : "Reactivate"}
                    </Button>
                  </div>
                </div>
              </Card>
            ))
          ) : (
            <EmptyState
              title="No projects created"
              description="Use the form to create the first OpsGPT project."
            />
          )}
        </div>
      </div>

      {selectedProject && (
        <ProjectMembersManager
          projectId={selectedProject.project_id}
          projectName={selectedProject.name}
        />
      )}
    </div>
  );
}

export default AdminProjectsPage;
