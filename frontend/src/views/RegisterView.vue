<script setup>
import axios from 'axios';
import { FwbButton, FwbInput, FwbCard } from 'flowbite-vue'
import { ref } from 'vue';
import {useAuthStore} from '../stores/authStore';
import router from '@/router';
const auth = useAuthStore();

const formdata = ref({
    username: '',
    email: '',
    password: '',
})
const formdataErrors = ref({});
const submit = async e => {
    auth.register({
        username: formdata.value.username,
        email: formdata.value.email,
        password: formdata.value.password,
    }).then(()=>{
        router.push('/login')
    }).catch(data=>{
        formdataErrors.value = data
    })
}

</script>

<template>
    <div class="mt-12">
        <div class="bg-white shadow-md border rounded-2xl md:max-w-[400px] mx-auto">
            <div class="p-4 md:p-8 lg:p-12">
                <form @submit.prevent="submit">
                    <h1 class="text-center my-6 font-semibold text-3xl">Register</h1>
                    <fwb-input v-model="formdata.username" placeholder="username" label="Username" />
                    <span class="text-sm text-red-500 mb-6 block" v-for="err in formdataErrors.username">{{ err }}</span>

                    <fwb-input v-model="formdata.email" placeholder="email" label="Email" />
                    <span class="text-sm text-red-500 mb-6 block" v-for="err in formdataErrors.email">{{ err }}</span>

                    <fwb-input v-model="formdata.password" placeholder="password" label="password" type="Password" />
                    <span class="text-sm text-red-500 mb-6 block" v-for="err in formdataErrors.username">{{ err }}</span>

                    <FwbButton class="w-full mt-4">Register</FwbButton>
                </form>
            </div>
        </div>
    </div>
</template>