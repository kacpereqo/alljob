<template>
  <div class="offert-card-wrapper" @click="getMoreDetails">
    <div class="heading">
      <div class="logo">
        <img :src="props.offert.company.logo_url" />
      </div>
      <div class="info">
        <div class="company-info">
          <span class="company"> {{ props.offert.title }}</span>
          <span class="work-title">{{ props.offert.company.name }}</span>
        </div>
        <span><OffertLocations :locations="offert.locations" /></span>
      </div>
    </div>
    <OffertTechnologies :technologies="props.offert.technologies" />
  </div>
</template>

<script setup lang="ts">
const router = useRouter();

const props = defineProps<{
  offert: LeadingOffert;
}>();

function getMoreDetails() {
  router.push(`/offert/${props.offert._id}`);
}
</script>

<style scoped>
.offert-card-wrapper {
  padding: var(--spacer-5);
  display: flex;
  flex-direction: column;
  background-color: var(--second-color);
  border-radius: var(--border-radius-2);
  cursor: pointer;
}

.company-info {
  display: flex;
  flex-direction: column;
}

.heading {
  gap: 1rem;
  display: flex;
  align-items: flex-start;
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.logo {
  width: 10rem;
  height: 8rem;
  border-radius: var(--border-radius-4);
  background-color: white;
  padding: var(--spacer-3);
  overflow: hidden;
}

.info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.info .company {
  font-size: var(--font-size-6);
  font-weight: bold;
  color: var(--font-color-light);
}

.info .work-title {
  font-size: var(--font-size-4);
}
</style>
