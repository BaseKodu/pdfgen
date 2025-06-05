import axios from 'axios'

const API_URL = '/api'

export const addNewTemplate = async (data) => {
  try {
    console.log("data: ", data)
    const response = await axios.post(`${API_URL}/templates`, data)
    return response.data
  } catch (error) {
    throw error
  }
}

export const updateTemplate = async (id, data) => {
  try {
    const response = await axios.patch(`${API_URL}/templates/${id}`, data)
    return response.data
  } catch (error) {
    throw error
  }
}

export const getTemplate = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/templates/${id}`)
    return response.data
  } catch (error) {
    throw error
  }
}


export const getTemplates = async () => {
  try {
    const response = await axios.get(`${API_URL}/templates`)
    return response.data
  } catch (error) {
    throw error
  }
}
