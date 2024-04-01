import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import router from '@/router';
export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  if(localStorage.getItem('refresh') && localStorage.getItem('refresh').trim() != ''){
    const decoded_access = jwtDecode(localStorage.getItem('refresh'));

    user.value = {
      user_id: decoded_access.user_id,
      username: decoded_access.username,
      email: decoded_access.email,
      is_staff: decoded_access.is_staff,
    }
  }
  const login = ({ email, password }) => {
    return new Promise(async (resolve, reject) => {
      const { status, data } = await axios.post('/token/', {
        email: email,
        password: password
      })
      if (status === 200) {
        localStorage.setItem('refresh', data.refresh);
        axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
        const decoded_access = jwtDecode(data.access);
        user.value = {
          user_id: decoded_access.user_id,
          username: decoded_access.username,
          email: decoded_access.email,
          is_staff: decoded_access.is_staff,
        }
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

  const logout = () => {
    localStorage.setItem('refresh', '');
    axios.defaults.headers.common['Authorization'] = '';
    user.value = null;
  }
  return { user, login, logout, register }
})
