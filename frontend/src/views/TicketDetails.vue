<script setup>
import { ref } from 'vue';
import { FwbInput, FwbSelect, FwbButton, FwbBadge, FwbTextarea } from 'flowbite-vue';
import { useTicketsStore } from '../stores/ticketsStore'
import { useAuthStore } from '@/stores/authStore';
import axios from 'axios';
import { useRoute } from 'vue-router';
import moment from 'moment';
const ticket = ref(null);

const route = useRoute();
axios.get(`tickets/${route.params.id}/`).then(res => {
    ticket.value = res.data
})

const auth = useAuthStore()

const newReply = ref('');

const sumbitReply = () => {
    axios.post(`/tickets/${ticket.value.id}/reply/`, {
        text: newReply.value
    }).then(res => {
        ticket.value = {
            ...ticket.value,
            reply: res.data
        }
    }).catch(e => {
        console.error(e);
    })
}

const closeTicket = () => {
    axios.put(`/tickets/${ticket.value.id}/update/`, {
        status: 'closed'
    }).then(res => {
        ticket.value = {
            ...ticket.value,
            status: 'closed'
        }
    }).catch(e => {
        console.error(e);
    })
}
const resolveTicket = () => {
    axios.put(`/tickets/${ticket.value.id}/update/`, {
        status: 'resolved'
    }).then(res => {
        ticket.value = {
            ...ticket.value,
            status: 'resolved'
        }
    }).catch(e => {
        console.error(e);
    })
}
</script>

<template>
    <div class="py-12 px-0 md:px-12">
        <div class="bg-white p-8 rounded-xl shadow-md">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
                <div class="">
                    <div class="flex items-center mb-3">
                        <div class="w-6 h-6 rounded-full mr-3" :class="{
                            'bg-green-400': ticket?.status == 'resolved',
                            'bg-blue-400': ticket?.status == 'open',
                            'bg-gray-400': ticket?.status == 'closed',
                        }"></div>
                        <span class="text-xl font-semibold block">Ticket #{{ ticket?.id }}
                            <fwb-badge class="inline text-white" :class="{
                            'bg-green-400': ticket?.status == 'resolved',
                            'bg-blue-400': ticket?.status == 'open',
                            'bg-gray-400': ticket?.status == 'closed'
                        }">{{ ticket?.status }}</fwb-badge>
                        </span>
                    </div>
                    <span class="text-sm text-slate-600 block">{{ moment(ticket?.created_at).format('ddd DD MMM YYYY hh:mm A')}}</span>
                </div>
                <div v-if="ticket?.status == 'open'" class="mt-4 md:mt-0">
                    <span @click="closeTicket" class="block underline cursor-pointer">change status to Closed</span>
                    <span @click="resolveTicket" class="block underline mt-4 cursor-pointer">change status to Resolved</span>
                </div>
            </div>
            <hr class="my-4">
            <span class="font-semibold text-xl">{{ ticket?.title }}</span>
            <p>
                {{ ticket?.description }}
            </p>

            <hr class="my-4">
            <span class="font-semibold">reply:</span>
            <div v-if="ticket?.reply">
                <p>{{ ticket?.reply?.text }}</p>
                <span class="text-xs text-slate-600">{{ moment(ticket?.reply?.created_at).format('ddd DD MMM YYYY hh:mm A') }}</span>
            </div>
            <div v-if="!ticket?.reply && auth.user?.is_staff">
                <fwb-textarea v-model="newReply" label="new reply" />
                <fwb-button @click="sumbitReply">send reply</fwb-button>
            </div>
        </div>
    </div>
</template>