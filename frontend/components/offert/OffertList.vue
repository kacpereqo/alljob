<template>
  <div class="offert-list-wrapper">
    <OffertCard v-for="offert in data" :key="offert._id" :offert="offert" />
  </div>
</template>

<script setup lang="ts">
const ENV = useRuntimeConfig().public;
const API_URL = ENV.API_URL;

const { data } = await useFetch<LeadingOffert[]>(API_URL + "/leading", {
  method: "POST",
});
</script>

<style scoped>
.offert-list-wrapper {
  flex: 1;
  display: grid;
  grid-gap: 1rem;
}
</style>
