import axios from 'axios'
import router from './router'
import { useAuth } from './lib/authStore'

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 20000,
})

// Request interceptor: Add token to all requests
AxiosInstance.interceptors.request.use(
    (config) => {
        const { token } = useAuth()
        if (token.value) {
            config.headers.Authorization = `Bearer ${token.value}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor: Handle 401 errors (token expired)
AxiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid - clear token and redirect to login
            const { clearToken } = useAuth()
            clearToken()
            
            // Only redirect if not already on login/signup page
            if (router.currentRoute.value.path !== '/login' && 
                router.currentRoute.value.path !== '/signup') {
                router.push('/login')
            }
        }
        return Promise.reject(error)
    }
)

export default AxiosInstance