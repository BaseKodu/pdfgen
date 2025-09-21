<template>
  <div class="w-full">
    <div v-if="title" class="flex justify-between items-center mb-2">
      <h4 class="font-medium text-sm text-base-content">{{ title }}</h4>
      <AppButton
        v-if="showCopyButton"
        @click="copyToClipboard"
        variant="ghost"
        size="xs"
        :disabled="isCopying"
      >
        <span v-if="isCopying" class="loading loading-spinner loading-xs"></span>
        <AppIcon v-else name="copy"  />
      </AppButton>
    </div>
    <div class="mockup-code">
      <pre><code>{{ content }}</code></pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from '../../composables/useToast'
import AppButton from './AppButton.vue'
import AppIcon from './AppIcon.vue'

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  language: {
    type: String,
    default: 'text'
  },
  title: {
    type: String,
    default: ''
  },
  showCopyButton: {
    type: Boolean,
    default: true
  }
})

const { showSuccess, showError } = useToast()
const isCopying = ref(false)

const copyToClipboard = async () => {
  try {
    isCopying.value = true
    await navigator.clipboard.writeText(props.content)
    showSuccess('Copied to clipboard!')
  } catch (error) {
    console.error('Failed to copy:', error)
    showError('Failed to copy to clipboard')
  } finally {
    isCopying.value = false
  }
}
</script>
