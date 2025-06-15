// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  routeRules: {
    '/api/**': {
      proxy: 'http://localhost:8000/api/**'
    }
  }
})
