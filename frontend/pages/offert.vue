<template>
  <div class="index-wrapper">
    <FilterList />
    <div class="offert-list">
      <OffertList />
      <div v-if="displayChild" class="detailed-offert" @loaded="loaded = true">
        <LoadingIndicator v-if="!loaded" />
        <NuxtPage />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter();
const displayChild = ref(false);
const loaded = ref(false);

watch(
  () => router.currentRoute.value.params,
  (params) => {
    if (params.id) {
      displayChild.value = true;
    }
  }
);

useHead({
  title: "oferty pracy",
});
</script>

<style scoped>
.detailed-offert {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacer-5);
}
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
