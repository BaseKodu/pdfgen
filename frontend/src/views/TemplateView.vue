<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from '../components/ui/AppNavbar.vue'
import CodeEditor from '../components/templates/CodeEditor.vue'

const route = useRoute()
const templateId = route.params.id

</script>

<template>
  <div class="flex flex-col min-h-screen">
    <AppNavbar />

    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold">Template {{ templateId }}</h1>
    </div>

    <div class="flex">
      <div class="w-1/2 p-4">
        <CodeEditor />
      </div>
      <div class="w-1/2 p-4">
        <!-- Right side content can go here -->
      </div>
    </div>
  </div>
</template>
