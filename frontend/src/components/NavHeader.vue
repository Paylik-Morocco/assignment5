<script setup>
import { useAuthStore } from '@/stores/authStore';
import { FwbNavbar, FwbNavbarCollapse, FwbNavbarLink } from 'flowbite-vue'
import {RouterLink} from 'vue-router';

const auth = useAuthStore();

</script>


<template>
    <fwb-navbar class="py-4">
        <template #logo>
            <span class="text-lg font-semibold">Task Management</span>
        </template>
        <template #default="{isShowMenu}">
            <fwb-navbar-collapse :is-show-menu="isShowMenu">
                <fwb-navbar-link v-if="!auth.user">
                    <RouterLink to="/" class="underline">Home</RouterLink>
                </fwb-navbar-link>
                <fwb-navbar-link v-if="!auth.user">
                    <RouterLink to="/login" class="underline">Login</RouterLink>
                </fwb-navbar-link>
                <fwb-navbar-link v-if="!auth.user">
                    <RouterLink to="/register" class="underline">Register</RouterLink>
                </fwb-navbar-link>
                <span v-if="auth.user">Welcome, {{ auth.user?.username }}!</span>
                <fwb-navbar-link v-if="auth.user">
                    <span @click="auth.logout" class="underline">Logout</span>
                </fwb-navbar-link>
            </fwb-navbar-collapse>
        </template>
    </fwb-navbar>
</template>