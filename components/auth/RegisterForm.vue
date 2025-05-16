<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useRouter } from 'vue-router'
import AppButton from '~/components/ui/AppButton.vue'
import AppInput from '~/components/ui/AppInput.vue'
import AppCard from '~/components/ui/AppCard.vue'

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
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.message || 'Registration failed'
  }
}
</script>

<template>
    <form class="space-y-4">
        <div class="form-control">
            <AppInput
            v-model="email"
            label="Email"
            placeholder="Email"
            type="email"
            :error="emailError"
            
            />              </div>
        <div class="form-control">
            <AppInput
            v-model="password"
            type="password"
            name="password"
            label="Password"
            placeholder="password"
            :error="passwordError"
            />
        </div>
        <div class="form-control">
            <AppInput
            v-model="confirmPassword"
            type="password"
            name="confirmPassword"
            label="Confirm Password"
            placeholder="Confirm Password"
            :error="confirmPasswordError"
            />
        </div>
        <div class="form-control mt-6">
            <AppButton><slot>Register</slot></AppButton>
        </div>
    </form>
</template>