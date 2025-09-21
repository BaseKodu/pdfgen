<template>
  <div v-if="isOpen" class="modal" :class="{ 'modal-open': isOpen }">
    <div class="modal-box" :class="sizeClasses">
      <!-- Modal Header -->
      <div v-if="showCloseButton" class="flex justify-between items-center mb-4">
        <h3 v-if="title" class="font-bold text-lg">{{ title }}</h3>
        <button
          v-if="showCloseButton"
          @click="close"
          class="btn btn-sm btn-circle btn-ghost"
        >
          ✕
        </button>
      </div>
      <div v-else-if="title" class="mb-4">
        <h3 class="font-bold text-lg">{{ title }}</h3>
      </div>

      <!-- Modal Content -->
      <div class="w-full">
        <slot></slot>
      </div>

      <!-- Modal Actions -->
      <div v-if="showActions" class="modal-action">
        <slot name="actions">
          <AppButton @click="close" variant="ghost">Cancel</AppButton>
          <AppButton @click="confirm" variant="primary">Confirm</AppButton>
        </slot>
      </div>
    </div>
    <div v-if="showBackdrop" class="modal-backdrop" @click="closeOnBackdrop && close()"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppButton from './AppButton.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: false
  },
  showBackdrop: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close', 'confirm'])

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-full'
  }
  return sizes[props.size]
})

const close = () => {
  emit('close')
}

const confirm = () => {
  emit('confirm')
}
</script>
