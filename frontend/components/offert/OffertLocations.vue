<template>
  <div
    class="offert-location-wrapper"
    @click="showAll = !showAll && props.locations.length - 1 > 0"
  >
    <div class="less-locations">
      <Icon name="material-symbols:location-on-outline-rounded" />
      <span>{{ props.locations[0] }}</span>
      <span v-if="props.locations.length > 1 && !showAll"
        >+{{ props.locations.length - 1 }}</span
      >
    </div>
    <div v-if="showAll" ref="moreLocations" class="more-locations">
      <ul>
        <li v-for="(location, idx) in props.locations" :key="idx">
          <Icon name="material-symbols:location-on-outline-rounded" />
          <span> {{ location }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
const moreLocations = ref<HTMLElement>();
onClickOutside(moreLocations, () => (showAll.value = false));

const props = defineProps<{
  locations: string[];
}>();

const showAll = ref(false);
</script>

<style scoped>
.offert-location-wrapper {
  flex: 0;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: var(--font-size-4);
  cursor: pointer;
}
.less-locations {
  display: flex;
  gap: 0.5rem;
}

.more-locations {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  width: 100%;
  font-size: var(--font-size-4);
  background-color: var(--second-color);
  padding: var(--spacer-5);
  box-shadow: 0px 5px 3px 0px rgba(0, 0, 0, 0.75);
  width: min-content;
}

.more-locations ul {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.more-locations li {
  display: flex;
  gap: 0.5rem;
}

.more-locations li span {
  white-space: nowrap;
  font-size: var(--font-size-5);
  color: var(--text-color-light);
}
</style>
