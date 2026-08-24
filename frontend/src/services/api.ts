import axios from 'axios';
import { Rental, RentalFormData } from '../types/rental';

const apiClient = axios.create({
  baseURL: '/api'
});

// Attach Authorization header if token exists
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  // Auth
  register: async (payload: { name: string; email: string; password: string }): Promise<any> => {
    const res = await apiClient.post('/auth/register', payload);
    return res.data;
  },

  login: async (payload: { email: string; password: string }): Promise<any> => {
    const res = await apiClient.post('/auth/login', payload);
    return res.data;
  },

  getMe: async (): Promise<any> => {
    const res = await apiClient.get('/auth/me');
    return res.data;
  },

  // Rentals
  getRentals: async (params?: { status?: string; city?: string; wifiType?: string; search?: string }): Promise<Rental[]> => {
    const res = await apiClient.get<Rental[]>('/rentals', { params });
    return res.data;
  },

  createRental: async (data: RentalFormData): Promise<Rental> => {
    const res = await apiClient.post<Rental>('/rentals', data);
    return res.data;
  },

  updateRental: async (id: string, data: Partial<RentalFormData>): Promise<Rental> => {
    const res = await apiClient.put<Rental>(`/rentals/${id}`, data);
    return res.data;
  },

  deleteRental: async (id: string): Promise<any> => {
    const res = await apiClient.delete(`/rentals/${id}`);
    return res.data;
  },

  seedData: async (): Promise<any> => {
    const res = await apiClient.post('/rentals/seed');
    return res.data;
  }
};
