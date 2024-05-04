import axios from "axios";
import AuthService from "../services/AuthService";

export const API_URL = 'http://localhost:6969'

const api = axios.create({
  withCredentials: true,
  baseURL: API_URL,
})

export const auth_api = axios.create({
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

api.interceptors.response.use((config) => {
  return config;
}, async (error) => {
  if (error.response.status === 401) {
    const refresh = localStorage.getItem("refresh");
    const originalRequest = error.config;

    if (!refresh) {
      console.log('ny ya xz cho delat')
      throw error
    }

    try {
      const response = await AuthService.refresh(refresh)
      console.log(`refresh: ${response}`)
      localStorage.setItem('access', response.data.access)

      return api.request(originalRequest);
    } catch (e) {
      console.log(e)
      throw error;
    }
  }
  return Promise.reject(error);
});

export default api;
