<script setup>
import { ref, onMounted } from 'vue';
import AppNavbar from '../components/ui/AppNavbar.vue';
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
  <div class="flex flex-col min-h-screen">
    <AppNavbar />
    <div class="p-4">
      <div class="flex items-end mb-6">
        <h1 class="text-2xl font-bold">New Template</h1>
        <button class="btn btn-primary btn-circle" @click="showModal">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>
    </div>

    <div class="container mx-auto p-4">
      <section v-for="template in templates" :key="template.id">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mx-auto">
          <AppCard :title="template.name" :description="template.description" :link="`/templates/${template.id}`" />
        </div>
      </section>
    </div>

    <AddNewTemplate ref="addNewTemplateModal" />
  </div>
</template>