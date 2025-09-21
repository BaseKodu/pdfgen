<template>
  <div class="card bg-base-100 shadow-sm border">
    <div class="card-body">
      <div class="flex justify-between items-start">
        <div class="flex-1">
          <h3 class="card-title text-lg">{{ apiKey.name }}</h3>
          <p v-if="apiKey.description" class="text-sm text-base-content/70 mt-1">
            {{ apiKey.description }}
          </p>
          <div class="flex items-center gap-4 mt-2 text-sm text-base-content/60">
            <span>Created: {{ formatDate(apiKey.created_at) }}</span>
            <span v-if="apiKey.last_used">Last used: {{ formatDate(apiKey.last_used) }}</span>
            <span v-if="apiKey.expires_at">Expires: {{ formatDate(apiKey.expires_at) }}</span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <AppBadge
            :variant="apiKey.is_active ? 'success' : 'warning'"
            size="sm"
          >
            {{ apiKey.is_active ? 'Active' : 'Inactive' }}
          </AppBadge>
          <AppButton
            variant="warning"
            size="sm"
            :disabled="isLoading"
            @click="toggleKey"
          >
            {{ apiKey.is_active ? 'Deactivate' : 'Activate' }}
        </AppButton>
          <AppButton
            variant="error"
            size="sm"
            :disabled="isLoading"
            @click="deleteKey"
          >
            <AppIcon name="trash" class="w-4 h-4" />
          </AppButton>
        </div>
      </div>
      <div class="mt-3">
        <div class="flex items-center gap-2">
          <code class="bg-base-200 px-2 py-1 rounded text-sm font-mono flex-1">
            {{ apiKey.key }}
          </code>
          <AppButton
            variant="ghost"
            size="xs"
            @click="copyToClipboard"
            title="Copy to clipboard"
          >
            <AppIcon name="copy" />
          </AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useToast } from '../../composables/useToast'
import AppBadge from '../ui/AppBadge.vue'
import AppButton from '../ui/AppButton.vue'
import AppIcon from '../ui/AppIcon.vue'

const props = defineProps({
  apiKey: {
    type: Object,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['toggle', 'delete', 'copy'])

const { showSuccess, showError } = useToast()

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const toggleKey = () => {
  emit('toggle', props.apiKey)
}

const deleteKey = () => {
  emit('delete', props.apiKey.id)
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.apiKey.key)
    showSuccess('Copied to clipboard!')
    emit('copy', props.apiKey.key)
  } catch (error) {
    console.error('Failed to copy:', error)
    showError('Failed to copy to clipboard')
  }
}
</script>
