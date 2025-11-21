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

        <!-- Column Selector Dropdown -->
        <div class="column-selector">
          <button @click="toggleColumnDropdown" class="btn-secondary column-btn">
            Columns {{ columnDropdownOpen ? '▲' : '▼' }}
          </button>
          <div v-if="columnDropdownOpen" class="column-dropdown">
            <div class="column-dropdown-header">
              <span>Select Columns</span>
              <div class="column-actions">
                <button @click="selectAllColumns" class="btn-small">All</button>
                <button @click="selectDefaultColumns" class="btn-small">Default</button>
              </div>
            </div>
            <div class="column-dropdown-content">
              <div v-for="category in columnCategories" :key="category.name" class="column-category">
                <h4>{{ category.name }}</h4>
                <label v-for="col in category.columns" :key="col.key" class="column-checkbox">
                  <input
                    type="checkbox"
                    :checked="visibleColumns.includes(col.key)"
                    @change="toggleColumn(col.key)"
                  />
                  {{ col.label }}
                </label>
              </div>
            </div>
          </div>
        </div>
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
            <th
              v-for="col in activeColumns"
              :key="col.key"
              @click="col.sortable ? sort(col.key) : null"
              :class="{ sortable: col.sortable }"
            >
              {{ col.label }} {{ col.sortable ? getSortIcon(col.key) : '' }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="uav in paginatedUAVs" :key="uav.id" @click="selectUAV(uav)" class="clickable">
            <td
              v-for="col in activeColumns"
              :key="col.key"
              :class="col.class"
            >
              <span v-if="col.key === 'type'" class="badge">{{ uav[col.key] || 'N/A' }}</span>
              <span v-else-if="col.key === 'operational_status'" :class="'status-' + (uav[col.key] || 'unknown').toLowerCase()">
                {{ uav[col.key] || 'Unknown' }}
              </span>
              <span v-else-if="col.format === 'currency'">{{ formatCurrency(uav[col.key]) }}</span>
              <span v-else-if="col.format === 'number'">{{ formatNumber(uav[col.key]) }}</span>
              <span v-else-if="col.format === 'array'">{{ formatArray(uav[col.key]) }}</span>
              <span v-else-if="col.format === 'boolean'">{{ uav[col.key] ? 'Yes' : 'No' }}</span>
              <span v-else>{{ uav[col.key] || 'N/A' }}</span>
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

// All available columns organized by category
const allColumnDefinitions = [
  // Identification
  { key: 'designation', label: 'Designation', sortable: true, category: 'Identification', class: 'designation' },
  { key: 'name', label: 'Name', sortable: true, category: 'Identification' },
  { key: 'manufacturer', label: 'Manufacturer', sortable: true, category: 'Identification' },
  { key: 'country_of_origin', label: 'Country', sortable: true, category: 'Identification' },
  { key: 'nato_class', label: 'NATO Class', sortable: true, category: 'Identification' },
  { key: 'type', label: 'Type', sortable: true, category: 'Identification' },
  { key: 'operational_status', label: 'Status', sortable: true, category: 'Identification' },
  { key: 'airframe_type', label: 'Airframe', sortable: true, category: 'Identification' },

  // Physical Dimensions
  { key: 'wingspan_meters', label: 'Wingspan (m)', sortable: true, category: 'Physical', class: 'numeric', format: 'number' },
  { key: 'wingspan_feet', label: 'Wingspan (ft)', sortable: true, category: 'Physical', class: 'numeric', format: 'number' },
  { key: 'length_meters', label: 'Length (m)', sortable: true, category: 'Physical', class: 'numeric', format: 'number' },
  { key: 'length_feet', label: 'Length (ft)', sortable: true, category: 'Physical', class: 'numeric', format: 'number' },
  { key: 'height_meters', label: 'Height (m)', sortable: true, category: 'Physical', class: 'numeric', format: 'number' },
  { key: 'height_feet', label: 'Height (ft)', sortable: true, category: 'Physical', class: 'numeric', format: 'number' },

  // Weight
  { key: 'empty_weight_kg', label: 'Empty Wt (kg)', sortable: true, category: 'Weight', class: 'numeric', format: 'number' },
  { key: 'empty_weight_lbs', label: 'Empty Wt (lbs)', sortable: true, category: 'Weight', class: 'numeric', format: 'number' },
  { key: 'max_takeoff_weight_kg', label: 'MTOW (kg)', sortable: true, category: 'Weight', class: 'numeric', format: 'number' },
  { key: 'max_takeoff_weight_lbs', label: 'MTOW (lbs)', sortable: true, category: 'Weight', class: 'numeric', format: 'number' },
  { key: 'payload_capacity_kg', label: 'Payload (kg)', sortable: true, category: 'Weight', class: 'numeric', format: 'number' },
  { key: 'payload_capacity_lbs', label: 'Payload (lbs)', sortable: true, category: 'Weight', class: 'numeric', format: 'number' },
  { key: 'fuel_capacity_kg', label: 'Fuel (kg)', sortable: true, category: 'Weight', class: 'numeric', format: 'number' },

  // Propulsion
  { key: 'engine_type', label: 'Engine Type', sortable: true, category: 'Propulsion' },
  { key: 'engine_manufacturer', label: 'Engine Mfr', sortable: true, category: 'Propulsion' },
  { key: 'engine_model', label: 'Engine Model', sortable: true, category: 'Propulsion' },
  { key: 'thrust_hp', label: 'Thrust (HP)', sortable: true, category: 'Propulsion', class: 'numeric', format: 'number' },
  { key: 'thrust_lbs', label: 'Thrust (lbs)', sortable: true, category: 'Propulsion', class: 'numeric', format: 'number' },
  { key: 'number_of_engines', label: 'Engines', sortable: true, category: 'Propulsion', class: 'numeric' },

  // Performance
  { key: 'cruise_speed_kmh', label: 'Cruise (km/h)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'cruise_speed_mph', label: 'Cruise (mph)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'cruise_speed_knots', label: 'Cruise (kts)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'max_speed_kmh', label: 'Max Speed (km/h)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'max_speed_mach', label: 'Max Speed (Mach)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'service_ceiling_meters', label: 'Ceiling (m)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'service_ceiling_feet', label: 'Ceiling (ft)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'range_km', label: 'Range (km)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'range_miles', label: 'Range (mi)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'range_nm', label: 'Range (nm)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'endurance_hours', label: 'Endurance (h)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },
  { key: 'combat_radius_km', label: 'Combat Radius (km)', sortable: true, category: 'Performance', class: 'numeric', format: 'number' },

  // Mission & Armament
  { key: 'primary_function', label: 'Primary Function', sortable: false, category: 'Mission' },
  { key: 'mission_types', label: 'Mission Types', sortable: false, category: 'Mission', format: 'array' },
  { key: 'armament', label: 'Armament', sortable: false, category: 'Mission', format: 'array' },
  { key: 'hardpoints', label: 'Hardpoints', sortable: true, category: 'Mission', class: 'numeric' },
  { key: 'internal_weapons_bays', label: 'Internal Bay', sortable: true, category: 'Mission', format: 'boolean' },
  { key: 'max_weapons_load_kg', label: 'Weapons Load (kg)', sortable: true, category: 'Mission', class: 'numeric', format: 'number' },

  // Sensors & Stealth
  { key: 'sensor_suite', label: 'Sensors', sortable: false, category: 'Systems', format: 'array' },
  { key: 'radar_type', label: 'Radar', sortable: true, category: 'Systems' },
  { key: 'stealth_features', label: 'Stealth Features', sortable: false, category: 'Systems' },
  { key: 'autonomy_level', label: 'Autonomy', sortable: true, category: 'Systems' },
  { key: 'datalink_type', label: 'Datalink', sortable: true, category: 'Systems' },

  // Operational
  { key: 'operators', label: 'Operators', sortable: false, category: 'Operational', format: 'array' },
  { key: 'crew_size_remote', label: 'Crew Size', sortable: true, category: 'Operational', class: 'numeric' },
  { key: 'launch_method', label: 'Launch Method', sortable: true, category: 'Operational' },
  { key: 'recovery_method', label: 'Recovery Method', sortable: true, category: 'Operational' },
  { key: 'total_units_produced', label: 'Units Produced', sortable: true, category: 'Operational', class: 'numeric', format: 'number' },

  // Economics
  { key: 'unit_cost_usd', label: 'Unit Cost', sortable: true, category: 'Economics', class: 'numeric', format: 'currency' },
  { key: 'program_cost_usd', label: 'Program Cost', sortable: true, category: 'Economics', class: 'numeric', format: 'currency' },
  { key: 'fiscal_year', label: 'Fiscal Year', sortable: true, category: 'Economics', class: 'numeric' },
]

// Default visible columns
const defaultColumns = ['designation', 'name', 'country_of_origin', 'type', 'wingspan_meters', 'endurance_hours', 'range_km', 'unit_cost_usd', 'operational_status']

export default {
  name: 'UAVList',
  setup() {
    const uavs = ref([])
    const countries = ref([])
    const types = ref([])
    const loading = ref(true)
    const error = ref(null)
    const selectedUAV = ref(null)

    // Column selector
    const columnDropdownOpen = ref(false)
    const visibleColumns = ref([...defaultColumns])

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

    // Column categories for dropdown
    const columnCategories = computed(() => {
      const categories = {}
      allColumnDefinitions.forEach(col => {
        if (!categories[col.category]) {
          categories[col.category] = { name: col.category, columns: [] }
        }
        categories[col.category].columns.push(col)
      })
      return Object.values(categories)
    })

    // Active columns based on selection
    const activeColumns = computed(() => {
      return allColumnDefinitions.filter(col => visibleColumns.value.includes(col.key))
    })

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

    const formatArray = (value) => {
      if (!value || !Array.isArray(value)) return 'N/A'
      return value.slice(0, 3).join(', ') + (value.length > 3 ? '...' : '')
    }

    // Column selector functions
    const toggleColumnDropdown = () => {
      columnDropdownOpen.value = !columnDropdownOpen.value
    }

    const toggleColumn = (key) => {
      const index = visibleColumns.value.indexOf(key)
      if (index === -1) {
        visibleColumns.value.push(key)
      } else {
        visibleColumns.value.splice(index, 1)
      }
    }

    const selectAllColumns = () => {
      visibleColumns.value = allColumnDefinitions.map(col => col.key)
    }

    const selectDefaultColumns = () => {
      visibleColumns.value = [...defaultColumns]
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
      columnDropdownOpen,
      visibleColumns,
      columnCategories,
      activeColumns,
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
      formatCurrency,
      formatArray,
      toggleColumnDropdown,
      toggleColumn,
      selectAllColumns,
      selectDefaultColumns
    }
  }
}
</script>
