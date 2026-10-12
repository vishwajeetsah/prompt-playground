import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// BACKEND_URL can point at the docker-compose service name when running
// inside compose; locally it defaults to the backend on localhost:8000.
const backendUrl = process.env.BACKEND_URL ?? 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': backendUrl,
    },
  },
})
