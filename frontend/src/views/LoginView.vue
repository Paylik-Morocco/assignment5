<script setup>
import { FwbButton, FwbInput, FwbCard } from 'flowbite-vue'
import NavHeader from '../components/NavHeader.vue'
</script>

<template>
    <div class="border rounded-2xl md:max-w-[400px] mx-auto">
        <div class="p-4 md:p-8 lg:p-12">
            <h1 class="text-center my-6 font-semibold text-3xl">Login</h1>
            <fwb-input placeholder="email" label="Email" />
            <br>
            <fwb-input placeholder="password" label="password" type="password" />
            <br>
            <FwbButton class="w-full">Login</FwbButton>
        </div>
    </div>
</template>