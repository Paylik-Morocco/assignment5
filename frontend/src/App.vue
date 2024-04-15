<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavHeader from './components/NavHeader.vue'
</script>

<template>

  <nav-header></nav-header>
  <div class="bg-slate-100">
    <main class="container mx-auto px-4">
      <RouterView />
    </main>
  </div>
</template>
