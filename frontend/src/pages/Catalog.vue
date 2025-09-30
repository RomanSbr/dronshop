<template>
  <section class="catalog">
    <div class="catalog-container">
      <Breadcrumbs />

      <header class="catalog-head">
        <div>
          <h1 class="catalog-title">{{ t('catalog.title') }}</h1>
          <p class="catalog-count" v-if="!isLoading">
            {{ t('catalog.count', { count: totalItems }) }}
          </p>
        </div>
        <form class="catalog-actions" @submit.prevent>
          <label class="search">
            <span class="sr-only">{{ t('catalog.searchPlaceholder') }}</span>
            <input
              type="search"
              v-model="q"
              class="input"
              :placeholder="t('catalog.searchPlaceholder')"
              autocomplete="off"
            />
          </label>

          <label class="sort">
            <span class="sr-only">{{ t('catalog.sortNewest') }}</span>
            <select v-model="sort" class="input">
              <option value="created_at:desc">{{ t('catalog.sortNewest') }}</option>
              <option value="price:asc">{{ t('catalog.sortPriceAsc') }}</option>
              <option value="price:desc">{{ t('catalog.sortPriceDesc') }}</option>
              <option value="name:asc">{{ t('catalog.sortNameAsc') }}</option>
            </select>
          </label>

          <button type="button" class="reset" @click="resetFilters">
            {{ t('catalog.filterReset') }}
          </button>
        </form>
      </header>

      <!-- Category tiles removed for a cleaner layout -->

      <div class="layout">
        <FilterPanel
          :categories="categories"
          :initial-category="category"
          :initial-min-price="priceMin"
          :initial-max-price="priceMax"
          :initial-only-in-stock="inStockOnly"
          @update:category="onCategoryChange"
          @update:minPrice="onMinPriceChange"
          @update:maxPrice="onMaxPriceChange"
          @update:onlyInStock="onStockToggle"
          @reset="resetFilters"
          @apply="applyFilters"
        />

        <div class="catalog-content">
          <AsyncState :loading="isLoading" :error="error" :retry="loadProducts">
            <template #loading>
              <div class="product-grid">
                <SkeletonLoader
                  v-for="i in skeletonCount"
                  :key="`skeleton-${i}`"
                  type="product-card"
                  class="skeleton"
                />
              </div>
            </template>

            <template #default>
              <div v-if="products.length" class="product-grid" role="list">
                <ProductCard v-for="product in products" :key="product.id" :product="product" role="listitem" />
              </div>

              <div v-else class="empty-state">
                <p>{{ t('common.error') }}</p>
              </div>

              <Pagination
                v-if="totalPages > 1"
                :current-page="currentPage"
                :total-pages="totalPages"
                @page-change="handlePageChange"
              />
            </template>
          </AsyncState>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Breadcrumbs from '../components/navigation/Breadcrumbs.vue'
import ProductCard from '../components/ProductCard.vue'
import FilterPanel from '../components/catalog/FilterPanel.vue'
import Pagination from '../components/navigation/Pagination.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import AsyncState from '../components/AsyncState.vue'
import api from '../shared/api'
import { useDebounce } from '../shared/debounce'
import { useApiCacheStore } from '../stores/api-cache'
import { useI18n } from '../shared/i18n'

const router = useRouter()
const route = useRoute()
const apiCacheStore = useApiCacheStore()
const { t } = useI18n()

const products = ref([])
const categories = ref([])
const loading = ref(false)
const error = ref(null)
const totalItemsState = ref(0)

const q = ref('')
const sort = ref('created_at:desc')
const category = ref()
const priceMin = ref('')
const priceMax = ref('')
const inStockOnly = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(12)

const debouncedQ = useDebounce(q, 400)
let syncingFromRoute = false

const isLoading = computed(() => loading.value)
const totalItems = computed(() => totalItemsState.value)
const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / itemsPerPage.value)))
const skeletonCount = computed(() => Math.min(itemsPerPage.value, 8))

function cleanObject(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([_, value]) => value !== undefined && value !== null && value !== '' && value !== false))
}

function buildQuery() {
  return cleanObject({
    q: q.value || undefined,
    sort: sort.value !== 'created_at:desc' ? sort.value : undefined,
    category: category.value ? String(category.value) : undefined,
    price_min: priceMin.value ? String(priceMin.value) : undefined,
    price_max: priceMax.value ? String(priceMax.value) : undefined,
    in_stock: inStockOnly.value ? '1' : undefined,
    page: currentPage.value > 1 ? String(currentPage.value) : undefined
  })
}

