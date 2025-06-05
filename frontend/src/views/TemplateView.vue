<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from '../components/ui/AppNavbar.vue'
import CodeEditor from '../components/templates/CodeEditor.vue'
import AppButton from '../components/ui/AppButton.vue'
import { updateTemplate, getTemplate } from '../services/templates'

const route = useRoute()
const templateId = route.params.id

const isLoading = ref(false)

const code = ref('')

const getCurrentTemplate = async() => {
  try {
    isLoading.value = true
    const response = await getTemplate(templateId)
    code.value = response.content
    console.log(response)
  } catch (error) {
    console.error('Error fetching template:', error)
  } finally {
    isLoading.value = false
  }
}

const saveTemplate = async() => {
  try {
    isLoading.value = true
    const data = {
      content: code.value,
      data: {}
    }
    const response = await updateTemplate(templateId, data)
    console.log('Template updated:', response)
  } catch (error) {
    console.error('Error updating template:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  getCurrentTemplate();
});

</script>

<template>
  <div class="flex flex-col min-h-screen">
    <AppNavbar />

    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold">Template {{ templateId }}</h1>
    </div>

    <div class="flex">
      <div class="w-1/2 p-4">
        <CodeEditor
          v-model:content="code"
          :engine="'jsx'"
        />
        <AppButton @click="saveTemplate" :isLoading="isLoading">Save</AppButton>
      </div>
      <div class="w-1/2 p-4">
        <!-- Right side content can go here -->
      </div>
    </div>
  </div>
</template>
