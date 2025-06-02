
<script setup>
import { ref } from 'vue'
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

const engine = ref(props.engine)
const content = ref(props.content)

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


const onChange = (value) => {
  console.log('changed:', value)
}
</script>

<template>
  <div class="editor-container">
    <Codemirror
      v-model="content"
      :extensions="extensions"
      :style="{ height: '400px' }"
      @change="onChange"
    />
  </div>
</template>
