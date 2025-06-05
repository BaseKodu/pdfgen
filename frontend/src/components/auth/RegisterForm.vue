<script setup>
import { ref } from 'vue'
import AppButton from '../ui/AppButton.vue'
import AppInput from '../ui/AppInput.vue'
import axios from 'axios'

const emit = defineEmits(['registration-success'])


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
    isLoading.value = false
    return
  }

  if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match'
    isLoading.value = false
    return
  }

  try {
    const response = await axios.post('/api/auth/register', {
      email: email.value,
      password: password.value,
    });
    console.log('Created:', response.data)
    emit('registration-success')
  } catch (err) {
    console.error('Error:', err.response?.data || err.message)
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