import { ref, reactive } from 'vue';

// Global toast state
const toasts = ref([]);

// Toast management composable
export function useToast() {
  const addToast = (text, type = 'info', duration = 5000) => {
    const id = Date.now() + Math.random();
    const toast = { id, text, type };

    toasts.value.push(toast);

    // Auto-remove toast after duration
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }

    return id;
  };

  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id);
    if (index > -1) {
      toasts.value.splice(index, 1);
    }
  };

  const removeToastByIndex = (index) => {
    if (index >= 0 && index < toasts.value.length) {
      toasts.value.splice(index, 1);
    }
  };

  const clearAllToasts = () => {
    toasts.value = [];
  };

  // Convenience methods for different toast types
  const showSuccess = (text, duration = 5000) => addToast(text, 'success', duration);
  const showError = (text, duration = 5000) => addToast(text, 'error', duration);
  const showWarning = (text, duration = 5000) => addToast(text, 'warning', duration);
  const showInfo = (text, duration = 5000) => addToast(text, 'info', duration);

  return {
    toasts,
    addToast,
    removeToast,
    removeToastByIndex,
    clearAllToasts,
    showSuccess,
    showError,
    showWarning,
    showInfo
  };
}
