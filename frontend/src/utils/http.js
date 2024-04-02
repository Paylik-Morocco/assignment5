import router from '@/router';
import axios from 'axios'
const refreshToken = () => {
    return new Promise(async (resolve, reject) => {
        try{
            const {status, data} = await public_api.post('/token/refresh/', {
                "refresh": localStorage.getItem('refresh')
            });
            localStorage.setItem('access', data.access);
            resolve(data.access)
        }catch(e){
            reject(e);
        }
    })
}


const public_api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
})

api.interceptors.request.use(config => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('access')}`
    return config;
})

api.interceptors.response.use(res=>res, async (error)=>{
    console.log(error)
    if(error.response.status === 401){
        try{
            const access = refreshToken();
            api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
            return axios(error.config);
        }catch(e){
            api.defaults.headers.common['Authorization'] = ``;
            return error;
        }
    }
    return error;
})

export {public_api as public_api}
export {api as api}