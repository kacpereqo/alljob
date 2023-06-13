export default defineNuxtConfig({
  ssr: true,
  modules: ["nuxt-icon", "@vueuse/nuxt"],
  plugins: ["~/plugins/directives.ts"],
  devtools: { enabled: true },
  components: [
    {
      path: "~/components/common",
    },
    {
      path: "~/components/offert",
    },
    "~/components",
  ],
  runtimeConfig: {
    public: {
      API_URL: process.env.API_URL,
    },
  },
  experimental: {
    payloadExtraction: false,
    inlineSSRStyles: false,
    renderJsonPayloads: true,
  },
  nitro: {
    compressPublicAssets: true,
  },
});
