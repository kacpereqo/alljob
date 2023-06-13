<template>
  <nav>
    <div class="logo">
      <NuxtLink to="/">
        <img src="@/assets/icons/logo.svg" alt="logo" />
      </NuxtLink>
    </div>
    <div class="links">
      <ul>
        <li>Oferty pracy</li>
        <li>Sprawdź pracodawce</li>
        <li class="separator"></li>
        <li><FilledButton :text="'Zaloguj się'" /></li>
      </ul>
    </div>
  </nav>
</template>

<style>
nav {
  background-color: var(--second-color);
  color: var(--font-color);
  height: 6rem;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  font-size: 1.6rem;
}

.logo {
  cursor: pointer;
  height: 100%;
  width: 8rem;
  display: flex;
  align-items: center;
}

.logo img {
  width: 100%;
}

.logo a {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.links ul {
  list-style: none;
  gap: 3rem;
  height: 100%;
  display: flex;
  align-items: center;
}

.links ul li {
  color: var(--font-color-dark);
}

.links ul li:hover {
  cursor: pointer;
  color: var(--font-color-light);
}

.links ul li:last-child {
  display: flex;
}

.separator {
  height: 2rem;
  width: 0.1rem;
  background-color: var(--font-color-dark);
}

.auth {
  color: var(--font-color-light) !important;
  background-color: var(--accent-color);
  padding: 0.8rem;
  border-radius: 0.5rem;
}

.auth:hover {
  transition: 0.2s;
  background-color: var(--accent-color-hover);
}
</style>
