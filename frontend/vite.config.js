import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true,
    },
    proxy: {
      '/api/apkscanner': {
        target: 'http://apkscanner:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/apkscanner/, ''),
        timeout: 30000
      },
      '/api/secrethunter': {
        target: 'http://secrethunter:8002',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/secrethunter/, ''),
        timeout: 30000
      },
      '/api/cryptocheck': {
        target: 'http://cryptocheck:8003',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/cryptocheck/, ''),
        timeout: 30000
      },
      '/api/networkinspector': {
        target: 'http://networkinspector:8004',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/networkinspector/, ''),
        timeout: 30000
      },
      '/api/reportgen': {
        target: 'http://reportgen:8005',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/reportgen/, ''),
        timeout: 30000
      },
      '/api/fixsuggest': {
        target: 'http://fixsuggest:8006',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/fixsuggest/, ''),
        timeout: 30000
      },
      '/api/ciconnector': {
        target: 'http://ciconnector:8007',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/ciconnector/, ''),
        timeout: 30000
      }
    }
  }
})
