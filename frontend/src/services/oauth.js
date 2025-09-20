import axios from 'axios'

const API_URL = '/api'

/**
 * Get available OAuth providers
 */
export const getOAuthProviders = async () => {
  try {
    const response = await axios.get(`${API_URL}/auth/oauth/providers`)
    return response.data
  } catch (error) {
    console.error('Failed to get OAuth providers:', error)
    throw error
  }
}

/**
 * Initiate Google OAuth flow
 */
export const initiateGoogleOAuth = async () => {
  try {
    const response = await axios.get(`${API_URL}/auth/oauth/google/authorize`)
    return response.data.authorization_url
  } catch (error) {
    console.error('Failed to initiate Google OAuth:', error)
    throw error
  }
}

/**
 * Initiate OAuth flow for any provider
 */
export const initiateOAuth = async (provider) => {
  try {
    const response = await axios.get(`${API_URL}/auth/oauth/${provider}/authorize`)
    return response.data.authorization_url
  } catch (error) {
    console.error(`Failed to initiate ${provider} OAuth:`, error)
    throw error
  }
}

/**
 * Associate OAuth account with existing user
 */
export const associateOAuthAccount = async (provider) => {
  try {
    const response = await axios.get(`${API_URL}/auth/oauth/${provider}/associate/authorize`)
    return response.data.authorization_url
  } catch (error) {
    console.error(`Failed to associate ${provider} account:`, error)
    throw error
  }
}

/**
 * Disconnect OAuth account
 */
export const disconnectOAuthAccount = async (provider) => {
  try {
    const response = await axios.delete(`${API_URL}/auth/oauth/${provider}/disconnect`)
    return response.data
  } catch (error) {
    console.error(`Failed to disconnect ${provider} account:`, error)
    throw error
  }
}
