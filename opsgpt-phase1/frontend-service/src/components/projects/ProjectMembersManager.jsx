import { Trash2 } from "lucide-react";
import { useState } from "react";

import api from "../../api/client.js";
import StatusBadge from "../StatusBadge.jsx";
import EmptyState from "../ui/EmptyState.jsx";
import ErrorMessage from "../ui/ErrorMessage.jsx";
import UserSearchSelect from "./UserSearchSelect.jsx";

export default function ProjectMembersManager({ members, onRefresh, projectId }) {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function assignUser(user) {
    setError("");
    setMessage("");
    try {
      await api.post(`/projects/${projectId}/members`, { user_id: user.id });
      setMessage(`${user.name} assigned to project`);
      await onRefresh();
      return true;
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(detail === "User is already assigned to this project" ? "That user is already assigned to this project." : detail || "Could not assign member");
      return false;
    }
  }

  async function removeUser(userId) {
    setError("");
    setMessage("");
    try {
      await api.delete(`/projects/${projectId}/members/${userId}`);
      setMessage("Member removed");
      await onRefresh();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not remove member");
    }
  }

  return (
    <section className="section-block">
      <div className="section-heading">
        <h2>Members</h2>
      </div>
      {error && <ErrorMessage message={error} />}
      {message && <div className="notice-state" role="status">{message}</div>}
      <UserSearchSelect onAssign={assignUser} />
      {members.length === 0 ? (
        <EmptyState title="No assigned members" />
      ) : (
        <div className="result-list">
          {members.map((member) => (
            <div className="result-row" key={member.id}>
              <div>
                <strong>{member.user.name}</strong>
                <span>{member.user.email}</span>
                <StatusBadge value={member.user.role} />
              </div>
              <button className="danger-button compact-button" onClick={() => removeUser(member.user_id)} type="button">
                <Trash2 size={16} aria-hidden="true" />
                Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
