<template>
  <div class="index-wrapper">
    <FilterList />
    <OffertList />
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.index-wrapper {
  display: flex;
  flex-direction: column;
  background-color: var(--second-color-light);
  border-radius: var(--border-radius-2);
  overflow: hidden;
}
</style>
