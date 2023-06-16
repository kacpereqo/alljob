<template>
  <div class="index-wrapper">
    <FilterList />
    <div class="offert-list">
      <OffertList />
      <NuxtPage />
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: "oferty pracy",
});
</script>

<style scoped>
.index-wrapper {
  display: flex;
  flex-direction: column;
  background-color: var(--second-color-light);
  border-radius: var(--border-radius-2);
  overflow: hidden;
}

.offert-list {
  display: flex;
  padding: var(--spacer-5);
  gap: var(--spacer-5);
}
</style>
