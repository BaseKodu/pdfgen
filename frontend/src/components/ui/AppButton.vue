<script setup>
import { VueSpinnerSync } from  'vue3-spinners';

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger', 'success', 'outline'].includes(value)
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
  <section v-if="!isLoading">
    <button
      :class="['btn', 'btn-active', `btn-${variant}`]"
      :type="type"
      :disabled="disabled"
      @click="handleClick"
    >
      <slot></slot>
    </button>
  </section>
  <div v-else>
    <VueSpinnerSync />
  </div>
</template>

