import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 7676,
    proxy: {
      '/api': {
        target: 'http://localhost:8877',
        changeOrigin: true,
      }
    }
  }
})
