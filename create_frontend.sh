#!/bin/bash

# Create all frontend configuration files
cd /home/claude/face-attendance-system/frontend

# vite.config.js
cat > vite.config.js << 'VITE'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
VITE

# tailwind.config.js
cat > tailwind.config.js << 'TAIL'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
TAIL

# postcss.config.js
cat > postcss.config.js << 'POST'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
POST

#.gitignore
cat > .gitignore << 'GIT'
node_modules
dist
.DS_Store
GIT

echo "Frontend configuration files created!"
