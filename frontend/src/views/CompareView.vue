<template>
  <div class="compare-view">
    <div class="container">
      <h2>UAV Comparison</h2>
      <p class="subtitle">Compare platforms, variants, and mission configurations</p>

      <div class="coming-soon">
        <h3>🚧 Under Construction</h3>
        <p>The comparison interface is being built as part of Phase 4 of the project plan.</p>
        <p>Features coming soon:</p>
        <ul>
          <li>Side-by-side platform comparison</li>
          <li>Variant-level analysis</li>
          <li>Mission configuration comparison</li>
          <li>Performance radar charts</li>
          <li>Cost analysis tools</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
// Compare view component
</script>

<style scoped>
.compare-view {
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
  max-width: 400px;
  margin: 1rem auto;
}

.coming-soon li {
  margin: 0.5rem 0;
}
</style>
