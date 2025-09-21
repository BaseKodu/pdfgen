<template>
  <form
    :class="formClasses"
    @submit.prevent="handleSubmit"
  >
    <!-- Form Header -->
    <div v-if="title" class="mb-6">
      <h3 class="text-lg font-semibold text-base-content">{{ title }}</h3>
      <p v-if="description" class="text-sm text-base-content/70 mt-1">{{ description }}</p>
    </div>

    <!-- Form Content -->
    <div :class="contentClasses">
      <slot></slot>
    </div>

    <!-- Form Actions -->
    <div v-if="showActions" class="flex justify-end gap-3 mt-6">
      <slot name="actions">
        <AppButton
          type="button"
          variant="ghost"
          @click="handleCancel"
          :disabled="isLoading"
        >
          Cancel
        </AppButton>
        <AppButton
          type="submit"
          variant="primary"
          :isLoading="isLoading"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
          {{ submitText }}
        </AppButton>
      </slot>
    </div>
  </form>
</template>

<script setup>
import { computed } from 'vue'
import AppButton from './AppButton.vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  showActions: {
    type: Boolean,
    default: true
  },
  submitText: {
    type: String,
    default: 'Submit'
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  layout: {
    type: String,
    default: 'vertical',
    validator: (value) => ['vertical', 'horizontal', 'inline'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formClasses = computed(() => {
  const classes = ['w-full']

  if (props.layout === 'inline') {
    classes.push('flex', 'flex-wrap', 'items-end', 'gap-4')
  }

  return classes.join(' ')
})

const contentClasses = computed(() => {
  const classes = []

  if (props.layout === 'horizontal') {
    classes.push('grid', 'grid-cols-1', 'md:grid-cols-2', 'gap-4')
  } else if (props.layout === 'inline') {
    classes.push('flex', 'flex-wrap', 'gap-4')
  } else {
    // Vertical layout
    if (props.size === 'sm') {
      classes.push('space-y-3')
    } else if (props.size === 'lg') {
      classes.push('space-y-6')
    } else {
      classes.push('space-y-4')
    }
  }

  return classes.join(' ')
})

const handleSubmit = () => {
  emit('submit')
}

const handleCancel = () => {
  emit('cancel')
}
</script>
