<template>
  <span
    :class="[
      'badge',
      variantClasses,
      sizeClasses,
      { 'badge-outline': outline }
    ]"
  >
    <slot></slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { BUTTON_VARIANTS, BUTTON_VARIANT_VALUES } from '../../composables/useComposables'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => BUTTON_VARIANT_VALUES.includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg'].includes(value)
  },
  outline: {
    type: Boolean,
    default: false
  }
})

const variantClasses = computed(() => {
  const variants = {
    neutral: 'badge-neutral',
    primary: 'badge-primary',
    secondary: 'badge-secondary',
    accent: 'badge-accent',
    success: 'badge-success',
    warning: 'badge-warning',
    error: 'badge-error',
    info: 'badge-info'
  }
  return variants[props.variant] || 'badge-neutral'
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'badge-xs',
    sm: 'badge-sm',
    md: '',
    lg: 'badge-lg'
  }
  return sizes[props.size]
})
</script>
