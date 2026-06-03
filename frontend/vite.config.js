import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiTarget = env.VITE_API_BASE_URL
  const credentials = Buffer.from(
    `${env.VITE_API_USERNAME}:${env.VITE_API_PASSWORD}`
  ).toString('base64')

  return {
    plugins: [react()],
    server: {
      proxy: {
        '/service_hub': {
          target: apiTarget,
          changeOrigin: true,
          headers: {
            Authorization: `Basic ${credentials}`,
          },
        },
      },
    },
  }
})
