<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from '../components/ui/AppNavbar.vue'
import CodeEditor from '../components/templates/CodeEditor.vue'
import AppButton from '../components/ui/AppButton.vue'
import PDFPreview from '../components/templates/PDFPreview.vue'
import { updateTemplate, getTemplate } from '../services/templates'

const route = useRoute()
const templateId = route.params.id
const pdfPreviewRef = ref(null)
const isLoading = ref(false)
const code = ref('')

const getCurrentTemplate = async() => {
  try {
    isLoading.value = true
    const response = await getTemplate(templateId)
    code.value = response.content
    //console.log(response)
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
      //data: {}
    }
    await updateTemplate(templateId, data)
    // Generate PDF preview after successful save
    await pdfPreviewRef.value.updatePreview()
  } catch (error) {
    console.error('Error updating template:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  getCurrentTemplate();
  pdfPreviewRef.value.updatePreview();
});

</script>

<template>
  <div class="flex flex-col min-h-screen">
    <AppNavbar />

    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold">Template {{ templateId }}</h1>
    </div>

    <div class="flex flex-1">
      <div class="w-1/2 p-4 flex flex-col">
        <div class="mb-4">
          <AppButton @click="saveTemplate" :isLoading="isLoading" class="w-full">
            Save Template & Generate PDF
          </AppButton>
        </div>
        <div class="flex-1">
          <CodeEditor
            v-model:content="code"
            :engine="'jsx'"
          />
        </div>
      </div>
      <div class="w-1/2 p-4 h-[calc(100vh-120px)]">
        <PDFPreview
          ref="pdfPreviewRef"
          :templateId="templateId"
        />
      </div>
    </div>
  </div>
</template>
