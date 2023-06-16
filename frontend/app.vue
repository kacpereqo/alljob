<template>
  <div id="app">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup>
useHead({
  htmlAttrs: {
    lang: "pl",
  },
  title: "NULL",
  titleTemplate: (titleChunk) => {
    return titleChunk ? `alljob - ${titleChunk} ` : "alljob";
  },
  meta: [
    {
      name: "description",
      content: "Serwis agregacyjny ofert pracy i nie tylko blowjob",
    },
  ],
});
</script>

<style>
@import url("assets/style/main.css");
@import url("https://fonts.googleapis.com/css2?family=Rubik:wght@300;400&family=Space+Grotesk&display=swap");

#app {
  font-family: "Rubik", sans-serif;
  font-family: "Space Grotesk", sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  color: var(--font-color);
  background-color: var(--main-color);
}

html {
  font-size: 62.5%;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

ul {
  list-style: none;
}
</style>
