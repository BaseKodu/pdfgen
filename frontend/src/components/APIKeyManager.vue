<template>
  <div class="api-key-manager">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">API Keys</h2>
      <button
        @click="showCreateForm = true"
        class="btn btn-primary"
        :disabled="isLoading"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        Create New Key
      </button>
    </div>

    <!-- Create API Key Form -->
    <div v-if="showCreateForm" class="card bg-base-200 mb-6">
      <div class="card-body">
        <h3 class="card-title">Create New API Key</h3>
        <form @submit.prevent="createApiKey" class="space-y-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text">Name</span>
            </label>
            <input
              v-model="newKey.name"
              type="text"
              placeholder="e.g., My App API Key"
              class="input input-bordered"
              required
            />
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text">Description (Optional)</span>
            </label>
            <textarea
              v-model="newKey.description"
              placeholder="Describe what this key is for..."
              class="textarea textarea-bordered"
            ></textarea>
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text">Expires At (Optional)</span>
            </label>
            <input
              v-model="newKey.expires_at"
              type="datetime-local"
              class="input input-bordered"
            />
          </div>
          <div class="card-actions justify-end">
            <button type="button" @click="cancelCreate" class="btn btn-ghost">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isCreating">
              <span v-if="isCreating" class="loading loading-spinner loading-sm"></span>
              Create Key
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- API Keys List -->
    <div v-if="isLoading" class="flex justify-center">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else-if="apiKeys.length === 0" class="text-center py-8">
      <p class="text-gray-500">No API keys found. Create your first one to get started!</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="key in apiKeys"
        :key="key.id"
        class="card bg-base-100 shadow-sm border"
      >
        <div class="card-body">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h3 class="card-title text-lg">{{ key.name }}</h3>
              <p v-if="key.description" class="text-sm text-gray-600 mt-1">
                {{ key.description }}
              </p>
              <div class="flex items-center gap-4 mt-2 text-sm text-gray-500">
                <span>Created: {{ formatDate(key.created_at) }}</span>
                <span v-if="key.last_used">Last used: {{ formatDate(key.last_used) }}</span>
                <span v-if="key.expires_at">Expires: {{ formatDate(key.expires_at) }}</span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span
                :class="[
                  'badge',
                  key.is_active ? 'badge-success' : 'badge-error'
                ]"
              >
                {{ key.is_active ? 'Active' : 'Inactive' }}
              </span>
              <button
                @click="toggleKey(key)"
                class="btn btn-sm btn-outline"
                :disabled="isLoading"
              >
                {{ key.is_active ? 'Deactivate' : 'Activate' }}
              </button>
              <button
                @click="deleteKey(key.id)"
                class="btn btn-sm btn-error"
                :disabled="isLoading"
              >
                Delete
              </button>
            </div>
          </div>
          <div class="mt-3">
            <div class="flex items-center gap-2">
              <code class="bg-gray-100 px-2 py-1 rounded text-sm font-mono">
                {{ key.key }}
              </code>
              <button
                @click="copyToClipboard(key.key)"
                class="btn btn-xs btn-ghost"
                title="Copy to clipboard"
              >
                📋
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- New API Key Modal -->
    <div v-if="newApiKey" class="modal modal-open">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-4">New API Key Created!</h3>
        <div class="alert alert-warning mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <span>This is the only time you'll see the full API key. Copy it now!</span>
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text">Your API Key</span>
          </label>
          <div class="flex items-center gap-2">
            <input
              :value="newApiKey.key"
              readonly
              class="input input-bordered flex-1 font-mono"
            />
            <button
              @click="copyToClipboard(newApiKey.key)"
              class="btn btn-primary"
            >
              Copy
            </button>
          </div>
        </div>
        <div class="modal-action">
          <button @click="closeNewKeyModal" class="btn btn-primary">
            Got it!
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from '../composables/useToast'
import axios from 'axios'

const { showSuccess, showError } = useToast()

const apiKeys = ref([])
const isLoading = ref(false)
const isCreating = ref(false)
const showCreateForm = ref(false)
const newApiKey = ref(null)

const newKey = ref({
  name: '',
  description: '',
  expires_at: ''
})

const loadApiKeys = async () => {
  try {
    isLoading.value = true
    const response = await axios.get('/api/api-keys')
    apiKeys.value = response.data
  } catch (error) {
    console.error('Failed to load API keys:', error)
    showError('Failed to load API keys')
  } finally {
    isLoading.value = false
  }
}

const createApiKey = async () => {
  try {
    isCreating.value = true
    // Filter out empty values to avoid validation errors
    const payload = {
      name: newKey.value.name,
      description: newKey.value.description || null,
      expires_at: newKey.value.expires_at ? new Date(newKey.value.expires_at).toISOString() : null
    }
    const response = await axios.post('/api/api-keys', payload)
    newApiKey.value = response.data
    showCreateForm.value = false
    newKey.value = { name: '', description: '', expires_at: '' }
    await loadApiKeys()
    showSuccess('API key created successfully!')
  } catch (error) {
    console.error('Failed to create API key:', error)
    showError('Failed to create API key')
  } finally {
    isCreating.value = false
  }
}

const toggleKey = async (key) => {
  try {
    isLoading.value = true
    await axios.put(`/api/api-keys/${key.id}`, {
      is_active: !key.is_active
    })
    await loadApiKeys()
    showSuccess(`API key ${!key.is_active ? 'activated' : 'deactivated'}`)
  } catch (error) {
    console.error('Failed to toggle API key:', error)
    showError('Failed to update API key')
  } finally {
    isLoading.value = false
  }
}

const deleteKey = async (keyId) => {
  if (!confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
    return
  }

  try {
    isLoading.value = true
    await axios.delete(`/api/api-keys/${keyId}`)
    await loadApiKeys()
    showSuccess('API key deleted successfully')
  } catch (error) {
    console.error('Failed to delete API key:', error)
    showError('Failed to delete API key')
  } finally {
    isLoading.value = false
  }
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showSuccess('Copied to clipboard!')
  } catch (error) {
    console.error('Failed to copy:', error)
    showError('Failed to copy to clipboard')
  }
}

const cancelCreate = () => {
  showCreateForm.value = false
  newKey.value = { name: '', description: '', expires_at: '' }
}

const closeNewKeyModal = () => {
  newApiKey.value = null
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadApiKeys()
})
</script>
