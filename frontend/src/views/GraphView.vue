<template>
  <div class="graph-view">
    <div class="container">
      <h2>Graph Visualization</h2>
      <p class="subtitle">Explore UAV relationships and connections</p>

      <div class="coming-soon">
        <h3>🚧 Under Construction</h3>
        <p>The graph visualization is being built as part of Phase 5 of the project plan.</p>
        <p>Features coming soon:</p>
        <ul>
          <li>Interactive graph exploration with Cytoscape.js</li>
          <li>Platform family relationships</li>
          <li>Manufacturer and country networks</li>
          <li>Mission and capability connections</li>
          <li>Autonomy provider relationships</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
// Graph view component
</script>

<style scoped>
.graph-view {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.coming-soon {
  background: #ecf0f1;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.coming-soon h3 {
  color: #f39c12;
  margin-bottom: 1rem;
}

.coming-soon ul {
  text-align: left;
  max-width: 500px;
  margin: 1rem auto;
}

.coming-soon li {
  margin: 0.5rem 0;
}
</style>
