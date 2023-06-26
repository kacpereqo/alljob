<template>
  <div ref="container" class="detailed-wrapper">
    <div ref="fixedContainer" class="fixed">
      <div v-if="data" class="offert">
        <div class="header">
          <div class="title">
            {{ data.title }}
          </div>
          <NuxtLink :to="data.url" target="_blank">
            <LinedButton
              >Aplikuj <Icon name="tabler:external-link" />
            </LinedButton>
          </NuxtLink>
        </div>
        <div class="description" v-html="data.description"></div>
      </div>
      <div v-if="!data" class="loading">
        <LoadingIndicator />
        <span> Ładowanie </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const id = route.params.id;

const ENV = useRuntimeConfig().public;
const API_URL = ENV.API_URL;

const container = ref<HTMLElement | null>(null);
const fixedContainer = ref<HTMLElement | null>(null);

const emit = defineEmits<{
  (e: "loaded"): void;
}>();

const { data } = await useFetch(API_URL + "/details/" + id, {
  method: "GET",
  onResponse() {
    emit("loaded");
  },
});

let top = 0;

function scrollHandler() {
  if (!fixedContainer.value || !parentElement) return;
  const marginTop = 10;

  if (parentElement.getBoundingClientRect().y < 0) {
    fixedContainer.value.style.position = "fixed";
    fixedContainer.value.style.width = `${parentElement?.clientWidth}px`;
    fixedContainer.value.style.top = marginTop + "px";
  } else {
    fixedContainer.value.style.position = "absolute";
    fixedContainer.value.style.top = "0px";
  }
}

onMounted(() => {
  if (fixedContainer.value) {
    top = fixedContainer.value.offsetTop;
  }

  document.addEventListener("scroll", scrollHandler);
});
</script>

<style>
a {
  color: inherit;
  text-decoration: none;
}

.detailed-wrapper {
  display: flex;
  flex-direction: column;
  flex: 1;
  position: relative;
}

.offert {
  gap: var(--spacer-5);
  display: flex;
  flex-direction: column;
}

.loading {
  flex: 1;
  position: absolute;
  display: flex;
  flex-direction: column;
  left: 50%;
  top: 30%;
  z-index: 1000;
  gap: var(--spacer-6);
  transform: translate(-50%, 50%);
}

.loading span {
  font-size: var(--font-size-6);
}

.fixed {
  padding: var(--spacer-5);
  border-radius: var(--border-radius-2);
  top: 0;
  bottom: 0;
  margin-right: var(--spacer-7);
  position: fixed;
  overflow-y: scroll;
  overflow-x: hidden;
  scrollbar-width: thin;
  display: flex;
}

.title {
  font-size: var(--font-size-10);
  font-weight: bold;
  color: var(--font-color-light);
}

.description {
  font-size: var(--font-size-6);
}

.description ul {
  margin-left: var(--spacer-6);
  list-style: circle;
}

.header {
  display: flex;
  justify-content: space-between;
}
</style>
