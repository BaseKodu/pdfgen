<template>
  <AppModal
    :isOpen="isOpen"
    title="New API Key Created!"
    size="lg"
    :showActions="false"
    @close="handleClose"
  >
    <div class="space-y-4">
      <div class="alert alert-warning">
        <AppIcon name="bi-exclamation-triangle" class="w-6 h-6" />
        <span>This is the only time you'll see the full API key. Copy it now!</span>
      </div>

      <div class="form-control">
        <label class="label">
          <span class="label-text font-medium">Your API Key</span>
        </label>
        <div class="flex items-center gap-2">
          <input
            :value="apiKey?.key"
            readonly
            class="input input-bordered flex-1 font-mono text-sm"
          />
          <AppButton
            variant="primary"
            @click="copyToClipboard"
            :isLoading="isCopying"
          >
            <span v-if="isCopying" class="loading loading-spinner loading-sm"></span>
            <AppIcon v-else name="bi-clipboard" />
            {{ isCopying ? 'Copying...' : 'Copy' }}
          </AppButton>
        </div>
      </div>

      <div v-if="apiKey" class="bg-base-200 p-4 rounded-lg">
        <h4 class="font-medium mb-2">Key Details:</h4>
        <div class="text-sm space-y-1">
          <div><strong>Name:</strong> {{ apiKey.name }}</div>
          <div v-if="apiKey.description"><strong>Description:</strong> {{ apiKey.description }}</div>
          <div v-if="apiKey.expires_at"><strong>Expires:</strong> {{ formatDate(apiKey.expires_at) }}</div>
        </div>
      </div>
    </div>

    <div class="modal-action">
      <AppButton variant="primary" @click="handleClose">
        Got it!
      </AppButton>
    </div>
  </AppModal>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from '../../composables/useToast'
import AppModal from '../ui/AppModal.vue'
import AppButton from '../ui/AppButton.vue'
import AppIcon from '../ui/AppIcon.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  apiKey: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const { showSuccess, showError } = useToast()
const isCopying = ref(false)

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const copyToClipboard = async () => {
  if (!props.apiKey?.key) return

  try {
    isCopying.value = true
    await navigator.clipboard.writeText(props.apiKey.key)
    showSuccess('API key copied to clipboard!')
  } catch (error) {
    console.error('Failed to copy:', error)
    showError('Failed to copy to clipboard')
  } finally {
    isCopying.value = false
  }
}

const handleClose = () => {
  emit('close')
}
</script>
