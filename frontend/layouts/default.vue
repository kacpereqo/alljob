<template>
  <div class="wrapper">
    <TheNavbar />
    <div>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.wrapper div {
  flex: 1;
  margin: 2rem;
}
</style>
