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

export const updateTemplate = async (data) => {
  try {
    const response = await axios.put(`${API_URL}/templates/${data.id}`, data)
    return response.data
  } catch (error) {
    throw error
  }
}