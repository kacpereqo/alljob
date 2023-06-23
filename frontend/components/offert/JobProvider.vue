<template>
  <div class="job-provider-wrapper">
    <Icon name="material-symbols:dashboard" />
    {{ props.provider }}
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  provider: string;
}>();
</script>

<style scoped>
.job-provider-wrapper {
  width: fit-content;
  flex: 0;
  position: relative;
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  font-size: var(--font-size-4);
  cursor: pointer;
  gap: var(--spacer-4);
  padding: var(--spacer-2);
  border-radius: var(--border-radius-2);
  background-color: var(--second-color-dark);
}
</style>
