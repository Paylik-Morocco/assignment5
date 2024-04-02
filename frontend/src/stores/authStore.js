import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { api } from '@/utils/http';
export const useAuthStore = defineStore('auth', () => {
  const user = ref(undefined);
  const login = ({ email, password }) => {
    return new Promise(async (resolve, reject) => {
      const { status, data } = await api.post('/token/', {
        email: email,
        password: password
      })
      if (status === 200) {
        localStorage.setItem('refresh', data.refresh);
        localStorage.setItem('access', data.access)
        resolve(data);
      } else {
        reject(data);
      }
    })
  }
  const register = ({ username, email, password }) => {
    return new Promise(async (resolve, reject) => {
      const { status, data, response } = await api.post('/signup/', {
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
      const { status, data, response } = await api.get('/profile/')
      if (status === 200) {
        user.value = data;
        resolve(data);
      } else {
        user.value = null;
        reject(response.data);
      }
    })
  }
  getProfile();
  const logout = () => {
    localStorage.setItem('refresh', '');
    localStorage.setItem('access', '');
    api.defaults.headers.common['Authorization'] = '';
    user.value = null;
  }

  
  return { user, login, logout, register, getProfile }
})
