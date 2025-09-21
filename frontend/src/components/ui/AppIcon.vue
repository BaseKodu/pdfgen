<template>
  <v-icon
    :name="iconName"
    :class="sizeClasses"
    :style="{
      animation: spinning ? 'spin 1s linear infinite' : 'none'
    }"
  />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: [String, Number],
    default: 24
  },
  spinning: {
    type: Boolean,
    default: false
  }
})

const iconName = computed(() => {
  // Map our icon names to oh-vue-icons names
  const iconMap = {
    // Navigation
    'plus': 'bi-plus',
    'minus': 'bi-dash',
    'close': 'bi-x',
    'check': 'bi-check',
    'arrow-left': 'bi-arrow-left',
    'arrow-right': 'bi-arrow-right',
    'arrow-up': 'bi-arrow-up',
    'arrow-down': 'bi-arrow-down',

    // Actions
    'copy': 'bi-clipboard',
    'edit': 'bi-pencil',
    'trash': 'bi-trash',
    'download': 'bi-download',
    'upload': 'bi-upload',

    // Status
    'check-circle': 'bi-check-circle',
    'x-circle': 'bi-x-circle',
    'alert-circle': 'bi-exclamation-triangle',
    'info': 'bi-info-circle',

    // UI Elements
    'menu': 'bi-list',
    'search': 'bi-search',
    'filter': 'bi-funnel',
    'settings': 'bi-gear',
    'user': 'bi-person',
    'lock': 'bi-lock',
    'unlock': 'bi-unlock',

    // API/Documentation
    'key': 'bi-key',
    'document': 'bi-file-text',
    'code': 'bi-code',
    'terminal': 'bi-terminal',

    // Loading/Spinner
    'spinner': 'bi-arrow-clockwise',
    'refresh': 'bi-arrow-clockwise'
  }

  return iconMap[props.name] || 'bi-question-circle'
})

const sizeClasses = computed(() => {
  const sizes = {
    16: 'w-4 h-4',
    20: 'w-5 h-5',
    24: 'w-6 h-6',
    32: 'w-8 h-8',
    48: 'w-12 h-12'
  }
  return sizes[props.size] || `w-${props.size} h-${props.size}`
})
</script>

<style scoped>
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
