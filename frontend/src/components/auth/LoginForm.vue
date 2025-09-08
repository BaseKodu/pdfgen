<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '../../composables/useToast'
import AppButton from '../ui/AppButton.vue'
import AppInput from '../ui/AppInput.vue'
import { login } from '../../services/auth'

const router = useRouter()
const { showError, showSuccess } = useToast()

const email = ref('')
const password = ref('')

const emailError = ref('')
const passwordError = ref('')

const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  emailError.value = ''
  passwordError.value = ''

  try {
    const response = await login({
      username: email.value,
      password: password.value
    })
    console.log("Login successful")
    console.log(response)
    showSuccess('Login successful! Redirecting...')
    // Redirect to protected route after successful login
    router.push('/templates')
  } catch (err) {
    console.error('Login error:', err)
    // Handle specific error messages from your API
    let errorMessage = 'Invalid credentials'
    if (err.response?.data?.detail) {
      errorMessage = err.response.data.detail
      emailError.value = err.response.data.detail
    } else {
      emailError.value = 'Login failed. Please try again.'
    }
    showError(errorMessage)
  } finally {
    isLoading.value = false
  }
}
</script>


<template>
    <form class="space-y-4" @submit.prevent="handleLogin">
      <div class="form-control">
            <AppInput
            v-model="email"
            label="Email"
            placeholder="Email"
            type="text"
            :error="emailError"/>
        </div>
        <div class="form-control">
            <AppInput
            v-model="password"
            type="password"
            name="password"
            label="Password"
            placeholder="password"
            :error="passwordError"/>
        </div>
        <div class="form-control mt-6">
          <AppButton
              type="submit"
              :isLoading="isLoading">
              <slot>Login</slot>
            </AppButton>
        </div>
    </form>
</template>
