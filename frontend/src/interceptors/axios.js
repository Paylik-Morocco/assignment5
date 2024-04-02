import axios from 'axios';
import router from '@/router';
axios.defaults.baseURL = import.meta.env.VITE_API_URL


axios.interceptors.response.use(res=>res, async error =>{
    if(error.response.status === 401){
        const {status, data} = await axios.post('/token/refresh/', {
            "refresh": localStorage.getItem('refresh')
        });

        if (status === 200){
            axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
            localStorage.setItem('access', data.access)
            return axios(error.config);
        }
        axios.defaults.headers.common['Authorization'] = ``;
        localStorage.setItem('access', '')

        router.push('/login')
    }

    return error;
})