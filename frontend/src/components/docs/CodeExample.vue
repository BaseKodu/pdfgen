<template>
  <div>
    <div v-if="title" class="mb-2">
      <h5 class="font-medium text-sm">{{ title }}</h5>
    </div>
    <AppCodeBlock
      :content="content"
      :language="language"
      :showCopyButton="showCopyButton"
    />
  </div>
</template>

<script setup>
import AppCodeBlock from '../ui/AppCodeBlock.vue'

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
</script>
