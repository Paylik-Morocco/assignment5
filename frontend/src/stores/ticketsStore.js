import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';
export const useTicketsStore = defineStore('tickets', () => {
  const tickets = ref([]);

  const fetchTickets = () =>{
    return new Promise(async (resolve, reject) => {
        try{
            const {data} = await axios.get('tickets/');
            tickets.value = data;
            resolve(data);
        }catch(e){
            reject(e);
        }
    })
  }
  return { tickets, fetchTickets }
})
