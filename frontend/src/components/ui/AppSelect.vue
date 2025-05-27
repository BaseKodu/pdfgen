<script setup>
const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean, Object],
    default: null
  },
  options: {
    type: Array,
    required: true,
    validator: (value) => {
      return value.every(option =>
        typeof option === 'object'
          ? ('value' in option && 'label' in option)
          : true
      )
    }
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

const emit = defineEmits(['update:modelValue', 'change'])

const handleChange = (event) => {
  const value = event.target.value
  emit('update:modelValue', value)
  emit('change', value)
}
</script>

<template>
  <div class="form-control w-full">
    <label v-if="label" class="label">
      <span class="label-text">{{ label }}</span>
    </label>

    <select
      class="select select-bordered"
      :class="{
        'select-error': error,
        'select-primary': !error,
        'select-disabled': disabled
      }"
      :value="modelValue"
      @change="handleChange"
      :disabled="disabled"
    >
      <option v-if="placeholder" disabled selected :value="null">
        {{ placeholder }}
      </option>
      <option
        v-for="option in options"
        :key="option.value || option"
        :value="option.value || option"
      >
        {{ option.label || option }}
      </option>
    </select>

    <label v-if="error" class="label">
      <span class="label-text-alt text-error">{{ error }}</span>
    </label>
    <label v-if="hint && !error" class="label">
      <span class="label-text-alt text-info">{{ hint }}</span>
    </label>
  </div>
</template>