async function loadCategories() {
  try {
    const data = await apiCacheStore.cachedApiCall(
      async () => {
        const response = await api.get('/categories')
        return response.data
      },
      'catalog-categories'
    )
    categories.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('Failed to load categories', e)
  }
}

async function loadProducts() {
  loading.value = true
  error.value = null
  try {
    const params = {
      page: currentPage.value,
      page_size: itemsPerPage.value,
      sort: sort.value,
      q: q.value || undefined,
      category: category.value || undefined,
      price_min: priceMin.value || undefined,
      price_max: priceMax.value || undefined,
      in_stock: inStockOnly.value ? 1 : undefined
    }

    const { data } = await api.get('/products', { params })

    if (Array.isArray(data)) {
      products.value = data
      totalItemsState.value = data.length
    } else {
      products.value = data.items || []
      totalItemsState.value = data.meta?.total ?? products.value.length
      if (data.meta?.page_size) {
        itemsPerPage.value = data.meta.page_size
      }
    }
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  if (syncingFromRoute) return
  const nextQuery = buildQuery()
  const currentQuery = route.query

  const same = JSON.stringify(nextQuery) === JSON.stringify(currentQuery)
  if (same) {
    loadProducts()
    return
  }

  router.replace({ query: nextQuery })
}

function onCategorySelect(categoryId) {
  category.value = categoryId
  currentPage.value = 1
  applyFilters()
}

function onCategoryChange(value) {
  category.value = value || undefined
  currentPage.value = 1
  applyFilters()
}

function onMinPriceChange(value) {
  priceMin.value = value || ''
  currentPage.value = 1
  applyFilters()
}

function onMaxPriceChange(value) {
  priceMax.value = value || ''
  currentPage.value = 1
  applyFilters()
}

function onStockToggle(value) {
  inStockOnly.value = value
  currentPage.value = 1
  applyFilters()
}

function handlePageChange(page) {
  currentPage.value = page
  applyFilters()
}

function resetFilters() {
  q.value = ''
  sort.value = 'created_at:desc'
  category.value = undefined
  priceMin.value = ''
  priceMax.value = ''
  inStockOnly.value = false
  currentPage.value = 1
  applyFilters()
}

watch(debouncedQ, () => {
  currentPage.value = 1
  applyFilters()
})

watch(sort, () => {
  currentPage.value = 1
  applyFilters()
})

watch(currentPage, () => {
  if (syncingFromRoute) return
  applyFilters()
})

watch(
  () => route.query,
  (query) => {
    syncingFromRoute = true
    q.value = query.q ?? ''
    sort.value = query.sort ?? 'created_at:desc'
    category.value = query.category ?? undefined
    priceMin.value = query.price_min ?? ''
    priceMax.value = query.price_max ?? ''
    inStockOnly.value = query.in_stock === '1' || query.in_stock === 'true'
    currentPage.value = query.page ? Number.parseInt(query.page, 10) || 1 : 1
    syncingFromRoute = false
    loadProducts()
  },
  { immediate: true }
)

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.catalog {
  @apply py-10;
}

.catalog-container {
  @apply container mx-auto px-4 flex flex-col gap-8;
}

.catalog-head {
  @apply flex flex-col md:flex-row md:items-center md:justify-between gap-6;
}

.catalog-title {
  @apply text-3xl font-bold text-gray-900;
}

.catalog-count {
  @apply text-sm text-gray-500;
}

.catalog-actions {
  @apply flex flex-col sm:flex-row gap-4 items-stretch sm:items-center;
}

.input {
  @apply border border-gray-200 rounded-xl px-4 py-3 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-accent-400 focus:border-accent-400 transition;
}

.search {
  @apply flex-1 w-full min-w-[220px];
}

.sort {
  @apply w-full sm:w-48;
}

.reset {
  @apply text-sm font-medium text-accent-700 bg-accent-50 px-4 py-2.5 rounded-xl hover:bg-accent-100 transition;
}

.layout {
  @apply grid gap-8 grid-cols-1 lg:grid-cols-[300px_1fr];
}

.catalog-content {
  @apply flex flex-col gap-6;
}

.product-grid {
  @apply grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4;
}

.skeleton {
  @apply h-80 rounded-xl;
}

.empty-state {
  @apply text-center text-gray-500 py-12;
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

@media (max-width: 1024px) {
  .layout {
    @apply grid-cols-1;
  }

  .product-grid {
    @apply grid-cols-2 md:grid-cols-3;
  }
}

@media (max-width: 768px) {
  .product-grid {
    @apply grid-cols-2;
  }

  .input {
    @apply py-2.5;
  }
}

@media (max-width: 480px) {
  .product-grid {
    @apply grid-cols-1;
  }
}
</style>

