<template>
  <div class="filter-panel">
    <aside v-if="!isMobile" class="filters" :aria-label="t('catalog.filters.title')">
      <section class="filter-group">
        <h3 class="filter-title">{{ t('catalog.filters.categories') }}</h3>
        <div class="chips" role="group" :aria-label="t('catalog.filters.categories')">
          <button
            type="button"
            class="chip"
            :class="{ active: !selectedCategory }"
            @click="updateCategory()"
          >
            {{ t('catalog.filters.all') }}
          </button>
          <button
            v-for="c in categories"
            :key="c.id"
            type="button"
            class="chip"
            :class="{ active: String(selectedCategory) === String(c.id) }"
            @click="updateCategory(c.id)"
          >
            {{ c.name }}
          </button>
        </div>
      </section>

      <section class="filter-group">
        <h3 class="filter-title">{{ t('catalog.filters.price') }}</h3>
        <div class="price">
          <label class="sr-only" :for="minId">{{ t('catalog.filters.from') }}</label>
          <input
            :id="minId"
            class="input"
            type="number"
            inputmode="numeric"
            :placeholder="t('catalog.filters.from')"
            v-model="minPrice"
          />
          <label class="sr-only" :for="maxId">{{ t('catalog.filters.to') }}</label>
          <input
            :id="maxId"
            class="input"
            type="number"
            inputmode="numeric"
            :placeholder="t('catalog.filters.to')"
            v-model="maxPrice"
          />
        </div>
      </section>

      <section class="filter-group">
        <h3 class="filter-title">{{ t('catalog.filters.inStock') }}</h3>
        <label class="row small">
          <input type="checkbox" v-model="onlyInStock" />
          <span>{{ t('catalog.filters.inStock') }}</span>
        </label>
      </section>

      <button type="button" class="btn ghost" @click="resetFilters">
        {{ t('catalog.filters.reset') }}
      </button>
    </aside>

    <div v-else class="mobile-filters">
      <button
        type="button"
        class="filter-toggle-btn"
        @click="isDrawerOpen = true"
        :aria-expanded="isDrawerOpen"
      >
        <span>{{ t('catalog.filters.open') }}</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      <div class="filter-drawer" :class="{ open: isDrawerOpen }" role="dialog" :aria-label="t('catalog.filters.title')">
        <div class="drawer-header">
          <h3>{{ t('catalog.filters.title') }}</h3>
          <button type="button" class="close-btn" @click="isDrawerOpen = false">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
            <span class="sr-only">{{ t('common.close') }}</span>
          </button>
        </div>

        <div class="drawer-content">
          <div class="filter-section">
            <h4>{{ t('catalog.filters.categories') }}</h4>
            <div class="chips">
              <button
                type="button"
                class="chip"
                :class="{ active: !selectedCategory }"
                @click="updateCategory(); isDrawerOpen = false"
              >
                {{ t('catalog.filters.all') }}
              </button>
              <button
                v-for="c in categories"
                :key="c.id"
                type="button"
                class="chip"
                :class="{ active: String(selectedCategory) === String(c.id) }"
                @click="updateCategory(c.id); isDrawerOpen = false"
              >
                {{ c.name }}
              </button>
            </div>
          </div>

          <div class="filter-section">
            <h4>{{ t('catalog.filters.price') }}</h4>
            <div class="price">
              <label class="sr-only" :for="drawerMinId">{{ t('catalog.filters.from') }}</label>
              <input
                :id="drawerMinId"
                class="input"
                type="number"
                inputmode="numeric"
                :placeholder="t('catalog.filters.from')"
                v-model="minPrice"
              />
              <label class="sr-only" :for="drawerMaxId">{{ t('catalog.filters.to') }}</label>
              <input
                :id="drawerMaxId"
                class="input"
                type="number"
                inputmode="numeric"
                :placeholder="t('catalog.filters.to')"
                v-model="maxPrice"
              />
            </div>
          </div>

          <div class="filter-section">
            <h4>{{ t('catalog.filters.inStock') }}</h4>
            <label class="row small">
              <input type="checkbox" v-model="onlyInStock" />
              <span>{{ t('catalog.filters.inStock') }}</span>
            </label>
          </div>

          <div class="drawer-actions">
            <button type="button" class="btn ghost" @click="resetFilters">{{ t('catalog.filters.reset') }}</button>
            <button type="button" class="btn" @click="applyFilters">{{ t('catalog.filters.apply') }}</button>
          </div>
        </div>
      </div>

      <div v-if="isDrawerOpen" class="drawer-backdrop" @click="isDrawerOpen = false"></div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useI18n } from '../../shared/i18n'

const props = defineProps({
  categories: { type: Array, default: () => [] },
  initialCategory: { type: [Number, String], default: undefined },
  initialMinPrice: { type: [Number, String], default: '' },
  initialMaxPrice: { type: [Number, String], default: '' },
  initialOnlyInStock: { type: Boolean, default: false }
})

const emit = defineEmits(['update:category', 'update:minPrice', 'update:maxPrice', 'update:onlyInStock', 'reset', 'apply'])
const { t } = useI18n()

