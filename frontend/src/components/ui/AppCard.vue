<script setup>
import { computed } from 'vue';
import { RouterLink } from 'vue-router';
import AppButton from './AppButton.vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    default: null
  },
  // Action configuration
  actionText: {
    type: String,
    default: 'Select'
  },
  actionStyle: {
    type: String,
    default: 'btn-primary'
  },
  // Route for RouterLink
  route: {
    type: String,
    default: null
  },
  // External link
  externalLink: {
    type: String,
    default: null
  },
  // For custom button actions (like guest login)
  isButton: {
    type: Boolean,
    default: false
  },
  // Center content for start options style
  centered: {
    type: Boolean,
    default: false
  },
  // Show action at all
  showAction: {
    type: Boolean,
    default: true
  },
  // Loading state for button
  isLoading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['action']);

const handleButtonClick = () => {
  emit('action');
};

// Extract variant from btn- prefixed style as computed property
const buttonVariant = computed(() => {
  return props.actionStyle?.replace('btn-', '') || 'primary';
});
</script>

<template>
  <div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all hover:-translate-y-1">
    <div class="card-body" :class="{ 'text-center': centered }">
      <div v-if="icon" class="text-4xl mb-4">{{ icon }}</div>
      <h2 class="card-title" :class="{ 'justify-center': centered }">{{ title }}</h2>
      <p :class="centered ? 'text-base-content/70 mb-6' : 'text-base-content/70'">{{ description }}</p>
      <div v-if="showAction" class="card-actions" :class="centered ? 'justify-center' : 'justify-end'">
        <!-- RouterLink for internal routes -->
        <RouterLink
          v-if="route && !isButton"
          :to="route"
          :class="['btn', actionStyle]">
          {{ actionText }}
        </RouterLink>
        <!-- Button for custom actions -->
        <AppButton
          v-else-if="isButton"
          :variant="buttonVariant"
          :is-loading="isLoading"
          @click="handleButtonClick">
          {{ actionText }}
        </AppButton>
        <!-- External link -->
        <a
          v-else-if="externalLink"
          :href="externalLink"
          target="_blank"
          rel="noopener noreferrer"
          :class="['btn', actionStyle]">
          {{ actionText }}
        </a>
      </div>
    </div>
  </div>
</template>
