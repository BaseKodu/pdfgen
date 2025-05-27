<template>
  <div class="textarea-container">
    <label v-if="label" :for="id" class="textarea-label">{{ label }}</label>
    <textarea
      :id="id"
      class="textarea"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :rows="rows"
      :class="{ 'textarea-error': error }"
      @input="handleInput"
      @blur="handleBlur"
    ></textarea>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="hint && !error" class="hint-text">{{ hint }}</div>
    <div v-if="showCount" class="character-count">
      {{ modelValue?.length || 0 }}/{{ maxLength }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
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
  },
  rows: {
    type: Number,
    default: 4
  },
  maxLength: {
    type: Number,
    default: null
  },
  showCount: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'blur'])

const id = computed(() => `textarea-${Math.random().toString(36).slice(2, 9)}`)

const handleInput = (event) => {
  let value = event.target.value
  if (props.maxLength) {
    value = value.slice(0, props.maxLength)
  }
  emit('update:modelValue', value)
}

const handleBlur = (event) => {
  emit('blur', event)
}
</script>
