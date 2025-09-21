<template>
  <div class="api-docs-section">
    <div class="card bg-base-200">
      <div class="card-body">
        <h3 class="card-title">{{ title }}</h3>
        <p v-if="description" class="text-sm text-base-content/70 mb-4">
          {{ description }}
        </p>
        <div class="space-y-6">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  }
})
</script>
