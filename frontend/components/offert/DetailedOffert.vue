<template>
  <div class="detailed-wrapper">
    <div v-if="data" ref="fixedContainer" class="fixed">
      <div class="header">
        <div class="title">
          {{ data.title }}
        </div>
        <div class="description" v-html="data.description"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute();
const id = route.params.id;

const ENV = useRuntimeConfig().public;
const API_URL = ENV.API_URL;

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
  if (!fixedContainer.value) return;
  const newTop = top - window.scrollY;
  const marginTop = 10;

  if (newTop < marginTop) {
    fixedContainer.value.style.top = marginTop + "px";
  } else {
    fixedContainer.value.style.top = newTop + "px";
  }
}

onMounted(() => {
  if (fixedContainer.value) {
    top = fixedContainer.value.offsetTop;
  }

  scrollHandler();
  document.addEventListener("scroll", scrollHandler);
});
</script>

<style>
.detailed-wrapper {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex: 1;

  position: relative;
}

.fixed {
  --_top: calc(
    var(--navbar-height) + var(--spacer-5) * 7 + var(--filterbar-height)
  );
  padding: var(--spacer-5);
  background-color: var(--second-color);
  border-radius: var(--border-radius-2);
  top: var(--_top);
  bottom: 0;
  margin-right: var(--spacer-7);
  position: fixed;
  overflow-y: scroll;
  overflow-x: hidden;
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
</style>
