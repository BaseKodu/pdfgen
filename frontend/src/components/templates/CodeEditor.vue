<script setup>
import { ref, watch } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { javascript } from '@codemirror/lang-javascript'
import { html } from '@codemirror/lang-html'
import { oneDark } from '@codemirror/theme-one-dark'

const props = defineProps({
  engine: {
    type: String,
    default: 'html'
  },
  content: {
    type: String,
    default: '// Type your code here nunjucks'
  }
})

const emit = defineEmits(['update:content'])

const engine = ref(props.engine)
const editorContent = ref(props.content)

// Watch for changes in the content prop
watch(() => props.content, (newContent) => {
  if (newContent !== editorContent.value) {
    editorContent.value = newContent
  }
}, { immediate: true })

// Watch for changes in the editor content
watch(editorContent, (newContent) => {
  emit('update:content', newContent)
})

const language = () => {
  if (engine.value === 'html') {
    return javascript({jsx:true})
  } else if (engine.value === 'vue') {
    return javascript({jsx:true})
  } else if (engine.value === 'jsx') {
    return javascript({jsx:true})
  }
}

const extensions = [language(), oneDark]
</script>

<template>
  <div class="editor-container">
    <Codemirror
      v-model="editorContent"
      :extensions="extensions"
      :style="{ height: '400px' }"
    />
  </div>
</template>
