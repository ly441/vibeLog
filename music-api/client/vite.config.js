import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: "/", // this is important for Vercel deployments
  plugins: [react()],
  server: {
    host: true,
    port: process.env.PORT || 5173
  }
})
