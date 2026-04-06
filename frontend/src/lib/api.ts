const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface FetchOptions extends RequestInit {
  token?: string;
}

async function fetchApi<T>(path: string, options: FetchOptions = {}): Promise<T> {
  const { token, headers: customHeaders, ...rest } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((customHeaders as Record<string, string>) || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_URL}${path}`, { headers, ...rest });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Request failed");
  }

  if (res.status === 204) return {} as T;
  return res.json();
}

// Auth
export const register = (email: string, password: string) =>
  fetchApi<{ access_token: string }>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

export const login = (email: string, password: string) =>
  fetchApi<{ access_token: string }>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

export const getMe = (token: string) =>
  fetchApi<{ id: string; email: string }>("/api/auth/me", { token });

// Accounts
export const listAccounts = (token: string) =>
  fetchApi<Account[]>("/api/accounts", { token });

export const createAccount = (token: string, data: { instagram_username: string; display_name?: string }) =>
  fetchApi<Account>("/api/accounts", { token, method: "POST", body: JSON.stringify(data) });

export const getAccount = (token: string, id: string) =>
  fetchApi<Account>(`/api/accounts/${id}`, { token });

export const deleteAccount = (token: string, id: string) =>
  fetchApi(`/api/accounts/${id}`, { token, method: "DELETE" });

// Snapshots
export const triggerSnapshot = (token: string, accountId: string) =>
  fetchApi<Snapshot>(`/api/accounts/${accountId}/snapshots`, { token, method: "POST" });

export const listSnapshots = (token: string, accountId: string) =>
  fetchApi<Snapshot[]>(`/api/accounts/${accountId}/snapshots`, { token });

// Changes
export const listChanges = (token: string, accountId: string) =>
  fetchApi<ChangeEvent[]>(`/api/accounts/${accountId}/changes`, { token });

export const getChangesSummary = (token: string) =>
  fetchApi<ChangeSummary>("/api/changes/summary", { token });

// Notifications
export const listNotifications = (token: string) =>
  fetchApi<Notification[]>("/api/notifications", { token });

export const markNotificationRead = (token: string, id: string) =>
  fetchApi(`/api/notifications/${id}/read`, { token, method: "PATCH" });

export const markAllNotificationsRead = (token: string) =>
  fetchApi("/api/notifications/read-all", { token, method: "POST" });

// Types
export interface Account {
  id: string;
  instagram_username: string;
  display_name: string | null;
  is_active: boolean;
  check_interval_minutes: number;
  last_checked_at: string | null;
  created_at: string;
}

export interface Snapshot {
  id: string;
  tracked_account_id: string;
  follower_count: number;
  following_count: number;
  status: string;
  error_message: string | null;
  snapshot_at: string;
}

export interface ChangeEvent {
  id: string;
  tracked_account_id: string;
  change_type: "new_follower" | "lost_follower" | "new_following" | "lost_following";
  instagram_username: string;
  detected_at: string;
}

export interface ChangeSummary {
  new_followers: number;
  lost_followers: number;
  new_following: number;
  lost_following: number;
  total_changes: number;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
  change_event_id: string | null;
}
