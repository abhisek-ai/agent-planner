import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const projectAPI = {
  createProject: async (description: string) => {
    const response = await api.post('/api/v1/projects/', { description });
    return response.data;
  },
  
  getProject: async (id: string) => {
    const response = await api.get(`/api/v1/projects/${id}`);
    return response.data;
  },
  
  getAllProjects: async () => {
    const response = await api.get('/api/v1/projects/');
    return response.data;
  },
};

export default api;