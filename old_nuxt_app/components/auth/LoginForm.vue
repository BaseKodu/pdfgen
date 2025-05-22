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
  email: '',
  password: '',
})

const error = ref('')
const loading = computed(() => authStore.loading)



const handleLogin = async () => {
  // Clear any previous errors
  error.value = ''
  
  try {
    await authStore.login({
      email: form.value.email,
      password: form.value.password
    })
    
    // Registration successful, navigate to dashboard
    router.push('/templates')
  } catch (err: any) {
    error.value = err.message || 'Registration failed'
    console.error('Login error:', error.value)
  }
}
</script>

<template>
    <form class="space-y-4" @submit.prevent="handleLogin">
        <div class="form-control">
            <AppInput
                v-model="form.email"
                label="Email"
                placeholder="Email"
                type="email"
                
            />
        </div>
        <div class="form-control">
            <AppInput 
                v-model="form.password"
                type="password"
                name="password"
                label="Password"
                placeholder="password"
                
                />
        </div>
        <div class="form-control mt-6">
            <AppButton 
                type="submit" 
                @click="handleLogin"><slot>Login</slot></AppButton>
        </div>
    </form>
</template>