<template>
  <AppForm
    :title="isEditing ? 'Edit API Key' : 'Create New API Key'"
    :description="isEditing ? 'Update your API key details' : 'Generate a new API key for external access'"
    :isLoading="isLoading"
    :submitText="isEditing ? 'Update Key' : 'Create Key'"
    @submit="handleSubmit"
    @cancel="handleCancel"
  >
    <div class="form-control">
      <label class="label">
        <span class="label-text">Name</span>
      </label>
      <AppInput
        v-model="formData.name"
        type="text"
        placeholder="e.g., My App API Key"
        class="input input-bordered"
        :class="{ 'input-error': errors.name }"
        required
      />
      <label v-if="errors.name" class="label">
        <span class="label-text-alt text-error">{{ errors.name }}</span>
      </label>
    </div>

    <div class="form-control">
      <label class="label">
        <span class="label-text">Description (Optional)</span>
      </label>
      <AppTextArea
        v-model="formData.description"
        placeholder="Describe what this key is for..."
        :rows=3
      ></AppTextArea>
    </div>

    <div class="form-control">
      <label class="label">
        <span class="label-text">Expires At (Optional)</span>
      </label>
      <AppInput
        v-model="formData.expires_at"
        type="datetime-local"
        class="input input-bordered"
        :class="{ 'input-error': errors.expires_at }"
      />
      <label v-if="errors.expires_at" class="label">
        <span class="label-text-alt text-error">{{ errors.expires_at }}</span>
      </label>
      <label v-else class="label">
        <span class="label-text-alt">Leave empty for no expiration</span>
      </label>
    </div>
  </AppForm>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import AppForm from '../ui/AppForm.vue'
import AppInput from '../ui/AppInput.vue'
import AppTextArea from '../ui/AppTextArea.vue'

const props = defineProps({
  apiKey: {
    type: Object,
    default: null
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

const isEditing = computed(() => !!props.apiKey)

const formData = ref({
  name: '',
  description: '',
  expires_at: ''
})

const errors = ref({
  name: '',
  description: '',
  expires_at: ''
})

const resetForm = () => {
  formData.value = {
    name: '',
    description: '',
    expires_at: ''
  }
  errors.value = {
    name: '',
    description: '',
    expires_at: ''
  }
}

// Watch for changes in the apiKey prop to populate form
watch(() => props.apiKey, (newApiKey) => {
  if (newApiKey) {
    formData.value = {
      name: newApiKey.name || '',
      description: newApiKey.description || '',
      expires_at: newApiKey.expires_at ? new Date(newApiKey.expires_at).toISOString().slice(0, 16) : ''
    }
  } else {
    resetForm()
  }
}, { immediate: true })



const validateForm = () => {
  errors.value = {
    name: '',
    description: '',
    expires_at: ''
  }

  let isValid = true

  if (!formData.value.name.trim()) {
    errors.value.name = 'Name is required'
    isValid = false
  }

  if (formData.value.expires_at) {
    const expiryDate = new Date(formData.value.expires_at)
    const now = new Date()
    if (expiryDate <= now) {
      errors.value.expires_at = 'Expiry date must be in the future'
      isValid = false
    }
  }

  return isValid
}

const handleSubmit = () => {
  if (validateForm()) {
    const payload = {
      name: formData.value.name.trim(),
      description: formData.value.description.trim() || null,
      expires_at: formData.value.expires_at ? new Date(formData.value.expires_at).toISOString() : null
    }
    emit('submit', payload)
  }
}

const handleCancel = () => {
  resetForm()
  emit('cancel')
}
</script>
