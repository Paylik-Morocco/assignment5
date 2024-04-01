<script setup>
import { ref } from 'vue';
import Ticket from '../components/Ticket.vue'
import { FwbInput, FwbSelect, FwbButton, FwbModal, FwbTextarea } from 'flowbite-vue';
import { useTicketsStore } from '../stores/ticketsStore'
import { useAuthStore } from '@/stores/authStore';
import axios from 'axios';
const statuses = [
    { value: 'all', name: 'no status filter' },
    { value: 'open', name: 'Open tickets' },
    { value: 'closed', name: 'Closed tickets' },
    { value: 'resolved', name: 'Resolved tickets' },
]
const dateOptions = [
    { value: 'today', name: 'Today' },
    { value: 'week', name: 'This week' },
    { value: 'month', name: 'This month' },
    { value: 'all', name: 'All time' },
]

const statusFilter = ref('all');
const datesFilter = ref('week');

const isShowModal = ref(false);
const openModal = () => {
    isShowModal.value = true;
}
const closeModal = () => {
    isShowModal.value = false;
}
const newTicket = ref({
    title: '',
    description: ''
})
const newTickerErrors = ref({});
const auth = useAuthStore();
const ticketsStore = useTicketsStore();
ticketsStore.fetchTickets();

const submitTicket = async () => {
    const { status, data, response } = await axios.post('tickets/create/', {
        title: newTicket.value.title,
        description: newTicket.value.description,
    })
    if(status === 201){
        console.log(data);
        isShowModal.value = false;
    }else{
        newTickerErrors.value = response.data;
    }
}

</script>

<template>
    <div class="py-12 px-0 md:px-12">
        <div v-if="auth.user?.is_staff" class="mb-8 grid grid-cols-1 xs:grid-cols-2 lg:grid-cols-4 gap-6 ">
            <div
                class="shadow-sm bg-amber-200 px-6 py-2 lg:py-6 rounded-xl flex flex-row lg:flex-row items-center justify-between">
                <span class="block font-semibold text-md">Total Tickets</span>
                <span class="block font-semibold lg:font-bold text-xl ml-4">03</span>
            </div>
            <div
                class="shadow-sm bg-blue-400 px-6 py-2 lg:py-6 rounded-xl flex flex-row lg:flex-row items-center justify-between">
                <span class="block font-semibold text-md">Open Tickets</span>
                <span class="block font-semibold lg:font-bold text-xl ml-4">03</span>
            </div>
            <div
                class="shadow-sm bg-slate-300 px-6 py-2 lg:py-6 rounded-xl flex flex-row lg:flex-row items-center justify-between">
                <span class="block font-semibold text-md">Closed Tickets</span>
                <span class="block font-semibold lg:font-bold text-xl ml-4">03</span>
            </div>
            <div
                class="shadow-sm bg-emerald-400 px-6 py-2 lg:py-6 rounded-xl flex flex-row lg:flex-row items-center justify-between">
                <span class="block font-semibold text-md">Resolved Tickets</span>
                <span class="block font-semibold lg:font-bold text-xl ml-4">03</span>
            </div>
        </div>
        <div class="bg-white p-8 rounded-xl shadow-md">
            <div class="flex flex-col lg:flex-row justify-between">
                <fwb-input label="Search" placeholder="enter your search query">
                    <template #prefix>
                        <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none"
                            stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round"
                                stroke-linejoin="round" stroke-width="2" />
                        </svg>
                    </template>
                </fwb-input>
                <div class="flex flex-col md:flex-row justify-between items-stretch md:items-end mt-4 lg:mt-0">
                    <div class="flex flex-col md:flex-row">
                        <fwb-select class="mr-0 md:mr-4" :model-value="statusFilter" :options="statuses"
                            label="Status" />
                        <fwb-select class="mt-4 md:mt-0" :model-value="datesFilter" :options="dateOptions"
                            label="Date" />
                    </div>
                    <fwb-button @click="openModal" v-if="!auth.user?.is_staff" class="md:ml-4 py-2.5 text-sm mt-4">New
                        Ticket</fwb-button>
                </div>
            </div>
            <hr class="my-6">
            <ul>
                <li v-for="ticket in ticketsStore.tickets" class="mb-6">
                    <Ticket :ticket="ticket" />
                </li>
            </ul>
            <span class="sm:text-2xl text-center block my-12" v-if="ticketsStore.tickets.length == 0">No tickets to show...</span>
        </div>
    </div>
    <fwb-modal v-if="isShowModal" @close="closeModal">
        <template #header>
            <div class="flex items-center text-lg">
                New Ticket
            </div>
        </template>
        <template #body>
            <form>
                <fwb-input placeholder="Give a title to your ticket..." label="Title"
                    v-model="newTicket.title" />
                <span v-for="err in newTickerErrors.title" class="text-red-500 text-sm block mb-6">{{ err }}</span>
                <fwb-textarea :validation-status="newTickerErrors.description?'error':''" label="Description" placeholder="Describe your new ticket..."
                    v-model="newTicket.description" />
                <span v-for="err in newTickerErrors.description" class="text-red-500 text-sm block">{{ err }}</span>

            </form>
        </template>
        <template #footer>
            <div class="flex justify-end">
                <fwb-button @click="closeModal" color="alternative">
                    Close
                </fwb-button>
                <fwb-button @click="submitTicket" color="green" class="ml-3">
                    Create Ticket
                </fwb-button>
            </div>
        </template>
    </fwb-modal>
</template>