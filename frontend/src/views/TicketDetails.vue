<script setup>
import { computed, ref } from 'vue';
import { FwbInput, FwbSelect, FwbButton, FwbBadge, FwbTextarea } from 'flowbite-vue';
import { useTicketsStore } from '../stores/ticketsStore'
import { useAuthStore } from '@/stores/authStore';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import moment from 'moment';
import ArrowLeft from 'vue-material-design-icons/ArrowLeft.vue';
import { api } from '@/utils/http';

const ticket = ref(null);

const route = useRoute();
const router = useRouter();
api.get(`tickets/${route.params.id}/`).then(res => {
    ticket.value = res.data
})

const auth = useAuthStore()

const newReply = ref('');

const sumbitReply = () => {
    api.post(`/tickets/${ticket.value.id}/reply/`, {
        text: newReply.value
    }).then(res => {
        ticket.value = {
            ...ticket.value,
            replies: [
                ...ticket.value.replies,
                res.data
            ]
        }
    }).catch(e => {
        console.error(e);
    })
}

const closeTicket = () => {
    api.put(`/tickets/${ticket.value.id}/update/`, {
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
    api.put(`/tickets/${ticket.value.id}/update/`, {
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

// returns if the current admin replies to this ticket.
const currentUserReplied = ()=>{
    return ticket.value?.replies?.some(r => r.created_by == auth.user.user_id)
}
</script>

<template>
    <div class="py-12 px-0 md:px-12">
        <div class="bg-white p-8 rounded-xl shadow-md">
            <div class="">
                <div @click="router.back()" class="flex justify-start items-center text-lg cursor-pointer hover:text-slate-500">
                    <span>
                        <ArrowLeft />
                    </span>
                    <span>Back</span>
                </div>
            </div>
            <hr class="my-4">
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
            </div>
            <hr class="my-4">
            <span class="font-semibold text-xl">{{ ticket?.title }}</span>
            <p>
                {{ ticket?.description }}
            </p>

            <hr class="my-4">
            <span class="font-semibold mb-6 block">Replies:</span>
            <div v-if="ticket?.replies" v-for="reply in ticket?.replies">
                <p>{{ reply?.text }}</p>
                <span class="text-xs text-slate-600">{{ moment(reply?.created_at).format('ddd DD MMM YYYY hh:mm A') }}</span>
            </div>
            <div v-if="!currentUserReplied() && auth.user?.is_staff" class="mt-12">
                <fwb-textarea v-model="newReply" label="new reply" />
                <fwb-button @click="sumbitReply">send reply</fwb-button>
            </div>
            <hr class="my-4">
            <span v-if="ticket?.status == 'open' && auth.user?.is_staff" class="font-semibold mb-6 block">Update ticket:</span>
            <div v-if="ticket?.status == 'open' && auth.user?.is_staff" class="mt-4">
                <fwb-button @click="closeTicket" class="mr-4" color="alternative">Closed</fwb-button>
                <fwb-button @click="resolveTicket" color="green">Resolved</fwb-button>
            </div>
        </div>
    </div>
</template>