import axios from "axios";
import AuthService from "../services/AuthService";

export const API_URL = 'http://localhost:6969'

const api = axios.create({
  withCredentials: true,
  baseURL: API_URL,
})

api.interceptors.request.use((config) => {
  const access_token = localStorage.getItem("access");

  if (access_token) {
    config.headers.Authorization = `Bearer ${access_token}`;
  }

  return config;
})

api.interceptors.request.use((config) => {
  return config;
}, async (error) => {
  console.log('handled 401');
  const originalRequest = error.config;
  if (error.response && error.response.status === 401) {
    const refresh = localStorage.getItem("refresh");

    if (!refresh) {
      console.log('ny ya xz cho delat')
    }

    try {
      const response = await AuthService.refresh(refresh)
      localStorage.setItem('access', response.data.access)
      localStorage.setItem('refresh', response.data.refresh)
    } catch (e) {
      console.log(e)
    }
    return api.request(originalRequest);
  }
})

export default api;
