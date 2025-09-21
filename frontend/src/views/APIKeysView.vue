<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">API Keys</h1>
      <p class="text-gray-600">
        Manage your API keys to generate PDFs from external applications
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- API Key Management -->
      <div>
        <APIKeyManager />
      </div>

      <!-- API Documentation -->
      <div>
        <APIKeyDocs />
      </div>
    </div>
  </div>
</template>

<script setup>
import APIKeyManager from '../components/APIKeyManager.vue'
import APIKeyDocs from '../components/APIKeyDocs.vue'
</script>
