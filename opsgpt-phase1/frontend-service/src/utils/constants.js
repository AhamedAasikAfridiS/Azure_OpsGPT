export const TOKEN_STORAGE_KEY = "opsgpt_access_token";
export const USER_STORAGE_KEY = "opsgpt_user";

export const USER_ROLES = {
  JUNIOR_ENGINEER: "junior_engineer",
  SENIOR_ENGINEER: "senior_engineer",
  ADMIN: "admin",
};

export const INCIDENT_STATUSES = [
  { value: "open", label: "Open" },
  { value: "in_progress", label: "In Progress" },
  { value: "resolved", label: "Resolved" },
];

export const INCIDENT_SEVERITIES = [
  { value: "critical", label: "Critical" },
  { value: "warning", label: "Warning" },
  { value: "informational", label: "Informational" },
];
