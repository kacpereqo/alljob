<template>
  <div class="offert-list-wrapper">
    <OffertCard
      v-for="offert in offerts"
      :key="offert._id"
      :offert="offert"
      @click="getMoreDetails(offert._id)"
    />
  </div>
</template>

<script setup lang="ts">
const ENV = useRuntimeConfig().public;
const API_URL = ENV.API_URL;
const router = useRouter();
const { data: offerts } = await fetchMoreOfferts(0, 10);

let newData;
const loading = false;
let currentOffertID = "";

function fetchMoreOfferts(offset: number, limit: number) {
  return useFetch<LeadingOffert[]>(API_URL + "/leading? ", {
    params: {
      offset,
      limit,
    },
    method: "POST",
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

function scrollHandler() {
  // console.log(ENV);
  const scrollHeight = document.documentElement.scrollHeight;
  const scrollTop = document.documentElement.scrollTop;
  const clientHeight = document.documentElement.clientHeight;

  if (scrollTop + clientHeight >= scrollHeight) {
    offerts.push(fetchMoreOfferts(0, 10).data);
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
</style>
