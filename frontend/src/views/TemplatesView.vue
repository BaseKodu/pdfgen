<script setup>
import { ref, onMounted } from 'vue';
import AppCard from '../components/ui/AppCard.vue';
import AddNewTemplate from '../components/modals/AddNewTemplate.vue';
import { getTemplates } from '../services/templates';
import { RouterLink } from 'vue-router';

const addNewTemplateModal = ref(null);
const templates = ref([]);

const getUserTemplates = async () => {
  try{
    const response = await getTemplates();
    templates.value = response;
  } catch (error) {
    console.error(error);
  }
}

onMounted(() => {
  getUserTemplates();
});

const showModal = () => {
  addNewTemplateModal.value?.showModal();
};
</script>

<template>
  <div class="p-6">
    <!-- Templates Grid -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold text-base-content">Your Templates</h2>
          <p class="text-base-content/60">Create and manage your PDF templates</p>
        </div>
        <button class="btn btn-primary" @click="showModal">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          New Template
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="templates.length === 0" class="text-center py-12">
        <div class="max-w-md mx-auto">
          <div class="mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-base-content/30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-base-content mb-2">No templates yet</h3>
          <p class="text-base-content/60 mb-6">Create your first PDF template to get started</p>
          <button class="btn btn-primary" @click="showModal">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Create Template
          </button>
        </div>
      </div>

      <!-- Templates Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AppCard
          v-for="template in templates"
          :key="template.id"
          :title="template.name"
          :description="template.description"
          :link="`/templates/${template.id}`"
          class="hover:shadow-lg transition-shadow"
        />
      </div>
    </div>

    <!-- Recent Activity Section -->
    <div class="border-t border-base-300 pt-8">
      <h3 class="text-lg font-semibold text-base-content mb-4">Quick Actions</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="card bg-base-100 border border-base-300 shadow-sm">
          <div class="card-body">
            <h4 class="card-title text-base">📚 Documentation</h4>
            <p class="text-sm text-base-content/60">Learn how to create templates</p>
            <div class="card-actions justify-end">
              <a href="https://github.com/Basekodu/pdfgen" target="_blank" class="btn btn-sm btn-outline">View Docs</a>
            </div>
          </div>
        </div>

        <div class="card bg-base-100 border border-base-300 shadow-sm">
          <div class="card-body">
            <h4 class="card-title text-base">🔗 API Keys</h4>
            <p class="text-sm text-base-content/60">Manage your API access</p>
            <div class="card-actions justify-end">
              <button class="btn btn-sm btn-outline" disabled>Coming Soon</button>
            </div>
          </div>
        </div>

        <div class="card bg-base-100 border border-base-300 shadow-sm">
          <div class="card-body">
            <h4 class="card-title text-base">📊 Usage Stats</h4>
            <p class="text-sm text-base-content/60">Track your PDF generation</p>
            <div class="card-actions justify-end">
              <button class="btn btn-sm btn-outline" disabled>Coming Soon</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <AddNewTemplate ref="addNewTemplateModal" />
  </div>
</template>
