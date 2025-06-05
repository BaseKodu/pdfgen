import axios from 'axios'

const API_URL = '/api/auth/jwt'

// Store token in memory (you could also use localStorage or cookies)
const TOKEN_KEY = 'auth_token'
let authToken = null

export const setAuthToken = (token) => {
  authToken = token
  if (token) {
    localStorage.setItem(TOKEN_KEY, token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    localStorage.removeItem(TOKEN_KEY)
    delete axios.defaults.headers.common['Authorization']
  }
}

// Initialize token from storage when app loads
const storedToken = localStorage.getItem(TOKEN_KEY)
if (storedToken) {
  setAuthToken(storedToken)
}

export const login = async (credentials) => {
  try {
    console.log("credentials: ", credentials)
    const response = await axios.post(`${API_URL}/login`, credentials)
    setAuthToken(response.data.access_token)
    return response.data
  } catch (error) {
    throw error
  }
}

export const logout = () => {
  setAuthToken(null)
}

export const getAuthToken = () => {
  return authToken
}