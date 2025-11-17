<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <div class="navbar-brand">
          <router-link to="/" class="brand-link">
            <h1>X-UAV</h1>
            <span class="tagline">UAV Comparison Platform</span>
          </router-link>
        </div>
        <div class="navbar-menu">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/compare" class="nav-link">Compare</router-link>
          <router-link to="/graph" class="nav-link">Graph View</router-link>
          <router-link to="/about" class="nav-link">About</router-link>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <div class="container">
        <p>&copy; 2025 X-UAV. Open Source UAV Comparison Platform.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Main application component
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand .brand-link {
  text-decoration: none;
  color: white;
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.navbar-brand h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
}

.navbar-brand .tagline {
  font-size: 0.9rem;
  color: #95a5a6;
}

.navbar-menu {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #34495e;
}

.nav-link.router-link-active {
  background-color: #3498db;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}

.footer {
  background-color: #2c3e50;
  color: white;
  padding: 1.5rem 0;
  margin-top: auto;
  text-align: center;
}

.footer p {
  margin: 0;
  color: #95a5a6;
}
</style>
