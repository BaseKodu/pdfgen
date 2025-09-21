<template>
  <div class="api-key-manager">
    <!-- API Keys List -->
    <ApiKeyList
      :apiKeys="apiKeys"
      :isLoading="isLoading"
      @create="createApiKey"
      @toggle="toggleKey"
      @delete="deleteKey"
      @copy="copyToClipboard"
    />

    <!-- New API Key Modal -->
    <ApiKeyModal
      :isOpen="!!newApiKey"
      :apiKey="newApiKey"
      @close="closeNewKeyModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from '../composables/useToast'
import axios from 'axios'
import ApiKeyList from './api-keys/ApiKeyList.vue'
import ApiKeyModal from './api-keys/ApiKeyModal.vue'

const { showSuccess, showError } = useToast()

const apiKeys = ref([])
const isLoading = ref(false)
const newApiKey = ref(null)

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

const createApiKey = async (formData) => {
  try {
    const response = await axios.post('/api/api-keys', formData)
    newApiKey.value = response.data
    await loadApiKeys()
    showSuccess('API key created successfully!')
  } catch (error) {
    console.error('Failed to create API key:', error.response?.data || error.message)
    showError('Failed to create API key: ' + (error.response?.data?.detail || error.message))
  }
}

const toggleKey = async (apiKey) => {
  try {
    isLoading.value = true
    await axios.put(`/api/api-keys/${apiKey.id}`, {
      is_active: !apiKey.is_active
    })
    await loadApiKeys()
    showSuccess(`API key ${!apiKey.is_active ? 'activated' : 'deactivated'}`)
  } catch (error) {
    console.error('Failed to toggle API key status:', error)
    showError('Failed to toggle API key status')
  } finally {
    isLoading.value = false
  }
}

const deleteKey = async (keyId) => {
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

const copyToClipboard = async (key) => {
  try {
    await navigator.clipboard.writeText(key)
    showSuccess('Copied to clipboard!')
  } catch (error) {
    console.error('Failed to copy:', error)
    showError('Failed to copy to clipboard')
  }
}

const closeNewKeyModal = () => {
  newApiKey.value = null
}

onMounted(() => {
  loadApiKeys()
})
</script>
