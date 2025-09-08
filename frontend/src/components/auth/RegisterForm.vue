<script setup>
import { ref } from 'vue'
import { useToast } from '../../composables/useToast'
import AppButton from '../ui/AppButton.vue'
import AppInput from '../ui/AppInput.vue'
import axios from 'axios'

const emit = defineEmits(['registration-success'])
const { showError, showSuccess } = useToast()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const emailError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')

// Add isLoading state
const isLoading = ref(false)

const handleRegister = async () => {
  // Set loading state to true
  isLoading.value = true

  // Clear any previous errors
  emailError.value = '';
  passwordError.value = '';
  confirmPasswordError.value = '';

  // Validate form data
  if (password.value.length < 6) {
    passwordError.value = 'Password must be at least 6 characters'
    showError('Password must be at least 6 characters')
    isLoading.value = false
    return
  }

  if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match'
    showError('Passwords do not match')
    isLoading.value = false
    return
  }

  try {
    const response = await axios.post('/api/auth/register', {
      email: email.value,
      password: password.value,
    });
    console.log('Created:', response.data)
    showSuccess('Registration successful! Please login with your new account.')
    emit('registration-success')
  } catch (err) {
    console.error('Error:', err.response?.data || err.message)
    let errorMessage = 'Registration failed. Please try again.'

    if (err.response?.data?.detail) {
      errorMessage = err.response.data.detail
    } else if (err.response?.data?.message) {
      errorMessage = err.response.data.message
    } else if (err.response?.status === 400) {
      errorMessage = 'Invalid registration data. Please check your inputs.'
    } else if (err.response?.status === 409) {
      errorMessage = 'Email already exists. Please use a different email.'
    }

    showError(errorMessage)
  } finally {
    // Ensure loading state is always set to false when done
    isLoading.value = false
  }
}
</script>

<template>
    <form class="space-y-4" @submit.prevent="handleRegister">
        <div class="form-control">
            <AppInput
            v-model="email"
            label="Email"
            placeholder="Email"
            type="email"
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
        <div class="form-control">
            <AppInput
            v-model="confirmPassword"
            type="password"
            name="confirmPassword"
            label="Confirm Password"
            placeholder="Confirm Password"
            :error="confirmPasswordError"/>
        </div>
        <div class="form-control mt-6">
            <AppButton
              type="submit"
              :isLoading="isLoading">
              <slot>Register</slot>
            </AppButton>
        </div>
    </form>
</template>
