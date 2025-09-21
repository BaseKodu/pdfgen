<template>
  <div class="api-key-list">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">API Keys</h2>
      <AppButton
        variant="primary"
        @click="handleCreateNew"
        :disabled="isLoading"
      >
        <AppIcon name="plus"  />
        Create New Key
      </AppButton>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && apiKeys.length === 0" class="flex justify-center py-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <!-- Empty State -->
    <div v-else-if="apiKeys.length === 0" class="text-center py-8">
      <AppIcon name="key" size="12" />
      <p class="text-base-content/60 mb-4">No API keys found. Create your first one to get started!</p>
      <AppButton variant="primary" @click="handleCreateNew">
        <AppIcon name="plus" size="16" />
        Create Your First API Key
      </AppButton>
    </div>

    <!-- API Keys Grid -->
    <div v-else class="space-y-4">
      <ApiKeyCard
        v-for="apiKey in apiKeys"
        :key="apiKey.id"
        :apiKey="apiKey"
        :isLoading="isLoading"
        @toggle="handleToggle"
        @delete="handleDelete"
        @copy="handleCopy"
      />
    </div>

    <!-- Create Form -->
    <div v-if="showCreateForm" class="mt-6">
      <ApiKeyForm
        :isLoading="isCreating"
        @submit="handleCreate"
        @cancel="handleCancelCreate"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from '../../composables/useToast'
import AppButton from '../ui/AppButton.vue'
import AppIcon from '../ui/AppIcon.vue'
import ApiKeyCard from './ApiKeyCard.vue'
import ApiKeyForm from './ApiKeyForm.vue'

const props = defineProps({
  apiKeys: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['create', 'toggle', 'delete', 'copy'])

const { showSuccess, showError } = useToast()

const showCreateForm = ref(false)
const isCreating = ref(false)

const handleCreateNew = () => {
  showCreateForm.value = true
}

const handleCreate = async (formData) => {
  try {
    isCreating.value = true
    emit('create', formData)
    showCreateForm.value = false
  } catch (error) {
    console.error('Failed to create API key:', error)
    showError('Failed to create API key')
  } finally {
    isCreating.value = false
  }
}

const handleCancelCreate = () => {
  showCreateForm.value = false
}

const handleToggle = (apiKey) => {
  emit('toggle', apiKey)
}

const handleDelete = (keyId) => {
  if (confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
    emit('delete', keyId)
  }
}

const handleCopy = (key) => {
  emit('copy', key)
}
</script>
