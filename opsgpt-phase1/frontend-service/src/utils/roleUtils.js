import { USER_ROLES } from "./constants";

export function canEditIncident(user) {
  return [USER_ROLES.SENIOR_ENGINEER, USER_ROLES.ADMIN].includes(user?.role);
}

export function canResolveIncident(user) {
  return canEditIncident(user);
}

export function isReadOnlyUser(user) {
  return user?.role === USER_ROLES.JUNIOR_ENGINEER;
}
