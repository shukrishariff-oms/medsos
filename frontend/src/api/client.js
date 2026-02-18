import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8001',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Check for 401 Unauthorized
        if (error.response && error.response.status === 401) {
            // Redirect to connect page if not already there, 
            // but avoid infinite loops if the connect page itself makes a 401 call (e.g. check status)
            if (window.location.pathname !== '/connect') {
                window.location.href = '/connect';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
