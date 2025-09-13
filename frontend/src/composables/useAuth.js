import { reactive, computed } from 'vue'
import { fetchMe, getToken, setToken } from '../services/authService'
import { getGuestFlag, setGuestFlag } from '../services/authCookies'
import { defaultGuestUser } from '../services/guestUser'

// Global auth state
const state = reactive({
  user: null,
  isAuthenticated: false,
  isGuest: false,
  isLoading: false,
  error: null,
  initialized: false
})

// Initialize auth state from stored data
async function initializeAuth() {
  const token = getToken()
  state.isGuest = getGuestFlag()

  if (!token) return

  state.isAuthenticated = true
  try {
    const { data } = await fetchMe()
    state.user = data
  } catch (error) {
    console.warn('Failed to fetch user info on init:', error)
    // If user info fetch fails but we have a token, still consider authenticated
    // but set default user data for guest users
    if (state.isGuest) {
      state.user = defaultGuestUser()
    }
  }
}

// Fetch current user information
const fetchUserInfo = async () => {
  try {
    state.isLoading = true
    state.error = null

    const { data } = await fetchMe()
    state.user = data
    state.isAuthenticated = true

    return data
  } catch (error) {
    state.error = error.response?.data?.detail || 'Failed to fetch user info'
    throw error
  } finally {
    state.isLoading = false
  }
}

// Login handler (extends existing auth service)
async function handleLoginSuccess(userData, isGuest = false) {
  try {
    state.isAuthenticated = true
    setGuestFlag(isGuest)
    state.isGuest = isGuest

    // Fetch fresh user info from API
    try {
      const { data } = await fetchMe()
      state.user = data
    } catch (error) {
      console.warn('Failed to fetch user info after login:', error)
      // Fallback for guest users
      if (isGuest) {
        state.user = defaultGuestUser()
      }
    }
  } catch (error) {
    console.warn('Login success handler error:', error)
    // Fallback for guest users
    if (isGuest) {
      state.user = defaultGuestUser()
      state.isAuthenticated = true
    }
  }
}

// Logout handler
function handleLogout() {
  state.user = null
  state.isAuthenticated = false
  state.isGuest = false
  state.error = null

  // Clear auth token
  setToken(null)

  // Clear guest status
  setGuestFlag(false)
}

// Auth composable
export function useAuth() {
  // Initialize auth state if not already done
  if (!state.initialized) {
    state.initialized = true
    initializeAuth()
  }

  // Computed properties for easy access
  const isLoggedIn = computed(() => state.isAuthenticated)
  const currentUser = computed(() => state.user)
  const isGuestUser = computed(() => state.isGuest)
  const isLoadingUser = computed(() => state.isLoading)
  const authError = computed(() => state.error)

  // User display helpers
  const userDisplayName = computed(() => {
    if (!state.user) return 'User'
    if (state.isGuest) return 'Guest User'
    return state.user.name || state.user.email || 'User'
  })

  const userInitials = computed(() => {
    if (state.isGuest) return 'G'
    const name = state.user?.name || state.user?.email || 'User'
    return name.charAt(0).toUpperCase()
  })

  const userEmail = computed(() => {
    if (state.isGuest) return 'guest@pdfgen.com'
    return state.user?.email || ''
  })

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
    setGuestStatus: setGuestFlag,

    // Raw state for advanced usage
    authState: state
  }
}
