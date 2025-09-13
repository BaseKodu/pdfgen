<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import CodeEditor from '../components/templates/CodeEditor.vue'
import AppButton from '../components/ui/AppButton.vue'
import PDFPreview from '../components/templates/PDFPreview.vue'
import { updateTemplate, getTemplate } from '../services/templates'
import { useToast } from '../composables/useToast'
import { handleTemplateError, validateJson, getSuccessMessage } from '../utils/errorHandler'

const route = useRoute()
const templateId = route.params.id
const pdfPreviewRef = ref(null)
const isLoading = ref(false)
const code = ref('')
const data = ref('{\n  // Add your template data here\n}')
const engine = ref('html')

const { showSuccess, showError, showWarning } = useToast()

const getCurrentTemplate = async() => {
  try {
    isLoading.value = true
    const response = await getTemplate(templateId)
    code.value = response.content
    data.value = response.data ? JSON.stringify(response.data, null, 2) : '{\n  // Add your template data here\n}'
    engine.value = response.engine
    // Only show success message if this is a retry/refresh, not on initial load
    console.log('Template loaded successfully')
  } catch (error) {
    const errorResult = handleTemplateError(error, 'load')
    showError(errorResult.message)
  } finally {
    isLoading.value = false
  }
}

const saveTemplate = async() => {
  try {
    isLoading.value = true

    // Validate JSON data first
    const jsonValidation = validateJson(data.value)
    if (!jsonValidation.success) {
      showError(jsonValidation.message)
      return
    }

    const templateData = {
      content: code.value,
      data: jsonValidation.data
    }

    await updateTemplate(templateId, templateData)
    showSuccess(getSuccessMessage('save', 'Template'))

    // Generate PDF preview after successful save
    try {
      await pdfPreviewRef.value.updatePreview()
    } catch (previewError) {
      console.warn('PDF preview update failed:', previewError)
      showWarning('Template saved, but PDF preview couldn\'t be updated. Please refresh to see changes.')
    }

  } catch (error) {
    const errorResult = handleTemplateError(error, 'save')
    showError(errorResult.message)
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
  <div class="flex flex-1 h-full">
    <!-- Code Editor Panel -->
    <div class="w-1/2 border-r border-base-300 flex flex-col">
      <div class="bg-base-100 border-b border-base-300 p-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold">Template Editor</h3>
            <p class="text-sm text-base-content/60">Edit your template code and data</p>
          </div>
          <div class="flex items-center space-x-2">
            <div class="badge badge-primary">{{ engine }}</div>
            <AppButton @click="saveTemplate" :isLoading="isLoading" size="sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              Save & Generate
            </AppButton>
          </div>
        </div>
      </div>

      <div class="flex-1 p-4 overflow-hidden">
        <CodeEditor
          v-model:content="code"
          v-model:data="data"
          :engine="engine"
          class="h-full"
        />
      </div>
    </div>

    <!-- PDF Preview Panel -->
    <div class="w-1/2 flex flex-col">
      <div class="bg-base-100 border-b border-base-300 p-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold">PDF Preview</h3>
            <p class="text-sm text-base-content/60">Live preview of your PDF output</p>
          </div>
          <div class="flex items-center space-x-2">
            <div class="badge badge-success">Live</div>
          </div>
        </div>
      </div>

      <div class="flex-1 p-4 overflow-hidden bg-base-200">
        <PDFPreview
          ref="pdfPreviewRef"
          :templateId="templateId"
          class="h-full"
        />
      </div>
    </div>
  </div>
</template>
