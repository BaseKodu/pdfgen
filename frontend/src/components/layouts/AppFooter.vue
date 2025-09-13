<script setup>
import { ref } from 'vue';

const currentYear = ref(new Date().getFullYear());
</script>

<template>
  <footer class="bg-base-100 border-t border-base-300 px-6 py-3">
    <div class="flex items-center justify-between text-sm text-base-content/60">
      <div class="flex items-center space-x-4">
        <span>&copy; {{ currentYear }} pdfGen</span>
        <span>•</span>
        <a href="https://github.com/Basekodu/pdfgen" target="_blank" class="hover:text-base-content transition-colors">
          Open Source
        </a>
      </div>
    </div>
  </footer>
</template>
