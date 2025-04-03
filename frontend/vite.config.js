import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    allowedHosts: true,
    proxy: {
      '/search_images': 'http://127.0.0.1:5000',
      '/contacts': 'http://127.0.0.1:5000',
      '/create_contact': 'http://127.0.0.1:5000',
      '/update_contact': 'http://127.0.0.1:5000',
      '/delete_contact': 'http://127.0.0.1:5000'
    }
  },
})
