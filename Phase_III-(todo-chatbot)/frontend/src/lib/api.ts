import axios from 'axios';

// Create Axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000, // 10 seconds timeout
  withCredentials: true, // Include cookies in requests
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-token'); // Or from cookies if using httpOnly
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling 401 errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth token and redirect to signin
      localStorage.removeItem('auth-token');
      // Note: We can't use router here, so we'll handle redirect in components
      console.warn('Authentication token expired. Redirecting to sign in.');
    }
    return Promise.reject(error);
  }
);

export default api;