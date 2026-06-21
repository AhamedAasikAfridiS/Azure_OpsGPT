import { InteractionRequiredAuthError, PublicClientApplication } from "@azure/msal-browser";

import { authProvider, isEntraConfigured, loginRequest, msalConfig } from "./msalConfig.js";

export const msalInstance =
  authProvider === "entra" && isEntraConfigured ? new PublicClientApplication(msalConfig) : null;

let initializationPromise = null;

export async function initializeMicrosoftAuth() {
  if (!msalInstance) {
    return null;
  }

  if (!initializationPromise) {
    initializationPromise = msalInstance.initialize().then(async () => {
      const response = await msalInstance.handleRedirectPromise();
      const account = response?.account || msalInstance.getActiveAccount() || msalInstance.getAllAccounts()[0];
      if (account) {
        msalInstance.setActiveAccount(account);
      }
      return account || null;
    });
  }
  return initializationPromise;
}

export async function getMicrosoftAccessToken() {
  if (!msalInstance) {
    return null;
  }

  const account = msalInstance.getActiveAccount() || msalInstance.getAllAccounts()[0];
  if (!account) {
    return null;
  }

  try {
    const response = await msalInstance.acquireTokenSilent({ ...loginRequest, account });
    return response.accessToken;
  } catch (error) {
    if (error instanceof InteractionRequiredAuthError) {
      await msalInstance.acquireTokenRedirect({ ...loginRequest, account });
      return null;
    }
    throw error;
  }
}

export async function signInWithMicrosoft() {
  if (!msalInstance) {
    throw new Error("Microsoft Entra ID configuration is incomplete.");
  }
  await msalInstance.loginRedirect(loginRequest);
}

export async function signOutFromMicrosoft() {
  if (!msalInstance) {
    return;
  }
  await msalInstance.logoutRedirect({
    account: msalInstance.getActiveAccount() || undefined,
    postLogoutRedirectUri: msalConfig.auth.postLogoutRedirectUri
  });
}
