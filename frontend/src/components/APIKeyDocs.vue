<template>
  <div class="api-docs">
    <ApiDocsSection
      title="API Documentation"
      description="Use your API key to generate PDFs from external applications"
    >
      <!-- Authentication Section -->
      <div>
        <h4 class="font-semibold text-lg mb-2">Authentication</h4>
        <p class="text-sm mb-2">Include your API key in the Authorization header:</p>
        <AppCodeBlock
          content="Authorization: Bearer YOUR_API_KEY"
          language="http"
        />
      </div>

      <!-- Generate PDF Endpoint -->
      <ApiEndpoint
        method="POST"
        endpoint="/api/v1/external/generate-pdf"
        description="Generate a PDF from a template or raw content"
        :requestExample="generatePdfExample"
        requestTitle="Request Body"
        :curlExample="curlExample"
        curlTitle="cURL Example"
        :responseCodes="responseCodes"
      />

      <!-- List Templates Endpoint -->
      <ApiEndpoint
        method="GET"
        endpoint="/api/v1/external/templates"
        description="Returns all your templates"
        :responseCodes="[
          { code: 200, description: 'Success' },
          { code: 401, description: 'Invalid or missing API key' }
        ]"
      />

      <!-- Get Template Endpoint -->
      <ApiEndpoint
        method="GET"
        endpoint="/api/v1/external/templates/{template_id}"
        description="Get a specific template by ID"
        :responseCodes="[
          { code: 200, description: 'Success' },
          { code: 401, description: 'Invalid or missing API key' },
          { code: 404, description: 'Template not found' }
        ]"
      />
    </ApiDocsSection>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ApiDocsSection from './docs/ApiDocsSection.vue'
import ApiEndpoint from './docs/ApiEndpoint.vue'
import AppCodeBlock from './ui/AppCodeBlock.vue'

const generatePdfExample = computed(() => {
  return `{
  "template_id": "abc123def4",
  "data": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}

// OR generate from raw content:
{
  "content": "<h1>Hello {{name}}</h1>",
  "data": {
    "name": "John Doe"
  },
  "is_jsx": false,
  "is_vue": false
}`
})

const curlExample = computed(() => {
  return `curl -X POST "https://your-domain.com/api/v1/external/generate-pdf" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "template_id": "abc123def4",
    "data": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }' \\
  --output "generated.pdf"`
})

const responseCodes = computed(() => [
  { code: 200, description: 'Success' },
  { code: 401, description: 'Invalid or missing API key' },
  { code: 404, description: 'Template not found' },
  { code: 500, description: 'PDF generation failed' }
])
</script>
