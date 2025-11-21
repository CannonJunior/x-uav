<template>
  <div class="uav-list">
    <div class="controls">
      <h2>UAV Database</h2>

      <div class="filters">
        <div class="filter-group">
          <label for="country-filter">Country:</label>
          <select id="country-filter" v-model="filters.country" @change="applyFilters">
            <option value="">All Countries</option>
            <option v-for="country in countries" :key="country" :value="country">
              {{ country }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label for="type-filter">Type:</label>
          <select id="type-filter" v-model="filters.type" @change="applyFilters">
            <option value="">All Types</option>
            <option v-for="type in types" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label for="search">Search:</label>
          <input
            id="search"
            type="text"
            v-model="searchQuery"
            placeholder="Search by name or designation..."
            @input="filterUAVs"
          />
        </div>

        <button @click="clearFilters" class="btn-secondary">Clear Filters</button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading UAV data...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>Error loading UAVs: {{ error }}</p>
      <button @click="loadUAVs" class="btn-primary">Retry</button>
    </div>

    <div v-else class="table-container">
      <p class="results-count">Showing {{ filteredUAVs.length }} of {{ totalUAVs }} UAVs</p>

      <table class="uav-table">
        <thead>
          <tr>
            <th @click="sort('designation')" class="sortable">
              Designation {{ getSortIcon('designation') }}
            </th>
            <th @click="sort('name')" class="sortable">
              Name {{ getSortIcon('name') }}
            </th>
            <th @click="sort('country_of_origin')" class="sortable">
              Country {{ getSortIcon('country_of_origin') }}
            </th>
            <th @click="sort('type')" class="sortable">
              Type {{ getSortIcon('type') }}
            </th>
            <th @click="sort('wingspan_meters')" class="sortable">
              Wingspan (m) {{ getSortIcon('wingspan_meters') }}
            </th>
            <th @click="sort('endurance_hours')" class="sortable">
              Endurance (h) {{ getSortIcon('endurance_hours') }}
            </th>
            <th @click="sort('range_km')" class="sortable">
              Range (km) {{ getSortIcon('range_km') }}
            </th>
            <th @click="sort('unit_cost_usd')" class="sortable">
              Unit Cost (USD) {{ getSortIcon('unit_cost_usd') }}
            </th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="uav in paginatedUAVs" :key="uav.id" @click="selectUAV(uav)" class="clickable">
            <td class="designation">{{ uav.designation }}</td>
            <td>{{ uav.name || 'N/A' }}</td>
            <td>{{ uav.country_of_origin || 'N/A' }}</td>
            <td><span class="badge">{{ uav.type || 'N/A' }}</span></td>
            <td class="numeric">{{ formatNumber(uav.wingspan_meters) }}</td>
            <td class="numeric">{{ formatNumber(uav.endurance_hours) }}</td>
            <td class="numeric">{{ formatNumber(uav.range_km) }}</td>
            <td class="numeric">{{ formatCurrency(uav.unit_cost_usd) }}</td>
            <td>
              <span :class="'status-' + (uav.operational_status || 'unknown').toLowerCase()">
                {{ uav.operational_status || 'Unknown' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredUAVs.length > itemsPerPage" class="pagination">
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
          class="btn-secondary"
        >
          Previous
        </button>
        <span class="page-info">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="btn-secondary"
        >
          Next
        </button>
      </div>
    </div>

    <!-- UAV Detail Modal -->
    <div v-if="selectedUAV" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <span class="close" @click="closeModal">&times;</span>
        <h2>{{ selectedUAV.designation }} - {{ selectedUAV.name }}</h2>

        <div class="uav-details">
          <div class="detail-section">
            <h3>General Information</h3>
            <dl>
              <dt>Manufacturer:</dt>
              <dd>{{ selectedUAV.manufacturer || 'N/A' }}</dd>
              <dt>Country:</dt>
              <dd>{{ selectedUAV.country_of_origin || 'N/A' }}</dd>
              <dt>Type:</dt>
              <dd>{{ selectedUAV.type || 'N/A' }}</dd>
              <dt>NATO Class:</dt>
              <dd>{{ selectedUAV.nato_class || 'N/A' }}</dd>
              <dt>Status:</dt>
              <dd>{{ selectedUAV.operational_status || 'N/A' }}</dd>
            </dl>
          </div>

          <div class="detail-section">
            <h3>Physical Characteristics</h3>
            <dl>
              <dt>Wingspan:</dt>
              <dd>{{ formatNumber(selectedUAV.wingspan_meters) }}m / {{ formatNumber(selectedUAV.wingspan_feet) }}ft</dd>
              <dt>Length:</dt>
              <dd>{{ formatNumber(selectedUAV.length_meters) }}m / {{ formatNumber(selectedUAV.length_feet) }}ft</dd>
              <dt>Height:</dt>
              <dd>{{ formatNumber(selectedUAV.height_meters) }}m / {{ formatNumber(selectedUAV.height_feet) }}ft</dd>
              <dt>Empty Weight:</dt>
              <dd>{{ formatNumber(selectedUAV.empty_weight_kg) }}kg / {{ formatNumber(selectedUAV.empty_weight_lbs) }}lbs</dd>
              <dt>Max Takeoff Weight:</dt>
              <dd>{{ formatNumber(selectedUAV.max_takeoff_weight_kg) }}kg / {{ formatNumber(selectedUAV.max_takeoff_weight_lbs) }}lbs</dd>
            </dl>
          </div>

          <div class="detail-section">
            <h3>Performance</h3>
            <dl>
              <dt>Endurance:</dt>
              <dd>{{ formatNumber(selectedUAV.endurance_hours) }} hours</dd>
              <dt>Range:</dt>
              <dd>{{ formatNumber(selectedUAV.range_km) }}km / {{ formatNumber(selectedUAV.range_miles) }}mi</dd>
              <dt>Cruise Speed:</dt>
              <dd>{{ formatNumber(selectedUAV.cruise_speed_kmh) }}km/h / {{ formatNumber(selectedUAV.cruise_speed_mph) }}mph</dd>
              <dt>Service Ceiling:</dt>
              <dd>{{ formatNumber(selectedUAV.service_ceiling_meters) }}m / {{ formatNumber(selectedUAV.service_ceiling_feet) }}ft</dd>
            </dl>
          </div>

          <div class="detail-section" v-if="selectedUAV.primary_function">
            <h3>Mission</h3>
            <dl>
              <dt>Primary Function:</dt>
              <dd>{{ selectedUAV.primary_function }}</dd>
              <dt>Mission Types:</dt>
              <dd>{{ selectedUAV.mission_types ? selectedUAV.mission_types.join(', ') : 'N/A' }}</dd>
              <dt>Armament:</dt>
              <dd>{{ selectedUAV.armament ? selectedUAV.armament.join(', ') : 'N/A' }}</dd>
            </dl>
          </div>

          <div class="detail-section" v-if="selectedUAV.unit_cost_usd">
            <h3>Economics</h3>
            <dl>
              <dt>Unit Cost:</dt>
              <dd>{{ formatCurrency(selectedUAV.unit_cost_usd) }}</dd>
              <dt>Fiscal Year:</dt>
              <dd>{{ selectedUAV.fiscal_year || 'N/A' }}</dd>
            </dl>
          </div>

          <div class="detail-section" v-if="selectedUAV.notes">
            <h3>Notes</h3>
            <p>{{ selectedUAV.notes }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api.js'

export default {
  name: 'UAVList',
  setup() {
    const uavs = ref([])
    const countries = ref([])
    const types = ref([])
    const loading = ref(true)
    const error = ref(null)
    const selectedUAV = ref(null)

    // Filters
    const filters = ref({
      country: '',
      type: '',
      status: ''
    })
    const searchQuery = ref('')

    // Sorting
    const sortKey = ref('designation')
    const sortOrder = ref('asc')

    // Pagination
    const currentPage = ref(1)
    const itemsPerPage = ref(20)

    const totalUAVs = computed(() => uavs.value.length)

    const filteredUAVs = computed(() => {
      let result = [...uavs.value]

      // Apply search
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(uav =>
          (uav.designation && uav.designation.toLowerCase().includes(query)) ||
          (uav.name && uav.name.toLowerCase().includes(query)) ||
          (uav.manufacturer && uav.manufacturer.toLowerCase().includes(query))
        )
      }

      // Apply sorting
      result.sort((a, b) => {
        let aVal = a[sortKey.value]
        let bVal = b[sortKey.value]

        // Handle null/undefined
        if (aVal == null) return 1
        if (bVal == null) return -1

        // Numeric comparison
        if (typeof aVal === 'number' && typeof bVal === 'number') {
          return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal
        }

        // String comparison
        aVal = String(aVal).toLowerCase()
        bVal = String(bVal).toLowerCase()

        if (sortOrder.value === 'asc') {
          return aVal < bVal ? -1 : aVal > bVal ? 1 : 0
        } else {
          return aVal > bVal ? -1 : aVal < bVal ? 1 : 0
        }
      })

      return result
    })

    const totalPages = computed(() =>
      Math.ceil(filteredUAVs.value.length / itemsPerPage.value)
    )

    const paginatedUAVs = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredUAVs.value.slice(start, end)
    })

    const loadUAVs = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await api.getAllUAVs()
        uavs.value = response.data.uavs
      } catch (err) {
        error.value = err.message
        console.error('Error loading UAVs:', err)
      } finally {
        loading.value = false
      }
    }

    const loadFilters = async () => {
      try {
        const [countriesRes, typesRes] = await Promise.all([
          api.getCountries(),
          api.getTypes()
        ])
        countries.value = countriesRes.data
        types.value = typesRes.data
      } catch (err) {
        console.error('Error loading filters:', err)
      }
    }

    const applyFilters = async () => {
      try {
        loading.value = true
        const response = await api.searchUAVs(filters.value)
        uavs.value = response.data.uavs
        currentPage.value = 1
      } catch (err) {
        error.value = err.message
        console.error('Error applying filters:', err)
      } finally {
        loading.value = false
      }
    }

    const clearFilters = () => {
      filters.value = { country: '', type: '', status: '' }
      searchQuery.value = ''
      loadUAVs()
    }

    const filterUAVs = () => {
      currentPage.value = 1
    }

    const sort = (key) => {
      if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortKey.value = key
        sortOrder.value = 'asc'
      }
    }

    const getSortIcon = (key) => {
      if (sortKey.value !== key) return ''
      return sortOrder.value === 'asc' ? '▲' : '▼'
    }

    const selectUAV = (uav) => {
      selectedUAV.value = uav
    }

    const closeModal = () => {
      selectedUAV.value = null
    }

    const previousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
      }
    }

    const formatNumber = (value) => {
      if (value == null) return 'N/A'
      return value.toLocaleString('en-US', { maximumFractionDigits: 1 })
    }

    const formatCurrency = (value) => {
      if (value == null) return 'N/A'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value)
    }

    onMounted(() => {
      loadUAVs()
      loadFilters()
    })

    return {
      uavs,
      countries,
      types,
      loading,
      error,
      selectedUAV,
      filters,
      searchQuery,
      sortKey,
      sortOrder,
      currentPage,
      itemsPerPage,
      totalUAVs,
      filteredUAVs,
      totalPages,
      paginatedUAVs,
      loadUAVs,
      applyFilters,
      clearFilters,
      filterUAVs,
      sort,
      getSortIcon,
      selectUAV,
      closeModal,
      previousPage,
      nextPage,
      formatNumber,
      formatCurrency
    }
  }
}
</script>
