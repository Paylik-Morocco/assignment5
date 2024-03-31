<script setup>
import { RouterLink } from 'vue-router';
import moment from 'moment';
const {ticket} = defineProps({
  ticket: Object,
})
</script>

<template>
    <div class="border rounded-md p-7 shadow-md">
        <div class="flex items-center mb-3">
            <div  class="w-6 h-6 rounded-full mr-3" :class="{
                'bg-green-400': ticket.status=='resolved',
                'bg-blue-400': ticket.status=='open',
                'bg-gray-400': ticket.status=='closed',
            }"></div>
            <span class="text-xl font-semibold block">Ticket #{{ ticket.id }} ({{ ticket.status }})</span>
        </div>
        <span class="text-md ,b-2 font-semibold block">{{ ticket.title }}</span>
        <div class="max-h-[70px] min-h-[50px] overflow-hidden fade mb-6">
            <p>{{ ticket.description }}</p>
        </div>
        <hr>
        <div class="flex justify-between mt-6">
            <div class="flex flex-col text-sm text-gray-500">
                <span>created at: {{ moment(ticket.created_at).format('ddd DD MMM YYYY hh:mm A') }}</span>
                <span>last updated at: {{ moment(ticket.updated_at).format('ddd DD MMM YYYY hh:mm A') }}</span>
            </div>
            <RouterLink :to="`/dashboard/ticket/${ticket.id}`"><span class="underline">View Ticket</span></RouterLink>
        </div>
    </div>    
</template>

<style scoped>
    .fade{
        mask-image: linear-gradient(180deg, #000 60%, transparent);
        -webkit-mask-image: linear-gradient(180deg, #000 60%, transparent);
    }
</style>