import axios from 'axios'
import { getAuthToken, setAuthToken } from './auth'

const API_URL = '/api'

export const fetchMe = () => axios.get(`${API_URL}/me`)

export const getToken = () => getAuthToken()

export const setToken = (token) => setAuthToken(token)
