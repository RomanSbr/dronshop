<template>
  <div class="category-tiles" role="list">
    <button
      v-for="category in categories"
      :key="category.id"
      type="button"
      class="category-tile"
      :class="{ active: isActive(category.id) }"
      @click="selectCategory(category.id)"
      :aria-pressed="isActive(category.id)"
      role="listitem"
    >
      <div class="diamond-shape">
        <div
          class="diamond-content"
          :style="{ backgroundImage: category.image ? `url(${category.image})` : undefined }"
        >
          <div class="diamond-overlay">
            <h3>{{ category.name }}</h3>
          </div>
        </div>
      </div>
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  },
  activeCategory: {
    type: [Number, String],
    default: undefined
  }
})

const emit = defineEmits(['select'])

function selectCategory(categoryId) {
  emit('select', categoryId)
}

function isActive(id) {
  const current = props.activeCategory
  if (current === undefined || current === null || current === '') return false
  return String(current) === String(id)
}
</script>

<style scoped>
.category-tiles {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
}

@media (min-width: 640px) {
  .category-tiles {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 768px) {
  .category-tiles {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1024px) {
  .category-tiles {
    grid-template-columns: repeat(5, 1fr);
  }
}

.category-tile {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background: transparent;
  border: none;
  padding: 0;
  transition: transform 0.3s ease;
}

.category-tile:hover,
.category-tile:focus-visible,
.category-tile.active {
  transform: scale(1.05);
}

.diamond-shape {
  width: 6rem;
  height: 6rem;
  position: relative;
  transform: rotate(45deg);
  overflow: hidden;
}

.diamond-content {
  position: absolute;
  inset: 0;
  background-color: #f3f4f6;
  transform: rotate(-45deg) scale(1.42);
  background-position: center;
  background-size: cover;
}

.diamond-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.category-tile:hover .diamond-overlay,
.category-tile:focus-visible .diamond-overlay,
.category-tile.active .diamond-overlay {
  background-color: rgba(37, 99, 235, 0.6);
}

.diamond-overlay h3 {
  color: white;
  text-align: center;
  font-size: 0.875rem;
  font-weight: 600;
  transform: rotate(-45deg);
  padding: 0 0.5rem;
}
</style>
