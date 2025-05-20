import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip middleware if going to auth pages
  if (to.path === '/login' || to.path === '/register') {
    return
  }

  const authStore = useAuthStore()
  const isAuthenticated = await authStore.checkAuth()

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return navigateTo('/login')
  }
})