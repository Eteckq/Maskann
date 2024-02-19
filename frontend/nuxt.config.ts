export default defineNuxtConfig({
  devtools: { enabled: true },
  css: [
    "~/assets/css/main.css",
    "primevue/resources/themes/aura-light-green/theme.css",
  ],
  modules: ["nuxt-primevue"],
  primevue: {
    cssLayerOrder: 'tailwind-base, primevue, tailwind-utilities'
  },
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  nitro: {
    routeRules: {
      "/api/**": { proxy: "http://localhost:4000/**" },
    },
  },
});
