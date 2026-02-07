import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

export const classAPI = {
  create: (data) => api.post('/classes', data),
  getAll: (search = '') => api.get('/classes', { params: { search } }),
  getOne: (id) => api.get(`/classes/${id}`),
  update: (id, data) => api.put(`/classes/${id}`, data),
  delete: (id) => api.delete(`/classes/${id}`),
};

export const studentAPI = {
  create: (classId, data) => api.post(`/students/class/${classId}`, data),
  getAll: (classId) => api.get(`/students/class/${classId}`),
  update: (id, data) => api.put(`/students/${id}`, data),
  delete: (id) => api.delete(`/students/${id}`),
};

export const attendanceAPI = {
  mark: (classId, data) => api.post(`/attendance/class/${classId}/mark`, data),
  getHistory: (classId) => api.get(`/attendance/class/${classId}/history`),
  update: (id, data) => api.put(`/attendance/${id}`, data),
  delete: (id) => api.delete(`/attendance/${id}`),
};

export default api;