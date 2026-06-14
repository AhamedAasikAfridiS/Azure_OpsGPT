import { useEffect, useState } from "react";

import { searchUsers } from "../api/userApi";
import { formatLabel } from "../utils/formatters";
import Button from "./Button";
import ErrorMessage from "./ErrorMessage";

function UserSearchSelect({ excludedUserIds = [], onAssign }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [isSearching, setIsSearching] = useState(false);
  const [isAssigning, setIsAssigning] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    const searchText = query.trim();
    if (!searchText || selectedUser) {
      setResults([]);
      setIsSearching(false);
      return undefined;
    }

    let active = true;
    setIsSearching(true);
    const timer = window.setTimeout(async () => {
      setError(null);
      try {
        const users = await searchUsers(searchText);
        if (active) {
          setResults(
            users.filter((user) => !excludedUserIds.includes(user.id)),
          );
        }
      } catch (requestError) {
        if (active) setError(requestError);
      } finally {
        if (active) setIsSearching(false);
      }
    }, 300);

    return () => {
      active = false;
      window.clearTimeout(timer);
    };
  }, [query, selectedUser, excludedUserIds]);

  function selectUser(user) {
    setSelectedUser(user);
    setQuery(`${user.name} (${user.email})`);
    setResults([]);
    setError(null);
    setSuccessMessage("");
  }

  async function assignSelectedUser() {
    if (!selectedUser) return;
    setIsAssigning(true);
    setError(null);
    setSuccessMessage("");
    try {
      await onAssign(selectedUser);
      setSuccessMessage(`${selectedUser.name} was assigned successfully.`);
      setSelectedUser(null);
      setQuery("");
      setResults([]);
    } catch (requestError) {
      setError(requestError);
    } finally {
      setIsAssigning(false);
    }
  }

  return (
    <div className="space-y-3">
      <label className="grid gap-2 text-sm font-semibold text-slate-700">
        Find an employee
        <input
          value={query}
          onChange={(event) => {
            setQuery(event.target.value);
            setSelectedUser(null);
            setSuccessMessage("");
          }}
          placeholder="Search users by name, email, or role..."
          className="rounded-lg border border-slate-300 bg-white px-3 py-2.5 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
        />
      </label>

      {isSearching && (
        <p className="text-sm text-slate-500">Searching users...</p>
      )}

      {!isSearching && query.trim() && !selectedUser && (
        <div className="max-h-64 overflow-auto rounded-xl border border-slate-200 bg-white shadow-lg">
          {results.length ? (
            results.map((user) => (
              <button
                type="button"
                key={user.id}
                onClick={() => selectUser(user)}
                className="flex w-full items-center justify-between gap-4 border-b border-slate-100 px-4 py-3 text-left last:border-0 hover:bg-brand-50"
              >
                <div>
                  <p className="font-semibold text-slate-800">{user.name}</p>
                  <p className="text-sm text-slate-500">{user.email}</p>
                </div>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
                  {formatLabel(user.role)}
                </span>
              </button>
            ))
          ) : (
            <p className="px-4 py-5 text-center text-sm text-slate-500">
              No unassigned users found.
            </p>
          )}
        </div>
      )}

      {selectedUser && (
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-brand-200 bg-brand-50 p-3">
          <div>
            <p className="font-semibold text-slate-800">
              {selectedUser.name}
            </p>
            <p className="text-sm text-slate-500">{selectedUser.email}</p>
          </div>
          <Button onClick={assignSelectedUser} disabled={isAssigning}>
            {isAssigning ? "Assigning..." : "Assign to Project"}
          </Button>
        </div>
      )}

      <ErrorMessage error={error} />
      {successMessage && (
        <div className="success-message">{successMessage}</div>
      )}
    </div>
  );
}

export default UserSearchSelect;
