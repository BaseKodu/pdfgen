<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  message: {
    type: String,
    default: 'Default toast message'
  },
  type: {
    type: String,
    default: 'info'
  },
  placement: {
    type: String,
    default: 'toast-start toast-middle'
  },
});
</script>

<template>
  <div :class="`toast ${props.placement}`">
    <div :class="`alert alert-${props.placement}`">
      <p>{{ props.message }}</p>
    </div>
  </div>

</template>
