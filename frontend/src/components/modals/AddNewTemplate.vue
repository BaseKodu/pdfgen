<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import AppButton from '../ui/AppButton.vue'
import AppInput from '../ui/AppInput.vue'
import AppTextArea from '../ui/AppTextArea.vue'
import { addNewTemplate } from '../../services/templates';
import AppSelect from '../ui/AppSelect.vue';

const router = useRouter();

const title = ref('');
const description = ref('');
const isLoading = ref(false);
const selectedEngine = ref('HTML')



defineExpose({
  showModal() {
    document.getElementById('addNewTemplateModal').showModal();
  }

});

const handleSubmit = async() => {
  isLoading.value = true;
  try {
    const response = await addNewTemplate({
      name: title.value,
      //description: description.value,
      engine: selectedEngine.value.toLowerCase(),
      content: "Hello world of templates, have a great time designing your pdf template"
    })

    console.log("Template added successfully")
    router.push(`/templates/${response.id}`)
  } catch (err) {
    console.error('Login error:', err)
    // Handle specific error messages from your API
    if (err.response?.data?.detail) {
      console.log(err.response.data.detail)
    } else {
      console.log('Invalid credentials')
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <dialog id="addNewTemplateModal" class="modal">
    <div class="modal-box">
      <form method="dialog" >
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      </form>
      <h3 class="font-bold text-lg mb-4">Add New Template</h3>

      <form id="newTemplateForm" class="space-y-4">
        <div class="form-control">
          <AppInput v-model="title" label="Template Name" placeholder="Enter template title" />
        </div>

        <div class="form-control">
          <AppTextArea v-model="description" label="Template Description" placeholder="Enter template description" />
        </div>

        <div class="form-control">
          <AppSelect label="Engine" :options="['HTML','VUE','JSX']" v-model="selectedEngine"/>
        </div>

        <div class="modal-action justify-between">
          <AppButton variant="ghost"><slot>Cancel</slot></AppButton>
          <AppButton :isLoading="isLoading" @click="handleSubmit"><slot>Add Template</slot></AppButton>
        </div>
      </form>
    </div>
  </dialog>
</template>


<style scoped>
.textarea-container {
  margin-bottom: 1rem;
  width: 100%;
}

.textarea-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s ease;
  resize: vertical;
  min-height: 100px;
}

.textarea:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.textarea.textarea-error {
  border-color: #e74c3c;
}

.textarea.textarea-error:focus {
  box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.2);
}

.textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  margin-top: 0.5rem;
  color: #e74c3c;
  font-size: 0.875rem;
}

.hint-text {
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.875rem;
}

.character-count {
  margin-top: 0.25rem;
  text-align: right;
  font-size: 0.75rem;
  color: #888;
}
</style>
