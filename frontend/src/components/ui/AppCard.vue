<script setup>
import { RouterLink } from 'vue-router';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  link: {
    type: String,
    required: true
  },

});
</script>

<template>
  <div class="card bg-base-100 shadow-xl gap-4">
    <div class="card-body">
      <h2 class="card-title">{{ title }}</h2>
      <p>{{ description }}</p>
      <div class="card-actions justify-end">
        <RouterLink :to="link" class="btn btn-primary">Select</RouterLink>
      </div>
    </div>
  </div>
</template>
