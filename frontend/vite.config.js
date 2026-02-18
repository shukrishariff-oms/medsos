import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
// Cache Bust: 2026-02-18
export default defineConfig({
  plugins: [react()],
})
