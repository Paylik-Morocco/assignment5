<script setup>
import { FwbNavbar, FwbNavbarCollapse, FwbNavbarLink } from 'flowbite-vue'
import {RouterLink} from 'vue-router'
</script>


<template>
    <fwb-navbar class="py-4">
        <template #logo>
            <span class="text-lg font-semibold">Task Management</span>
        </template>
        <template #default="{isShowMenu}">
            <fwb-navbar-collapse :is-show-menu="isShowMenu">
                <fwb-navbar-link>
                    <RouterLink to="/">Home</RouterLink>
                </fwb-navbar-link>
                <fwb-navbar-link>
                    <RouterLink to="/login">Login</RouterLink>
                </fwb-navbar-link>
                <fwb-navbar-link>
                    <RouterLink to="/register">Register</RouterLink>
                </fwb-navbar-link>
            </fwb-navbar-collapse>
        </template>
    </fwb-navbar>
</template>