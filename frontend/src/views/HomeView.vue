<template>
  <div class="home-view">
    <div class="container">
      <section class="hero">
        <h2>Welcome to X-UAV</h2>
        <p class="lead">
          Advanced UAV comparison platform featuring graph-based visualization,
          mission-centric analysis, and variant-level comparisons.
        </p>
        <div class="cta-buttons">
          <router-link to="/compare" class="btn btn-primary">
            Start Comparing UAVs
          </router-link>
          <router-link to="/graph" class="btn btn-secondary">
            Explore Graph View
          </router-link>
        </div>
      </section>

      <section class="features">
        <h3>Key Features</h3>
        <div class="feature-grid">
          <div class="feature-card">
            <h4>🎯 Mission-Centric Analysis</h4>
            <p>Compare UAVs by mission type: ISR, Strike, EW, and more</p>
          </div>
          <div class="feature-card">
            <h4>🔄 Variant Comparison</h4>
            <p>Analyze platform families and their mission-specific configurations</p>
          </div>
          <div class="feature-card">
            <h4>🕸️ Graph Visualization</h4>
            <p>Explore relationships between platforms, countries, and capabilities</p>
          </div>
          <div class="feature-card">
            <h4>⚡ Real-Time Search</h4>
            <p>Intelligent search powered by local LLM and MCP tools</p>
          </div>
        </div>
      </section>

      <section class="status">
        <h3>System Status</h3>
        <div class="status-grid">
          <div class="status-card" :class="{ 'status-ok': apiStatus === 'healthy' }">
            <span class="status-label">API</span>
            <span class="status-value">{{ apiStatus }}</span>
          </div>
          <div class="status-card">
            <span class="status-label">UAVs in Database</span>
            <span class="status-value">{{ uavCount }}</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { checkApiHealth, getUAVs } from '@/services/api'

const apiStatus = ref('checking...')
const uavCount = ref(0)

onMounted(async () => {
  try {
    const health = await checkApiHealth()
    apiStatus.value = health.status

    // Fetch UAV count
    const uavData = await getUAVs()
    uavCount.value = uavData.total
  } catch (error) {
    apiStatus.value = 'unavailable'
    console.error('API health check failed:', error)
  }
})
</script>

<style scoped>
.home-view {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.hero {
  text-align: center;
  padding: 3rem 0;
  border-bottom: 2px solid #ecf0f1;
  margin-bottom: 3rem;
}

.hero h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.lead {
  font-size: 1.2rem;
  color: #7f8c8d;
  max-width: 800px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
}

.btn-secondary {
  background-color: #ecf0f1;
  color: #2c3e50;
}

.btn-secondary:hover {
  background-color: #bdc3c7;
  transform: translateY(-2px);
}

section {
  margin-bottom: 3rem;
}

section h3 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.feature-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #ecf0f1;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.feature-card h4 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.5;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.status-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #e74c3c;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-card.status-ok {
  border-color: #2ecc71;
}

.status-label {
  font-size: 0.9rem;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
}
</style>
