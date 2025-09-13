/**
 * Shared error handling utilities for consistent error messages and user feedback
 */

/**
 * Maps HTTP error codes to user-friendly messages
 */
const ERROR_MESSAGES = {
  400: 'Invalid request data. Please check your input and try again.',
  401: 'You are not authorized. Please log in and try again.',
  403: 'You don\'t have permission to perform this action.',
  404: 'The requested resource was not found.',
  409: 'This action conflicts with the current state. Please refresh and try again.',
  422: 'The data provided is invalid. Please check your input.',
  429: 'Too many requests. Please wait a moment and try again.',
  500: 'Server error occurred. Please try again later.',
  502: 'Service temporarily unavailable. Please try again later.',
  503: 'Service temporarily unavailable. Please try again later.',
  504: 'Request timed out. Please try again later.'
}

/**
 * Handles API errors and returns appropriate user messages
 * @param {Error} error - The error object from the API call
 * @param {string} context - Context of the operation (e.g., 'loading template', 'saving template')
 * @returns {Object} Object with message, type, and shouldRetry properties
 */
export function handleApiError(error, context = 'performing this action') {
  console.error(`Error ${context}:`, error)

  // Check for network connectivity
  if (!navigator.onLine) {
    return {
      message: 'No internet connection. Please check your network and try again.',
      type: 'error',
      shouldRetry: true
    }
  }

  // Handle network errors (no response)
  if (!error.response) {
    return {
      message: `Network error while ${context}. Please check your connection and try again.`,
      type: 'error',
      shouldRetry: true
    }
  }

  const status = error.response.status
  const serverMessage = error.response?.data?.detail || error.response?.data?.message

  // Use server message if available and helpful, otherwise use our predefined messages
  let message = ERROR_MESSAGES[status] || `An error occurred while ${context}. Please try again.`

  // For 400 errors, include server details if available
  if (status === 400 && serverMessage) {
    message = `Validation error: ${serverMessage}`
  }

  return {
    message,
    type: 'error',
    shouldRetry: status >= 500 || status === 429 // Server errors and rate limits are retryable
  }
}

/**
 * Handles template-specific errors with context-aware messages
 * @param {Error} error - The error object
 * @param {string} operation - The operation being performed ('load', 'save', 'delete', etc.)
 * @returns {Object} Error handling result
 */
export function handleTemplateError(error, operation) {
  const baseContext = {
    load: 'loading template',
    save: 'saving template',
    delete: 'deleting template',
    create: 'creating template'
  }[operation] || 'performing template operation'

  const result = handleApiError(error, baseContext)

  // Add operation-specific message overrides
  if (error.response?.status === 404) {
    if (operation === 'load') {
      result.message = 'Template not found. It may have been deleted or you don\'t have permission to access it.'
    } else if (operation === 'save') {
      result.message = 'Template not found. It may have been deleted.'
    }
  }

  if (error.response?.status === 403) {
    if (operation === 'load') {
      result.message = 'You don\'t have permission to access this template.'
    } else if (operation === 'save') {
      result.message = 'You don\'t have permission to edit this template.'
    }
  }

  return result
}

/**
 * Validates JSON string and returns parsed result or error
 * @param {string} jsonString - JSON string to validate
 * @returns {Object} Object with success boolean, data (if successful), or error message
 */
export function validateJson(jsonString) {
  try {
    const parsed = JSON.parse(jsonString)
    return {
      success: true,
      data: parsed
    }
  } catch (error) {
    return {
      success: false,
      message: 'Invalid JSON format. Please check your syntax and try again.',
      details: error.message
    }
  }
}

/**
 * Creates a standardized success message for operations
 * @param {string} operation - The operation that succeeded
 * @param {string} entity - The entity that was operated on (optional)
 * @returns {string} Success message
 */
export function getSuccessMessage(operation, entity = '') {
  const messages = {
    save: `${entity ? entity + ' ' : ''}saved successfully!`,
    load: `${entity ? entity + ' ' : ''}loaded successfully!`,
    create: `${entity ? entity + ' ' : ''}created successfully!`,
    delete: `${entity ? entity + ' ' : ''}deleted successfully!`,
    update: `${entity ? entity + ' ' : ''}updated successfully!`
  }

  return messages[operation] || `${operation} completed successfully!`
}
