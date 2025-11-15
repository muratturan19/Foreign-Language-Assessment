import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const API_TOKEN = import.meta.env.VITE_APP_SECRET_TOKEN;

if (!API_TOKEN) {
  throw new Error(
    "VITE_APP_SECRET_TOKEN is not set. Please create a .env file in the frontend directory " +
    "with VITE_APP_SECRET_TOKEN set to match the backend's APP_SECRET_TOKEN. " +
    "See frontend/.env.example for reference."
  );
}

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${API_TOKEN}`
  }
});

export function setAuthToken(token: string) {
  api.defaults.headers.common.Authorization = `Bearer ${token}`;
}
