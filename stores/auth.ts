import  {defineStore} from 'pinia'
import type { User } from '~/server/services/db';
import { userService } from '~/server/services/UserService'

interface AuthState {
  user: Omit<User, 'password'> | null
  isAuthenticated: boolean
  error: string | null
  loading: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: false,
    error: null,
    loading: false
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated
  },

  actions: {
    async register(userData: { email: string; password: string; name: string }) {
      try {
        this.loading = true
        this.error = null
        
        const user = await userService.register(userData)
        
        if (user) {
          this.user = user
          this.isAuthenticated = true
          
          // Store user ID in local storage for persistence
          localStorage.setItem('userId', user._id || '')
        }
        
        return user
      } catch (error: any) {
        this.error = error.message || 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async login(email: string, password: string) {
      try {
        this.loading = true
        this.error = null
        
        const user = await userService.login(email, password)
        
        if (user) {
          this.user = user
          this.isAuthenticated = true
          
          // Store user ID in local storage for persistence
          localStorage.setItem('userId', user._id || '')
        }
        
        return user
      } catch (error: any) {
        this.error = error.message || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await userService.logout()
        
        // Clear user state
        this.user = null
        this.isAuthenticated = false
        
        // Remove from local storage
        localStorage.removeItem('userId')
      } catch (error: any) {
        this.error = error.message || 'Logout failed'
      }
    },

    async checkAuth() {
      try {
        const userId = localStorage.getItem('userId')
        
        if (!userId) {
          return false
        }
        
        const user = await userService.getUserById(userId)
        
        if (user) {
          this.user = user
          this.isAuthenticated = true
          return true
        } else {
          // Invalid stored ID - clear it
          localStorage.removeItem('userId')
          return false
        }
      } catch (error) {
        return false
      }
    }
  }
})