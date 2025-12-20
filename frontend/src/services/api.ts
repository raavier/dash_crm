import axios from 'axios';

// Em produção no Databricks Apps, o backend está no mesmo host
// Em desenvolvimento local, usa localhost:8001
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || (
    import.meta.env.PROD ? '' : 'http://localhost:8001'
  ),
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30s timeout (queries podem demorar no primeiro request)
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;
