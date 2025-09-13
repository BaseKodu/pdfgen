import axios from 'axios'
import Cookies from 'js-cookie'

const API_URL = '/api'

// Cookie configuration
const TOKEN_COOKIE = 'auth_token'
const COOKIE_OPTIONS = {
  expires: 7, // Token expires in 7 days
  secure: process.env.NODE_ENV === 'production', // Use secure cookies in production
  sameSite: 'strict' // Protect against CSRF
}

export const setAuthToken = (token) => {
  if (token) {
    // Store token in cookie
    Cookies.set(TOKEN_COOKIE, token, COOKIE_OPTIONS)
    // Set axios default header
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    // Remove token from cookie
    Cookies.remove(TOKEN_COOKIE)
    // Remove axios default header
    delete axios.defaults.headers.common['Authorization']
  }
}

// Initialize token from cookie when app loads
const storedToken = Cookies.get(TOKEN_COOKIE)
if (storedToken) {
  setAuthToken(storedToken)
}

export const login = async (credentials) => {
  try {
    // Create URLSearchParams object for form-urlencoded data
    const formData = new URLSearchParams({
      username: credentials.username,
      password: credentials.password,
      grant_type: '',  // Optional fields as shown in curl example
      scope: '',
      client_id: '',
      client_secret: ''
    })

    const response = await axios.post(`${API_URL}/auth/jwt/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    // Store both the access token and token type
    const { access_token, token_type } = response.data
    setAuthToken(access_token)

    return response.data
  } catch (error) {
    throw error
  }
}

export const loginAsGuest = async () => {
  try {
    // Create guest user
    const guestResponse = await axios.post(`${API_URL}/guest`)

    // Login with guest credentials
    const loginResponse = await login({
      username: guestResponse.data.email,
      password: guestResponse.data.password
    })

    // Return both login response and guest info
    return {
      ...loginResponse,
      isGuest: true,
      guestUserData: guestResponse.data
    }
  } catch (error) {
    console.error('Guest login error:', error)
    throw error
  }
}

export const logout = () => {
  setAuthToken(null)
}

export const getAuthToken = () => {
  return Cookies.get(TOKEN_COOKIE)
}
