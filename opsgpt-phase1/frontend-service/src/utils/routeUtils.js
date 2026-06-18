export function isActiveNavItem(key, pathname) {
  const path = pathname.replace(/\/+$/, "") || "/";

  const matchers = {
    projects: /^\/projects$/,
    dashboard: /^\/projects\/[^/]+\/dashboard$/,
    incidents: /^\/projects\/[^/]+\/incidents(?:\/[^/]+)?$/,
    knowledgeBase: /^\/knowledge-base$/,
    profile: /^\/profile$/,
    adminProjects: /^\/admin\/projects(?:\/[^/]+\/sources)?$/,
  };

  return Boolean(matchers[key]?.test(path));
}
