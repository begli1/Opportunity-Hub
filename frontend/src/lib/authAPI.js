import api from '@/apiClient'


export async function register(payload){
    const response = await api.post('/register',payload);

    return response.data;
}


export async function login(payload){
    const response = await api.post('/auth/login',payload);

    return response.data;
}