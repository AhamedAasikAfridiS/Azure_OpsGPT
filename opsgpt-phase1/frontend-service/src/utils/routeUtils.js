export function isActiveNavItem(key, pathname) {
  const path =
    pathname.length > 1 ? pathname.replace(/\/+$/, "") : pathname;

  const matchers = {
    projects: /^\/projects$/,
    dashboard: /^(\/dashboard|\/projects\/[^/]+\/dashboard)$/,
    incidents:
      /^(\/incidents(?:\/[^/]+)?|\/projects\/[^/]+\/incidents(?:\/[^/]+)?)$/,
    knowledgeBase: /^\/knowledge-base$/,
    profile: /^\/profile$/,
    adminProjects: /^\/admin\/projects(?:\/[^/]+\/sources)?$/,
  };

  return matchers[key]?.test(path) || false;
}
