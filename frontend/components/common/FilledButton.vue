<template>
  <div class="wrapper">
    {{ props.text }}
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  text: { type: String, required: true },
});
</script>

<style scoped>
.wrapper {
  background-color: var(--accent-color);
  color: var(--font-color-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacer-5);
  font-size: var(--font-size-5);
  border-radius: var(--border-radius-2);
  cursor: pointer;
}
.wrapper :hover {
  color: var(--font-color-light);
}
</style>
