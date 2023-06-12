<template>
  <div class="detailed-wrapper">
    <div class="header">
      <div class="title">
        {{ data.title }}
      </div>
      <div class="description" v-html="data.description"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const id = route.params.id;

const ENV = useRuntimeConfig().public;
const API_URL = ENV.API_URL;

const { data } = await useFetch(API_URL + "/details/" + id, {
  method: "GET",
});
</script>

<style>
.detailed-wrapper {
  display: flex;
  flex-direction: column;
  background-color: var(--second-color);
  border-radius: var(--border-radius-2);
  overflow: hidden;
  flex: 1;
  height: 100%;
  padding: var(--spacer-5);
}

.title {
  font-size: var(--font-size-10);
  font-weight: bold;
  color: var(--font-color-light);
}

.description {
  font-size: var(--font-size-6);
  margin-top: var(--spacer-3);
  /* color: var(--font-color-light); */
}
.description ul li {
  list-style: circle;
}
</style>
