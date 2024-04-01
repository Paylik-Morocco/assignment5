import axios from 'axios';
import router from '@/router';
axios.defaults.baseURL = 'http://localhost:8000/api/'


axios.interceptors.response.use(res=>res, async error =>{
    if(error.response.status === 401){
        const {status, data} = await axios.post('/token/refresh/', {
            "refresh": localStorage.getItem('refresh')
        });

        if (status === 200){
            axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
            return axios(error.config);
        }
        router.push('/login')
    }

    return error;
})