import { ref, reactive, computed } from 'vue'
import { getAuthToken, setAuthToken } from '../services/auth'
import Cookies from 'js-cookie'
import axios from 'axios'

const API_URL = '/api'

// Cookie configuration for guest status
const GUEST_COOKIE = 'is_guest_user'
const COOKIE_OPTIONS = {
  expires: 7,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict'
}

// Global auth state
const authState = reactive({
  user: null,
  isAuthenticated: false,
  isGuest: false,
  isLoading: false,
  error: null
})

// Initialize auth state from stored data
const initializeAuth = async () => {
  const token = getAuthToken()
  const isGuest = Cookies.get(GUEST_COOKIE) === 'true'

  if (token) {
    authState.isAuthenticated = true
    authState.isGuest = isGuest

    // Try to fetch user info
    try {
      await fetchUserInfo()
    } catch (error) {
      console.warn('Failed to fetch user info on init:', error)
      // If user info fetch fails but we have a token, still consider authenticated
      // but set default user data
      if (authState.isGuest) {
        authState.user = {
          name: 'Guest User',
          email: 'guest@pdfgen.com',
          is_guest: true
        }
      }
    }
  }
}

// Fetch current user information
const fetchUserInfo = async () => {
  try {
    authState.isLoading = true
    authState.error = null

    const response = await axios.get(`${API_URL}/me`)
    authState.user = response.data
    authState.isAuthenticated = true

    return response.data
  } catch (error) {
    authState.error = error.response?.data?.detail || 'Failed to fetch user info'
    throw error
  } finally {
    authState.isLoading = false
  }
}

// Set guest status
const setGuestStatus = (isGuest) => {
  authState.isGuest = isGuest
  if (isGuest) {
    Cookies.set(GUEST_COOKIE, 'true', COOKIE_OPTIONS)
  } else {
    Cookies.remove(GUEST_COOKIE)
  }
}

// Login handler (extends existing auth service)
const handleLoginSuccess = async (userData, isGuest = false) => {
  try {
    authState.isAuthenticated = true
    setGuestStatus(isGuest)

    // Fetch fresh user info from API
    await fetchUserInfo()

    // If it's a guest user and we couldn't fetch user info, set default
    if (isGuest && !authState.user) {
      authState.user = {
        name: 'Guest User',
        email: 'guest@pdfgen.com',
        is_guest: true
      }
    }
  } catch (error) {
    console.warn('Failed to fetch user info after login:', error)
    // Fallback for guest users
    if (isGuest) {
      authState.user = {
        name: 'Guest User',
        email: 'guest@pdfgen.com',
        is_guest: true
      }
      authState.isAuthenticated = true
    }
  }
}

// Logout handler
const handleLogout = () => {
  authState.user = null
  authState.isAuthenticated = false
  authState.isGuest = false
  authState.error = null

  // Clear auth token
  setAuthToken(null)

  // Clear guest status
  Cookies.remove(GUEST_COOKIE)
}

// Auth composable
export function useAuth() {
  // Computed properties for easy access
  const isLoggedIn = computed(() => authState.isAuthenticated)
  const currentUser = computed(() => authState.user)
  const isGuestUser = computed(() => authState.isGuest)
  const isLoadingUser = computed(() => authState.isLoading)
  const authError = computed(() => authState.error)

  // User display helpers
  const userDisplayName = computed(() => {
    if (!authState.user) return 'User'
    if (authState.isGuest) return 'Guest User'
    return authState.user.name || authState.user.email || 'User'
  })

  const userInitials = computed(() => {
    if (authState.isGuest) return 'G'
    const name = authState.user?.name || authState.user?.email || 'User'
    return name.charAt(0).toUpperCase()
  })

  const userEmail = computed(() => {
    if (authState.isGuest) return 'guest@pdfgen.com'
    return authState.user?.email || ''
  })

  // Initialize auth state if not already done
  if (!authState.hasBeenInitialized) {
    authState.hasBeenInitialized = true
    initializeAuth()
  }

  return {
    // State
    user: currentUser,
    isLoggedIn,
    isGuestUser,
    isLoadingUser,
    authError,

    // Computed helpers
    userDisplayName,
    userInitials,
    userEmail,

    // Methods
    fetchUserInfo,
    handleLoginSuccess,
    handleLogout,
    setGuestStatus,

    // Raw state for advanced usage
    authState
  }
}
