const configuredProvider = (import.meta.env.VITE_AUTH_PROVIDER || "local").toLowerCase();
const tenantId = import.meta.env.VITE_AZURE_TENANT_ID || "";
const clientId = import.meta.env.VITE_AZURE_CLIENT_ID || "";
const apiScope = import.meta.env.VITE_AZURE_API_SCOPE || "";

export const authProvider = configuredProvider === "entra" ? "entra" : "local";
export const isEntraConfigured = Boolean(tenantId && clientId && apiScope);

export const msalConfig = {
  auth: {
    clientId,
    authority: tenantId ? `https://login.microsoftonline.com/${tenantId}` : undefined,
    redirectUri: import.meta.env.VITE_AZURE_REDIRECT_URI || window.location.origin,
    postLogoutRedirectUri: import.meta.env.VITE_AZURE_POST_LOGOUT_REDIRECT_URI || window.location.origin
  },
  cache: {
    cacheLocation: "sessionStorage"
  }
};

export const loginRequest = {
  scopes: apiScope ? [apiScope] : []
};
