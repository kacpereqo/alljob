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

let top = 0;

function scrollHandler() {
  if (!fixedContainer.value) return;
  const newTop = top - window.scrollY;
  const marginTop = 10;

  if (newTop < marginTop) {
    fixedContainer.value.style.top = marginTop + "px";
  } else {
    fixedContainer.value.style.top = newTop + "px";
  }
}

function WindowResizeHandler() {
  if (fixedContainer.value && container.value) {
    fixedContainer.value.style.width = `${container.value.clientWidth}px`;
  }
}

const { data } = await useLazyFetch(API_URL + "/details/" + id, {
  method: "GET",
});

onMounted(() => {
  if (fixedContainer.value && container.value) {
    top = fixedContainer.value.offsetTop;
    WindowResizeHandler();
  }

  scrollHandler();
  document.addEventListener("scroll", scrollHandler);
  window.addEventListener("resize", WindowResizeHandler);
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
  overflow: hidden;
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
  --_top: calc(
    var(--navbar-height) + var(--spacer-5) * 7 + var(--filterbar-height)
  );
  padding: var(--spacer-5);
  border-radius: var(--border-radius-2);
  top: var(--_top);
  bottom: 0;
  margin-right: var(--spacer-9);
  position: fixed;
  background-color: var(--second-color);
  overflow-y: scroll;
  scrollbar-width: thin;
}

.title {
  font-size: var(--font-size-10);
  font-weight: bold;
  color: var(--font-color-light);
}

.description {
  font-size: var(--font-size-6);
  margin-top: var(--spacer-3);
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
