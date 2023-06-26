<template>
  <div class="filter-wrapper">
    <h1>Oferty pracy</h1>
    <div class="filter-buttons">
      <ul>
        <li>
          <LinedButton
            ><span>Szukaj</span><Icon name="material-symbols:search" />
          </LinedButton>
        </li>
        <li>
          <LinedButton @click="showFilters = !showFilters">
            <span>Filtruj</span>
            <Icon name="material-symbols:filter-alt" />
          </LinedButton>
        </li>
      </ul>
    </div>
  </div>
  <div v-if="showFilters" class="filters"></div>
</template>

<script setup lang="ts">
const showFilters = ref(true);
</script>

<style scoped>
.filter-buttons ul {
  display: flex;
  gap: 3rem;
  margin-right: 0.8rem;
  height: var(--filterbar-height);
}

.filters {
  width: 100%;
  height: 10rem;
  background-color: var(--second-color);
  margin-top: var(--spacer-3);
}

.filter-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  background-color: var(--second-color);
}
</style>
