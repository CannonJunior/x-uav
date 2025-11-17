<template>
  <div class="about-view">
    <div class="container">
      <h2>About X-UAV</h2>

      <section>
        <h3>Project Overview</h3>
        <p>
          X-UAV is an advanced UAV comparison platform designed for defense analysts,
          procurement specialists, researchers, and UAV enthusiasts. The platform provides
          comprehensive comparison capabilities across technical specifications, missions,
          capabilities, costs, proliferation, and RF spectrum usage.
        </p>
      </section>

      <section>
        <h3>Key Innovation: Variant-Level Comparison</h3>
        <p>
          Unlike traditional UAV databases that treat each platform as a single entity,
          X-UAV recognizes that modern UAVs—especially next-generation Collaborative Combat
          Aircraft (CCA)—are designed as modular platforms with multiple mission-specific
          configurations.
        </p>
        <p>Example: The General Atomics Gambit family includes:</p>
        <ul>
          <li>Gambit 1 (baseline platform)</li>
          <li>Gambit 4 (ISR-focused)</li>
          <li>Gambit 6 (strike/EW variant)</li>
        </ul>
      </section>

      <section>
        <h3>Technical Stack</h3>
        <ul>
          <li><strong>Frontend:</strong> Vue.js 3 with Vite</li>
          <li><strong>Backend:</strong> FastAPI (Python)</li>
          <li><strong>Graph Database:</strong> ArangoDB</li>
          <li><strong>Relational Database:</strong> PostgreSQL</li>
          <li><strong>Cache:</strong> Redis</li>
          <li><strong>LLM:</strong> Ollama (local deployment)</li>
          <li><strong>Visualization:</strong> Cytoscape.js, ECharts</li>
        </ul>
      </section>

      <section>
        <h3>Open Source</h3>
        <p>
          X-UAV is an open-source project focused on zero-cost deployment and
          transparent UAV capability comparison. All data sources are cited and
          verifiable.
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
// About view component
</script>

<style scoped>
.about-view {
  padding: 2rem 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
}

h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 2rem;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

section {
  margin-bottom: 2rem;
}

h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

p {
  line-height: 1.6;
  color: #34495e;
  margin-bottom: 1rem;
}

ul {
  margin-left: 2rem;
  line-height: 1.8;
  color: #34495e;
}

li {
  margin-bottom: 0.5rem;
}

strong {
  color: #2c3e50;
}
</style>
