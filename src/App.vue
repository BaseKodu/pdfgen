<script setup lang="ts">
//import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <div data-theme="sunset">
    <div class="min-h-screen bg-base-200">
        <div class="flex flex-col lg:flex-row-reverse w-full">
          <RouterView />
        </div>
    </div>
  </div>
</template>

<style scoped>
</style>
