<template>
  <div class="offert-list-wrapper">
    <OffertCard
      v-for="offert in offerts"
      :key="offert._id"
      :offert="offert"
      @click="getMoreDetails(offert._id)"
    />
    <div v-if="pending" class="pending">
      <LoadingIndicator />
      <span> Fetching Data </span>
    </div>
  </div>
</template>

<script setup lang="ts">
const ENV = useRuntimeConfig().public;
const API_URL = ENV.API_URL;
const router = useRouter();
const pending = ref(false);
const { data: offerts } = await fetchMoreOfferts(0, 10);

let currentOffertID = "";
const limit = 20;

function fetchMoreOfferts(offset = 0, limit = 20) {
  return useFetch<LeadingOffert[]>(API_URL + "/leading? ", {
    params: {
      offset,
      limit,
    },
    method: "POST",
    server: true,
  });
}

function getMoreDetails(OffertID: string) {
  if (currentOffertID !== OffertID) {
    currentOffertID = OffertID;
    router.push(`/offert/${OffertID}`);
  } else {
    currentOffertID = "";
    router.push(`/offert/`);
  }
}

async function scrollHandler() {
  console.log(ENV);
  const scrollHeight = document.documentElement.scrollHeight;
  const scrollTop = document.documentElement.scrollTop;
  const clientHeight = document.documentElement.clientHeight;

  if (scrollTop + clientHeight >= scrollHeight) {
    if (pending.value) return;
    if (!offerts.value) return;

    pending.value = true;

    const { data, error } = await fetchMoreOfferts(offerts.value.length, limit);
    offerts.value = [...offerts.value, ...(data.value as [])];

    pending.value = false;
  }
}

onMounted(() => {
  window.addEventListener("scroll", scrollHandler);
});

onUnmounted(() => {
  window.removeEventListener("scroll", scrollHandler);
});
</script>

<style scoped>
.offert-list-wrapper {
  flex: 1;
  display: grid;
  grid-gap: 1rem;
}

.pending {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  gap: var(--spacer-7);
  font-size: var(--font-size-4);
  padding: var(--spacer-5);
}
</style>
