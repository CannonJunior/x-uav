/**
 * API service for communicating with the backend.
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * Check API health status.
 *
 * @returns {Promise<Object>} Health status object
 */
export async function checkApiHealth() {
  const response = await apiClient.get('/health')
  return response.data
}

/**
 * Get list of UAVs.
 *
 * @param {number} skip - Number of records to skip
 * @param {number} limit - Maximum number of records
 * @returns {Promise<Object>} List of UAVs
 */
export async function getUAVs(skip = 0, limit = 20) {
  const response = await apiClient.get('/api/v1/uavs', {
    params: { skip, limit }
  })
  return response.data
}

/**
 * Get UAV by ID.
 *
 * @param {string} uavId - UAV ID
 * @returns {Promise<Object>} UAV details
 */
export async function getUAV(uavId) {
  const response = await apiClient.get(`/api/v1/uavs/${uavId}`)
  return response.data
}

/**
 * Search UAVs.
 *
 * @param {Object} query - Search query parameters
 * @returns {Promise<Object>} Search results
 */
export async function searchUAVs(query) {
  const response = await apiClient.post('/api/v1/search', query)
  return response.data
}

export default {
  checkApiHealth,
  getUAVs,
  getUAV,
  searchUAVs
}
