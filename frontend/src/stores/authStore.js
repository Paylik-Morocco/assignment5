import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';
export const useAuthStore = defineStore('auth', () => {
  const user = ref(undefined);
  const login = ({ email, password }) => {
    return new Promise(async (resolve, reject) => {
      const { status, data } = await axios.post('/token/', {
        email: email,
        password: password
      })
      if (status === 200) {
        localStorage.setItem('refresh', data.refresh);
        axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
        localStorage.setItem('access', data.access)
        resolve(data);
      } else {
        reject(data);
      }
    })
  }
  const register = ({ username, email, password }) => {
    return new Promise(async (resolve, reject) => {
      const { status, data, response } = await axios.post('/signup/', {
        username: username,
        email: email,
        password: password
      })
      if (status === 201) {
        resolve(data);
      } else {
        reject(response.data);
      }
    })
  }

  const getProfile = () => {
    return new Promise(async (resolve, reject) => {
      const { status, data, response } = await axios.get('/profile/')
      if (status === 200) {
        user.value = data;
        resolve(data);
      } else {
        user.value = null;
        reject(response.data);
      }
    })
  }

  const logout = () => {
    localStorage.setItem('refresh', '');
    axios.defaults.headers.common['Authorization'] = '';
    user.value = null;
  }

  async function initialize(){
    try{
      await getProfile();
    }catch(e){
      console.log('unauthenticated')
    }
  }

  initialize();
  return { user, login, logout, register, getProfile }
})
