export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive("click-outside", {
    mounted(el, binding) {
      onClickOutside(el, (event) => console.log(event, binding));
    },
    getSSRProps() {
      return {};
    },
  });
});
