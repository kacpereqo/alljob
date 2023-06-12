<template>
  <div class="lined-button-wrapper">
    <span>
      <slot />
    </span>
  </div>
</template>

<style scoped>
.lined-button-wrapper {
  width: 100%;
  text-align: center;
  cursor: pointer;
  position: relative;
  font-size: var(--font-size-5);
  overflow: hidden;
  border-radius: var(--border-radius-1);
}

span {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: var(--spacer-2);
  padding: var(--spacer-2) var(--spacer-3);
}

span:hover {
  color: var(--font-color-light);
}
.lined-button-wrapper::after {
  position: absolute;
  content: "";
  height: 0;
  width: 100%;
  bottom: 0;
  left: 0;
  border-radius: var(--border-radius-3);
  border-top: var(--border-width-3) solid var(--accent-color);
}

.lined-button-wrapper::before {
  animation: disappear 0.2s ease-in-out forwards;
  position: absolute;
  content: "";
  height: 0;
  width: 100%;
  bottom: 0;
  border-radius: var(--border-radius-1);
  border: var(--border-width-3) solid var(--accent-color);
  border-right: none;
  border-left: none;
}
.lined-button-wrapper:hover::before {
  animation: appear 0.2s ease-in-out forwards;
}

@keyframes appear {
  from {
    left: 100%;
  }
  to {
    left: 0;
  }
}

@keyframes disappear {
  from {
    left: calc(var(--border-width-3) * -1);
  }
  to {
    left: 100%;
  }
}
</style>
