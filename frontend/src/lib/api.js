import axios from 'axios';

// In Docker/Production, we want to simply use the relative path '/api'
// because the same server (FastAPI) is serving both frontend and backend.
// Only use localhost in DEV mode when they are separate.
const BASE_URL = import.meta.env.PROD ? '/api' : (import.meta.env.VITE_API_BASE || 'http://localhost:8001/api');

const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        return Promise.reject(error);
    }
);

export const getAuthStatus = async () => {
    const response = await api.get('/auth/threads/status');
    return response.data;
};

export const listPosts = async (limit = 10) => {
    const response = await api.get(`/threads/posts?limit=${limit}`);
    return response.data;
};

export const createPost = async (text) => {
    const response = await api.post('/threads/post', { text });
    return response.data;
};

export const deletePost = async (mediaId) => {
    const response = await api.delete(`/threads/post/${mediaId}`);
    return response.data;
};

export default api;
