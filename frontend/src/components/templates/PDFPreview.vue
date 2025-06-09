<template>
  <div class="h-full">
    <div v-if="isLoading" class="flex items-center justify-center h-full">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>
    <iframe
      v-else-if="pdfUrl"
      :src="pdfUrl"
      class="w-full h-full border rounded-lg mt-8"
      type="application/pdf"
    ></iframe>
    <div v-else class="flex items-center justify-center h-full text-gray-500">
      Click save to generate PDF preview
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { generatePDF } from '../../services/templates';

const props = defineProps({
  templateId: {
    type: String,
    required: true
  }
});

const pdfUrl = ref(null);
const isLoading = ref(false);

const updatePreview = async () => {
  try {
    isLoading.value = true;
    const response = await generatePDF({
      template_id: props.templateId
    });

    // Create a blob URL from the PDF response
    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    if (pdfUrl.value) {
      URL.revokeObjectURL(pdfUrl.value);
    }
    pdfUrl.value = URL.createObjectURL(blob);
  } catch (error) {
    console.error('Error generating PDF preview:', error);
  } finally {
    isLoading.value = false;
  }
};

// Expose the updatePreview method to parent
defineExpose({ updatePreview });
</script>
