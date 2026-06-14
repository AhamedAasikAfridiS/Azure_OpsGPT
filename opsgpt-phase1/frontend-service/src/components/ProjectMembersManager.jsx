import { useCallback, useEffect, useMemo, useState } from "react";

import {
  addProjectMember,
  getProjectMembers,
  removeProjectMember,
} from "../api/projectApi";
import { getUsers } from "../api/userApi";
import Button from "./Button";
import Card from "./Card";
import ErrorMessage from "./ErrorMessage";
import LoadingSpinner from "./LoadingSpinner";
import UserSearchSelect from "./UserSearchSelect";

function ProjectMembersManager({ projectId, projectName }) {
  const [members, setMembers] = useState([]);
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [membershipData, userData] = await Promise.all([
        getProjectMembers(projectId),
        getUsers(),
      ]);
      setMembers(membershipData);
      setUsers(userData);
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    load();
  }, [load]);

  const userById = useMemo(
    () => Object.fromEntries(users.map((user) => [user.id, user])),
    [users],
  );

  async function assignUser(user) {
    await addProjectMember(projectId, {
      user_id: user.id,
      role_in_project: null,
    });
    await load();
  }

  async function removeMember(userId) {
    try {
      await removeProjectMember(projectId, userId);
      await load();
    } catch (requestError) {
      setError(requestError);
    }
  }

  return (
    <Card>
      <div>
        <p className="eyebrow">Membership</p>
        <h3 className="text-xl font-bold text-slate-900">{projectName}</h3>
        <p className="mt-1 text-sm text-slate-500">
          Search active users and control access to this project.
        </p>
      </div>

      <div className="mt-6">
        <UserSearchSelect
          excludedUserIds={members.map((member) => member.user_id)}
          onAssign={assignUser}
        />
      </div>

      <ErrorMessage error={error} />

      <div className="mt-7">
        <h4 className="text-sm font-bold uppercase tracking-wide text-slate-500">
          Assigned members
        </h4>
        {isLoading ? (
          <LoadingSpinner message="Loading project members..." />
        ) : (
          <div className="mt-3 divide-y divide-slate-100">
            {members.length ? (
              members.map((member) => {
                const user = userById[member.user_id];
                return (
                  <div
                    key={member.user_id}
                    className="flex items-center justify-between gap-4 py-3"
                  >
                    <div>
                      <p className="font-semibold text-slate-800">
                        {user?.name || `User ${member.user_id}`}
                      </p>
                      <p className="text-sm text-slate-500">
                        {user?.email || "User details unavailable"}
                        {user?.role ? ` | ${user.role}` : ""}
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      onClick={() => removeMember(member.user_id)}
                    >
                      Remove
                    </Button>
                  </div>
                );
              })
            ) : (
              <p className="py-5 text-sm text-slate-500">
                No engineers are assigned to this project.
              </p>
            )}
          </div>
        )}
      </div>
    </Card>
  );
}

export default ProjectMembersManager;
