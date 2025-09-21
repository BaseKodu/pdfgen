<template>
  <div class="api-endpoint">
    <div class="space-y-4">
      <!-- Endpoint Header -->
      <div class="flex items-center gap-3">
        <AppBadge :variant="methodVariant" size="sm">
          {{ method.toUpperCase() }}
        </AppBadge>
        <code class="bg-base-300 text-base-content px-3 py-1 rounded text-sm font-mono">
          {{ endpoint }}
        </code>
      </div>

      <!-- Description -->
      <p v-if="description" class="text-sm text-base-content/70">
        {{ description }}
      </p>

      <!-- Request Body Example -->
      <div v-if="requestExample" class="space-y-2">
        <h5 class="font-medium text-sm">Request Body:</h5>
        <AppCodeBlock
          :content="requestExample"
          language="json"
          :title="requestTitle"
        />
      </div>

      <!-- cURL Example -->
      <div v-if="curlExample" class="space-y-2">
        <h5 class="font-medium text-sm">cURL Example:</h5>
        <AppCodeBlock
          :content="curlExample"
          language="bash"
          :title="curlTitle"
        />
      </div>

      <!-- Response Codes -->
      <div v-if="responseCodes && responseCodes.length > 0" class="space-y-2">
        <h5 class="font-medium text-sm">Response Codes:</h5>
        <div class="space-y-1">
          <div
            v-for="code in responseCodes"
            :key="code.code"
            class="flex items-center gap-2 text-sm"
          >
            <AppBadge :variant="getCodeVariant(code.code)" size="xs">
              {{ code.code }}
            </AppBadge>
            <span>{{ code.description }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppBadge from '../ui/AppBadge.vue'
import AppCodeBlock from '../ui/AppCodeBlock.vue'

const props = defineProps({
  method: {
    type: String,
    required: true,
    validator: (value) => ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].includes(value.toUpperCase())
  },
  endpoint: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  requestExample: {
    type: String,
    default: ''
  },
  requestTitle: {
    type: String,
    default: ''
  },
  curlExample: {
    type: String,
    default: ''
  },
  curlTitle: {
    type: String,
    default: ''
  },
  responseCodes: {
    type: Array,
    default: () => []
  }
})

const methodVariant = computed(() => {
  const variants = {
    'GET': 'info',
    'POST': 'primary',
    'PUT': 'warning',
    'DELETE': 'error',
    'PATCH': 'secondary'
  }
  return variants[props.method.toUpperCase()] || 'neutral'
})

const getCodeVariant = (code) => {
  if (code >= 200 && code < 300) return 'success'
  if (code >= 400 && code < 500) return 'error'
  if (code >= 500) return 'error'
  return 'neutral'
}
</script>
