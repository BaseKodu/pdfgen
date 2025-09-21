<template>
  <div class="min-h-screen flex items-center justify-center bg-base-100">
    <div class="card w-96 bg-base-200 shadow-xl">
      <div class="card-body text-center">
        <div v-if="isLoading" class="flex flex-col items-center gap-4">
          <span class="loading loading-spinner loading-lg"></span>
          <h2 class="card-title justify-center">Completing login...</h2>
          <p>Please wait while we complete your authentication.</p>
        </div>

        <div v-else-if="error" class="flex flex-col items-center gap-4">
          <div class="text-error text-6xl">⚠️</div>
          <h2 class="card-title text-error justify-center">Login Failed</h2>
          <p class="text-error">{{ error }}</p>
          <div class="card-actions justify-center">
            <router-link to="/login" class="btn btn-primary">
              Try Again
            </router-link>
          </div>
        </div>

        <div v-else class="flex flex-col items-center gap-4">
          <div class="text-success text-6xl">✅</div>
          <h2 class="card-title text-success justify-center">Login Successful!</h2>
          <p>Redirecting you to the application...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { useToast } from '../composables/useToast'
import { setAuthToken } from '../services/auth'

const router = useRouter()
const route = useRoute()
const { handleLoginSuccess } = useAuth()
const { showError } = useToast()

const isLoading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    // Get the token from URL parameters
    const token = route.query.token
    const success = route.query.success

    if (!success || !token) {
      throw new Error('Authentication failed - missing token or success parameter')
    }

    // Store the token using the proper auth service (cookies)
    setAuthToken(token)
    await handleLoginSuccess(null, false) // false = not a guest user

    // Redirect to templates page
    setTimeout(() => {
      router.push('/templates')
    }, 2000)

  } catch (err) {
    console.error('OAuth callback error:', err)
    error.value = err.message || 'Authentication failed'
    showError(error.value)
  } finally {
    isLoading.value = false
  }
})
</script>
