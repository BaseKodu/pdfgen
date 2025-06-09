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
const data = ref('{\n  // Add your template data here\n}')

const getCurrentTemplate = async() => {
  try {
    isLoading.value = true
    const response = await getTemplate(templateId)
    code.value = response.content
    data.value = response.data ? JSON.stringify(response.data, null, 2) : '{\n  // Add your template data here\n}'
  } catch (error) {
    console.error('Error fetching template:', error)
  } finally {
    isLoading.value = false
  }
}

const saveTemplate = async() => {
  try {
    isLoading.value = true
    let parsedData = {}
    try {
      parsedData = JSON.parse(data.value)
    } catch (e) {
      console.error('Invalid JSON data:', e)
      return
    }

    const templateData = {
      content: code.value,
      data: parsedData
    }
    await updateTemplate(templateId, templateData)
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

    <div class="flex flex-1">
      <div class="w-1/2 p-1 flex flex-col">
        <div class="flex flex-col">
          <CodeEditor
            v-model:content="code"
            v-model:data="data"
            :engine="'jsx'"
          />
          <AppButton @click="saveTemplate" :isLoading="isLoading" class="mt-2">
            Save Template & Generate PDF
          </AppButton>
        </div>
      </div>
      <div class="w-1/2 p-4 flex flex-col">
        <PDFPreview
          ref="pdfPreviewRef"
          :templateId="templateId"

        />
      </div>
    </div>
  </div>
</template>
