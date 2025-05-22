// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  modules: ['@nuxt/eslint', '@nuxt/icon', '@pinia/nuxt'],
  nitro: {
    esbuild: {
      options: {
        target: 'esnext'
      }
    }
  },
  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    middleware: ['auth'],
  },
  
  vite: {
    plugins: [tailwindcss()],
  },
  css: ["~/assets/app.css"],
})
