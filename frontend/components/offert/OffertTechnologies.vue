<template>
  <div ref="carousel" class="technologies" @mousedown="dragStartHandler">
    <div ref="items">
      <span v-for="(tech, i) in props.technologies" :key="i" class="technology">
        {{ tech }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
const isDragging = ref(false);

const carousel: Ref<HTMLElement | null> = ref(null);
const items: Ref<HTMLElement | null> = ref(null);

const props = defineProps<{
  technologies: string[];
}>();

let mouseupListner: void;
let mousemoveListner: void;
let startX: number;

let leftShadow = false;
let rightShadow = false;

function dragStartHandler(event: MouseEvent) {
  isDragging.value = true;
  startX = event.clientX + carousel.value!.scrollLeft;

  mouseupListner = document.addEventListener("mouseup", dragEndHandler);
  mousemoveListner = document.addEventListener("mousemove", dragHandler);
}

function dragHandler(event: MouseEvent) {
  if (!isDragging.value) return;
  if (!carousel.value || !items.value) return;

  carousel.value.scrollLeft = startX - event.clientX;
  setBoxShadow();
}

function setBoxShadow() {
  if (!carousel.value || !items.value) return;
  if (
    carousel.value.scrollLeft + carousel.value.offsetWidth <
    items.value.offsetWidth
  ) {
    rightShadow = true;
  } else {
    rightShadow = false;
  }

  leftShadow = carousel.value.scrollLeft !== 0;

  if (leftShadow && rightShadow) {
    carousel.value.style.transition = "none";
    carousel.value.classList.add("shadow-both");
  } else {
    carousel.value.style.transition = "0.2s ease-in-out";
    carousel.value.classList.remove("shadow-both");
  }

  if (leftShadow) {
    carousel.value.classList.add("shadow-left");
  } else {
    carousel.value.classList.remove("shadow-left");
  }

  if (rightShadow) {
    carousel.value.classList.add("shadow-right");
  } else {
    carousel.value.classList.remove("shadow-right");
  }
}

function dragEndHandler() {
  isDragging.value = false;
  document.removeEventListener("mouseup", mouseupListner!);
  document.removeEventListener("mousemove", mousemoveListner!);
}

onMounted(() => {
  setBoxShadow();
});
</script>

<style scoped>
.technologies {
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;
  --_height: 4rem;
  overflow: hidden;
  position: relative;
  padding-top: calc(var(--spacer-3) + var(--border-width-2));
  padding-bottom: var(--spacer-3);
  border-top: var(--border-width-1) solid var(--font-color-dark);
  margin-top: var(--spacer-3);
  height: var(--_height);
  cursor: grab;
  box-shadow: 0 4px 0px 0px var(--second-color),
    0 -4px 0px 0px var(--second-color);
  transition: 0.1s ease-in-out;
}

.shadow-right {
  box-shadow: inset -10px 0 2px -2px rgba(0, 0, 0, 0.3);
}

.shadow-both {
  box-shadow: inset 10px 0 2px -2px rgba(0, 0, 0, 0.3),
    inset -10px 0 2px -2px rgba(0, 0, 0, 0.3) !important;
}

.shadow-left {
  box-shadow: inset 10px 0 2px -2px rgba(0, 0, 0, 0.3);
}

.technologies div {
  position: absolute;
  display: flex;
  flex-wrap: nowrap;
  left: 0;
  gap: 1rem;
}

.technology {
  font-size: var(--font-size-4);
  display: block;
  padding: var(--spacer-2);
  background-color: var(--second-color-dark);
  border-radius: var(--border-radius-2);
  white-space: nowrap;
}
.arrow {
  left: 0;
  width: 5.4rem;
  height: 5.4rem;
  opacity: 0;
  z-index: 1000;
  color: var(--accent-color);
  cursor: pointer;
  padding: 1.2rem;
}

svg path {
  stroke-width: 10px;
}

.arrow:hover {
  opacity: 1;
  transition: 0.1s ease-in-out;
}
</style>
