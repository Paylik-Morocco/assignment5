<script setup>
import axios from 'axios';
import { FwbButton, FwbInput, FwbCard } from 'flowbite-vue'
import { ref } from 'vue';
import {useAuthStore} from '../stores/authStore';
import router from '@/router';
const auth = useAuthStore();

const formdata = ref({ email: '', password: '' })

const submit = async e => {
    auth.login({
        email: formdata.value.email,
        password: formdata.value.password
    }).then((data)=>{
        router.replace({path: '/dashboard'})
    }).catch(e=>{
        console.log(e);
    })
}

</script>

<template>
    <div class="mt-12">
        <div class="bg-white shadow-md border rounded-2xl md:max-w-[400px] mx-auto">
            <div class="p-4 md:p-8 lg:p-12">
                <form @submit.prevent="submit">
                    <h1 class="text-center my-6 font-semibold text-3xl">Login</h1>
                    <fwb-input v-model="formdata.email" placeholder="email" label="Email" />
                    <br>
                    <fwb-input v-model="formdata.password" placeholder="password" label="password" type="password" />
                    <br>
                    <FwbButton class="w-full">Login</FwbButton>
                </form>
            </div>
        </div>
    </div>
</template>