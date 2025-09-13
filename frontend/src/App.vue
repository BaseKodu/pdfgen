<script setup>
import { RouterView } from 'vue-router';
import AppToast from './components/ui/AppToast.vue';

</script>

<template>
  <div data-theme="sunset">
    <div class="min-h-screen bg-base-200">
      <div class="flex flex-col w-full">
        <AppToast position="top-center" />
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
