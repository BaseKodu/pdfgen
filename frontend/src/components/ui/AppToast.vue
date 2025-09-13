<script setup>
import { useToast } from '../../composables/useToast';

const props = defineProps({
  position: {
    type: String,
    default: 'top-center',
    validator: (value) => [
      'top-start', 'top-center', 'top-end',
      'middle-start', 'middle-center', 'middle-end',
      'bottom-start', 'bottom-center', 'bottom-end'
    ].includes(value)
  }
});

const { toasts, removeToastByIndex } = useToast();

const handleClose = (index) => {
  removeToastByIndex(index);
};

const getPositionClass = () => {
  return props.position
    .split('-')
    .map(segment => `toast-${segment}`)
    .join(' ');
};

const getAlertClass = (type) => {
  const typeMap = {
    'info': 'alert-info',
    'success': 'alert-success',
    'warning': 'alert-warning',
    'error': 'alert-error'
  };
  return typeMap[type] || 'alert-info';
};
</script>

<template>
  <div v-if="toasts.length > 0" :class="['toast', getPositionClass()]">
    <div
      v-for="(toast, index) in toasts"
      :key="toast.id"
      :class="['alert', getAlertClass(toast.type)]"
    >
      <span>{{ toast.text }}</span>
      <button
        v-if="toast.closeable !== false"
        @click="handleClose(index)"
        @keydown.enter="handleClose(index)"
        @keydown.space.prevent="handleClose(index)"
        class="btn btn-sm btn-circle btn-ghost ml-2"
        type="button"
        :aria-label="`Close ${toast.type} notification`"
        role="button"
        tabindex="0"
      >
        <span aria-hidden="true">✕</span>
      </button>
    </div>
  </div>
</template>
