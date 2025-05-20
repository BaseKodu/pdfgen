<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import AuthView from '../components/auth/AuthView.vue'
import { navigateTo } from 'nuxt/app'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const error = ref('')
const loading = computed(() => authStore.loading)

const handleRegister = async () => {
  // Clear any previous errors
  error.value = ''
  
  // Validate form data
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }
  
  if (form.value.password.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }
  
  try {
    await authStore.register({
      name: form.value.name,
      email: form.value.email,
      password: form.value.password
    })
    
    // Registration successful, navigate to dashboard
   navigateTo("/dashboard")
  } catch (err: any) {
    error.value = err.message || 'Registration failed'
  }
}
</script>
<template>
  <AuthView />
</template>