<script setup>
import { BUTTON_VARIANTS, BUTTON_VARIANT_VALUES } from '../../composables/useComposables'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => BUTTON_VARIANT_VALUES.includes(value)
  },
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (!props.disabled) {
    emit('click', event)
  }
}



</script>

<template>
  <button
    :class="['btn', 'btn-soft', `btn-${variant}`]"
    :type="type"
    :disabled="disabled || isLoading"
    @click="handleClick"
  >
    <span v-if="isLoading" class="loading loading-dots"></span>
    <slot v-if="!isLoading"></slot>
  </button>
</template>

