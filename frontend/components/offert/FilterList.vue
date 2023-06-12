<template>
  <div class="filter-wrapper">
    <h1>Oferty pracy</h1>
    <div class="filter-buttons">
      <ul>
        <li>
          <LinedButton
            ><span>Szukaj</span><Icon name="material-symbols:search" />
          </LinedButton>
        </li>
        <li>
          <LinedButton>
            <span>Filtruj</span>
            <Icon name="material-symbols:filter-alt" />
          </LinedButton>
        </li>
        <li>
          <LinedButton>
            <span>Sortuj</span>
            <Icon name="material-symbols:sort-by-alpha-rounded" />
          </LinedButton>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.filter-buttons ul {
  display: flex;
  gap: 3rem;
}

.filter-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  background-color: var(--second-color);
}
</style>
