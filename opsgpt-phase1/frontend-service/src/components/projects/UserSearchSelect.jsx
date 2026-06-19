import { Plus, Search } from "lucide-react";
import { useEffect, useState } from "react";

import api from "../../api/client.js";
import StatusBadge from "../StatusBadge.jsx";

export default function UserSearchSelect({ onAssign }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    const term = query.trim();
    if (!term) {
      setResults([]);
      setSearched(false);
      return undefined;
    }

    const timeout = window.setTimeout(async () => {
      setLoading(true);
      setSearched(true);
      try {
        const response = await api.get("/users/search", { params: { query: term } });
        setResults(response.data || []);
      } catch {
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => window.clearTimeout(timeout);
  }, [query]);

  function handleAssign(user) {
    onAssign(user).then((assigned) => {
      if (assigned) {
        setQuery("");
        setResults([]);
        setSearched(false);
      }
    });
  }

  return (
    <div className="user-search">
      <label>
        Search users
        <div className="input-with-icon">
          <Search size={16} aria-hidden="true" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Name, email, or role"
            autoComplete="off"
          />
        </div>
      </label>
      {loading && <div className="muted-list-state" role="status">Searching users...</div>}
      {!loading && searched && results.length === 0 && <div className="muted-list-state">No users found</div>}
      {!loading && results.length > 0 && (
        <div className="result-list" role="listbox" aria-label="User search results">
          {results.map((user) => (
            <div className="result-row" key={user.id} role="option" aria-selected="false">
              <div>
                <strong>{user.name}</strong>
                <span>{user.email}</span>
                <StatusBadge value={user.role} />
              </div>
              <button className="primary-button compact-button" onClick={() => handleAssign(user)} type="button">
                <Plus size={16} aria-hidden="true" />
                Assign
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