const selectedCategory = ref(props.initialCategory)
const minPrice = ref(props.initialMinPrice ?? '')
const maxPrice = ref(props.initialMaxPrice ?? '')
const onlyInStock = ref(props.initialOnlyInStock)

const isDrawerOpen = ref(false)
const isMobile = ref(false)

const minId = `filter-min-${Math.random().toString(36).slice(2, 8)}`
const maxId = `filter-max-${Math.random().toString(36).slice(2, 8)}`
const drawerMinId = `${minId}-drawer`
const drawerMaxId = `${maxId}-drawer`

function syncViewport() {
  isMobile.value = window.innerWidth < 960
}

function updateCategory(categoryId) {
  selectedCategory.value = categoryId
  emit('update:category', categoryId)
}

function resetFilters() {
  selectedCategory.value = undefined
  minPrice.value = ''
  maxPrice.value = ''
  onlyInStock.value = false
  emit('update:category', undefined)
  emit('update:minPrice', '')
  emit('update:maxPrice', '')
  emit('update:onlyInStock', false)
  emit('reset')
  isDrawerOpen.value = false
}

function applyFilters() {
  emit('update:category', selectedCategory.value)
  emit('update:minPrice', minPrice.value)
  emit('update:maxPrice', maxPrice.value)
  emit('update:onlyInStock', onlyInStock.value)
  emit('apply')
  isDrawerOpen.value = false
}

watch(() => props.initialCategory, (newVal) => {
  selectedCategory.value = newVal
})

watch(() => props.initialMinPrice, (newVal) => {
  minPrice.value = newVal ?? ''
})

watch(() => props.initialMaxPrice, (newVal) => {
  maxPrice.value = newVal ?? ''
})

watch(() => props.initialOnlyInStock, (newVal) => {
  onlyInStock.value = Boolean(newVal)
})

watch(minPrice, (newVal) => {
  if (!isMobile.value) {
    emit('update:minPrice', newVal)
  }
})

watch(maxPrice, (newVal) => {
  if (!isMobile.value) {
    emit('update:maxPrice', newVal)
  }
})

watch(onlyInStock, (newVal) => {
  if (!isMobile.value) {
    emit('update:onlyInStock', newVal)
  }
})

onMounted(() => {
  syncViewport()
  window.addEventListener('resize', syncViewport)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', syncViewport)
})
</script>

<style scoped>
.filter-panel {
  @apply space-y-4;
}

.filters {
  @apply sticky top-20 flex flex-col gap-6 bg-white rounded-2xl p-6 shadow-sm border border-gray-100;
}

.filter-group {
  @apply space-y-4;
}

.filter-title {
  @apply text-sm font-semibold uppercase tracking-wide text-gray-500;
}

.chips {
  @apply flex flex-wrap gap-2;
}

.chip {
  @apply inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-gray-100 text-gray-700 hover:bg-accent-50 hover:text-accent-700 transition;
}

.chip.active {
  @apply bg-accent-600 text-white;
}

.price {
  @apply grid grid-cols-2 gap-3;
}

.input {
  @apply w-full border border-gray-200 rounded-xl px-4 py-2 bg-white focus:outline-none focus:border-accent-400 focus:ring-2 focus:ring-accent-200 transition;
}

.row {
  @apply flex items-center gap-2 text-sm text-gray-700;
}

.btn {
  @apply inline-flex items-center justify-center rounded-xl px-4 py-2 font-medium transition;
}

.btn.ghost {
  @apply bg-transparent text-gray-700 border border-gray-300 hover:bg-gray-100;
}

.mobile-filters {
  @apply md:hidden;
}

.filter-toggle-btn {
  @apply inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-200 text-gray-700 shadow-sm bg-white;
}

.filter-drawer {
  @apply fixed top-0 right-0 h-full w-80 max-w-sm bg-white shadow-xl transform translate-x-full transition-transform duration-300 z-50 flex flex-col;
}

.filter-drawer.open {
  @apply translate-x-0;
}

.drawer-header {
  @apply flex items-center justify-between p-6 border-b border-gray-200;
}

.drawer-content {
  @apply flex-1 overflow-y-auto p-6 flex flex-col gap-6;
}

.filter-section h4 {
  @apply text-sm font-semibold text-gray-700 mb-3;
}

.drawer-actions {
  @apply flex gap-3 mt-auto pt-6 border-t border-gray-200;
}

.drawer-actions .btn {
  @apply flex-1 py-3;
}

.drawer-backdrop {
  @apply fixed inset-0 bg-black/50 z-40;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

@media (max-width: 640px) {
  .filter-drawer {
    @apply w-full max-w-none;
  }

  .drawer-content {
    @apply p-4 gap-4;
  }

  .filter-section h4 {
    @apply text-base;
  }

  .chips {
    @apply gap-1.5;
  }

  .chip {
    @apply px-3 py-1.5 text-xs;
  }

  .price {
    @apply grid-cols-1 gap-2;
  }

  .drawer-actions {
    @apply flex-col gap-2;
  }

  .drawer-actions .btn {
    @apply w-full;
  }
}
</style>
