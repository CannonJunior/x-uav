<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <h1>X-UAV</h1>
        <p class="subtitle">Unmanned Aerial Vehicle Comparison Platform</p>
      </div>
    </header>

    <main class="container">
      <UAVList />
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2025 X-UAV Platform | {{ uavCount }} UAVs from {{ countryCount }} countries</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import UAVList from './components/UAVList.vue'
import api from './services/api.js'

export default {
  name: 'App',
  components: {
    UAVList
  },
  setup() {
    const uavCount = ref(0)
    const countryCount = ref(0)

    onMounted(async () => {
      try {
        const response = await api.getStats()
        uavCount.value = response.data.total
        countryCount.value = response.data.by_country.length
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    })

    return {
      uavCount,
      countryCount
    }
  }
}
</script>

<style>
/* Global styles are in assets/css/main.css */
</style>
