const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

async function apiRequest(path, options = {}) {
  const token = localStorage.getItem("travel_access_token");
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;

  let response = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (response.status === 401 && localStorage.getItem("travel_refresh_token")) {
    const refreshResponse = await fetch(`${API_URL}/auth/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: localStorage.getItem("travel_refresh_token") }),
    });
    if (refreshResponse.ok) {
      const refreshData = await refreshResponse.json();
      localStorage.setItem("travel_access_token", refreshData.access);
      headers.Authorization = `Bearer ${refreshData.access}`;
      response = await fetch(`${API_URL}${path}`, { ...options, headers });
    } else {
      localStorage.removeItem("travel_access_token");
      localStorage.removeItem("travel_refresh_token");
    }
  }

  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (!response.ok) {
    const message = data?.detail || Object.values(data || {})?.flat?.()?.[0] || "Something went wrong.";
    throw new Error(message);
  }
  return data;
}

export const api = {
  listDestinations: (params = "") => apiRequest(`/destinations/${params ? `?${params}` : ""}`),
  getDestination: (id) => apiRequest(`/destinations/${id}/`),
  register: (payload) => apiRequest("/auth/register/", { method: "POST", body: JSON.stringify(payload) }),
  login: (payload) => apiRequest("/auth/token/", { method: "POST", body: JSON.stringify(payload) }),
  me: () => apiRequest("/auth/me/"),
  favorites: () => apiRequest("/favorites/"),
  addFavorite: (destinationId) => apiRequest("/favorites/", { method: "POST", body: JSON.stringify({ destination_id: destinationId }) }),
  removeFavorite: (destinationId) => apiRequest(`/favorites/${destinationId}/`, { method: "DELETE" }),
};
