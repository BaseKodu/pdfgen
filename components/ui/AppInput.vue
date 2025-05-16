
<script setup lang="ts">
import { computed } from 'vue'

const _props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String as () => 
      'text' | 'password' | 'email' | 'number' | 'tel' | 'url' | 'search',
    default: 'text',
    validator: (value: string) => [
      'text',
      'password',
      'email',
      'number',
      'tel',
      'url',
      'search'
    ].includes(value)
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number): void
  (e: 'blur', event: Event): void
}>()

const id = computed(() => 'input-' + useId())

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const handleBlur = (event: Event) => {
  emit('blur', event)
}
</script>


<template>
  <div class="input-container">
    <label v-if="label" :for="id" class="label-text">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :class="['input input-bordered', { 'input-error': error }]"
      @input="handleInput"
      @blur="handleBlur"
    >
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="hint && !error" class="hint-text">{{ hint }}</div>
  </div>
</template>
