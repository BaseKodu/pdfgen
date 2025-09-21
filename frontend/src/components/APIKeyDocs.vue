<template>
  <div class="api-docs">
    <div class="card bg-base-200">
      <div class="card-body">
        <h3 class="card-title">API Documentation</h3>
        <p class="text-sm text-gray-600 mb-4">
          Use your API key to generate PDFs from external applications
        </p>

        <div class="space-y-6">
          <!-- Authentication -->
          <div>
            <h4 class="font-semibold text-lg mb-2">Authentication</h4>
            <p class="text-sm mb-2">Include your API key in the Authorization header:</p>
            <div class="bg-gray-100 p-3 rounded font-mono text-sm">
              Authorization: Bearer YOUR_API_KEY
            </div>
          </div>

          <!-- Generate PDF Endpoint -->
          <div>
            <h4 class="font-semibold text-lg mb-2">Generate PDF</h4>
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <span class="badge badge-primary">POST</span>
                <code class="bg-gray-100 px-2 py-1 rounded text-sm">
                  /api/v1/external/generate-pdf
                </code>
              </div>

              <div class="bg-gray-50 p-4 rounded">
                <h5 class="font-medium mb-2">Request Body:</h5>
                <pre class="text-sm overflow-x-auto">{{ generatePdfExample }}</pre>
              </div>

              <div class="bg-gray-50 p-4 rounded">
                <h5 class="font-medium mb-2">cURL Example:</h5>
                <pre class="text-sm overflow-x-auto">{{ curlExample }}</pre>
              </div>
            </div>
          </div>

          <!-- List Templates -->
          <div>
            <h4 class="font-semibold text-lg mb-2">List Templates</h4>
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <span class="badge badge-secondary">GET</span>
                <code class="bg-gray-100 px-2 py-1 rounded text-sm">
                  /api/v1/external/templates
                </code>
              </div>
              <p class="text-sm text-gray-600">Returns all your templates</p>
            </div>
          </div>

          <!-- Get Template -->
          <div>
            <h4 class="font-semibold text-lg mb-2">Get Template</h4>
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <span class="badge badge-secondary">GET</span>
                <code class="bg-gray-100 px-2 py-1 rounded text-sm">
                  /api/v1/external/templates/{template_id}
                </code>
              </div>
              <p class="text-sm text-gray-600">Get a specific template by ID</p>
            </div>
          </div>

          <!-- Response Codes -->
          <div>
            <h4 class="font-semibold text-lg mb-2">Response Codes</h4>
            <div class="space-y-1 text-sm">
              <div class="flex items-center gap-2">
                <span class="badge badge-success">200</span>
                <span>Success</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="badge badge-error">401</span>
                <span>Invalid or missing API key</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="badge badge-error">404</span>
                <span>Template not found</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="badge badge-error">500</span>
                <span>PDF generation failed</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

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
</script>
