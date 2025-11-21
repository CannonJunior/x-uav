/**
 * API service for X-UAV backend communication.
 *
 * Provides methods to interact with the FastAPI backend.
 */

import axios from 'axios'

const API_BASE_URL = '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  /**
   * Get health status.
   *
   * @returns {Promise} Health status
   */
  getHealth() {
    return apiClient.get('/health')
  },

  /**
   * Get database statistics.
   *
   * @returns {Promise} Database statistics
   */
  getStats() {
    return apiClient.get('/stats')
  },

  /**
   * Get all UAVs.
   *
   * @returns {Promise} List of all UAVs
   */
  getAllUAVs() {
    return apiClient.get('/uavs')
  },

  /**
   * Get specific UAV by designation.
   *
   * @param {string} designation - UAV designation (e.g., "MQ-9")
   * @returns {Promise} UAV details
   */
  getUAV(designation) {
    return apiClient.get(`/uavs/${designation}`)
  },

  /**
   * Compare multiple UAVs.
   *
   * @param {Array<string>} designations - List of UAV designations
   * @returns {Promise} Comparison data
   */
  compareUAVs(designations) {
    return apiClient.post('/uavs/compare', { designations })
  },

  /**
   * Search UAVs with filters.
   *
   * @param {Object} filters - Search filters
   * @param {string} filters.country - Filter by country
   * @param {string} filters.type - Filter by UAV type
   * @param {string} filters.status - Filter by operational status
   * @param {string} filters.nato_class - Filter by NATO class
   * @returns {Promise} Filtered UAVs
   */
  searchUAVs(filters) {
    return apiClient.post('/uavs/search', filters)
  },

  /**
   * Get list of countries.
   *
   * @returns {Promise} List of countries
   */
  getCountries() {
    return apiClient.get('/filters/countries')
  },

  /**
   * Get list of UAV types.
   *
   * @returns {Promise} List of UAV types
   */
  getTypes() {
    return apiClient.get('/filters/types')
  },
}
