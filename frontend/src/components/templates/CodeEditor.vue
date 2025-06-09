<script setup>
import { ref, watch } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { javascript } from '@codemirror/lang-javascript'
import { html } from '@codemirror/lang-html'
import { json } from '@codemirror/lang-json'
import { oneDark } from '@codemirror/theme-one-dark'

const props = defineProps({
  engine: {
    type: String,
    default: 'html'
  },
  content: {
    type: String,
    default: '// Type your code here nunjucks'
  },
  data: {
    type: String,
    default: '{\n  // Add your template data here\n}'
  }
})

const emit = defineEmits(['update:content', 'update:data'])

const engine = ref(props.engine)
const editorContent = ref(props.content)
const dataContent = ref(props.data)
const activeTab = ref('code')

// Watch for changes in the content prop
watch(() => props.content, (newContent) => {
  if (newContent !== editorContent.value) {
    editorContent.value = newContent
  }
}, { immediate: true })

// Watch for changes in the data prop
watch(() => props.data, (newData) => {
  if (newData !== dataContent.value) {
    dataContent.value = newData
  }
}, { immediate: true })

// Watch for changes in the editor content
watch(editorContent, (newContent) => {
  emit('update:content', newContent)
})

// Watch for changes in the data content
watch(dataContent, (newData) => {
  emit('update:data', newData)
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

const codeExtensions = [language(), oneDark]
const dataExtensions = [json(), oneDark]
</script>

<template>
  <div class="editor-container">
    <div class="tabs tabs-boxed mb-2">
      <a
        class="tab"
        :class="{ 'tab-active': activeTab === 'code' }"
        @click="activeTab = 'code'"
      >
        Code
      </a>
      <a
        class="tab"
        :class="{ 'tab-active': activeTab === 'data' }"
        @click="activeTab = 'data'"
      >
        Data
      </a>
    </div>

    <div v-show="activeTab === 'code'" class="h-[400px]">
      <Codemirror
        v-model="editorContent"
        :extensions="codeExtensions"
        :style="{ height: '100%' }"
      />
    </div>

    <div v-show="activeTab === 'data'" class="h-[400px]">
      <Codemirror
        v-model="dataContent"
        :extensions="dataExtensions"
        :style="{ height: '100%' }"
      />
    </div>
  </div>
</template>
