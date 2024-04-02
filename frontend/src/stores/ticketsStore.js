import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';
import moment from 'moment';
import { api } from '@/utils/http';
export const useTicketsStore = defineStore('tickets', () => {
  const tickets = ref([]);
  const ticketsCount = ref({
    all: 0,
    open: 0,
    resolved: 0,
    closed: 0
  })
  const fetchTickets = ({ status, start_datetime, end_datetime, search }) => {
    return new Promise(async (resolve, reject) => {
      try {
        const params = {}
        if (status) {
          params.status = status;
        }
        if (search && search != '') {
          params.search = search
        }
        if (start_datetime != null) {
          params.start_datetime = moment(start_datetime).toISOString();
        }
        if (end_datetime != null) {
          params.end_datetime = moment(end_datetime).toISOString();
        }
        const paramsobj = new URLSearchParams(params)
        const { data } = await axios.get('tickets/?' + paramsobj.toString(), {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access')}`
          }
        });
        tickets.value = data;
        resolve(data);
      } catch (e) {
        reject(e);
      }
    })
  }
  const fetchTicketsOverview = () => {
    return new Promise(async (resolve, reject) => {
      try {
        const { data } = await api.get('tickets/overview/');
        ticketsCount.value = data;
        resolve(data);
      } catch (e) {
        reject(e);
      }
    })
  }
  return { tickets, ticketsCount, fetchTickets, fetchTicketsOverview }
})
