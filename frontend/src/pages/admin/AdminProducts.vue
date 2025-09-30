<template>
  <section class="admin-products">
    <div class="container mx-auto px-4 py-6">
      <AdminNavigation />

      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold">Товары</h1>
        <div class="flex gap-3">
          <router-link to="/admin/products/new" class="btn-primary">
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Создать товар
          </router-link>
        </div>
      </div>

      <div class="filters bg-white p-4 rounded-lg shadow-sm mb-6">
        <div class="flex flex-wrap gap-4 items-end">
          <div class="filter-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Поиск</label>
            <input v-model="filters.search" class="input" placeholder="Поиск по названию" @keyup.enter="loadProducts" />
          </div>

          <div class="filter-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Категория</label>
            <select v-model="filters.categoryId" class="input" @change="loadProducts">
              <option :value="null">Все категории</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
            </select>
          </div>

          <div class="filter-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
            <select v-model="filters.active" class="input" @change="loadProducts">
              <option :value="null">Любой</option>
              <option :value="true">Активные</option>
              <option :value="false">Неактивные</option>
            </select>
          </div>

          <div class="filter-group ml-auto">
            <button @click="loadProducts" class="btn">
              <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Обновить
            </button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-accent"></div>
        <p class="mt-2 text-gray-600">Загрузка товаров...</p>
      </div>

      <div v-else-if="items.length === 0" class="text-center py-8 bg-white rounded-lg shadow-sm">
        <p class="text-gray-600">Товары не найдены</p>
        <router-link to="/admin/products/new" class="btn-secondary inline-block mt-4">Создать первый товар</router-link>
      </div>

      <div v-else class="products-grid grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        <div v-for="product in items" :key="product.id" class="product-card bg-white rounded-lg shadow-sm overflow-hidden" :class="{ 'opacity-60': !product.active }">
          <div class="product-image h-40 bg-gray-100 relative">
            <img v-if="product.image" :src="product.image" :alt="product.name" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
              <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            </div>
            <div v-if="!product.active" class="absolute top-2 right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">Неактивен</div>
          </div>

          <div class="product-info p-4">
            <h3 class="font-medium text-lg mb-1 line-clamp-2">{{ product.name }}</h3>
            <div class="text-accent font-bold mb-3">{{ product.price.toLocaleString() }} ₽</div>
            <div class="text-sm text-gray-500 mb-4 line-clamp-2">{{ product.description || 'Описание отсутствует' }}</div>
            <div class="flex justify-between items-center">
              <div class="text-xs text-gray-500">ID: {{ product.id }}</div>
              <button class="btn-sm btn-danger ml-2" @click="removeProduct(product)" :disabled="deletingId === product.id">
                <span v-if="deletingId === product.id">Удаление...</span>
                <span v-else>Удалить</span>
              </button>
              <router-link :to="`/admin/products/${product.id}`" class="btn-sm btn-primary">Открыть</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import api from '../../shared/api'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'

const categories = ref([])
const items = ref([])
const loading = ref(true)
const deletingId = ref(null)

const filters = reactive({ search: '', categoryId: null, active: null })

async function loadProducts() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/products', {
      params: {
        q: filters.search || undefined,
        category: filters.categoryId || undefined,
        active: filters.active,
        sort: 'created_at:desc',
        page_size: 100,
      },
    })
    items.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Failed to load products', error)
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  try {
    const { data } = await api.get('/categories')
    categories.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Failed to load categories', error)
  }
}

onMounted(() => {
  loadCategories()
  loadProducts()
})

async function removeProduct(product) {
  if (deletingId.value || !product || !product.id) return
  if (!confirm(`Удалить товар "${product.name}" (ID: ${product.id})? Это действие нельзя отменить.`)) return
  deletingId.value = product.id
  try {
    await api.delete(`/admin/products/${product.id}`)
    items.value = items.value.filter((p) => p.id !== product.id)
  } catch (error) {
    console.error('Failed to delete product', error)
    alert(error?.response?.data?.detail || 'Не удалось удалить товар')
  } finally {
    deletingId.value = null
  }
}
</script>

<style scoped>
.input { @apply px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent; }
.btn { @apply inline-flex items-center px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity; }
.btn-primary { @apply inline-flex items-center px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity; }
.btn-secondary { @apply inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors; }
.btn-sm { @apply px-3 py-1 text-sm rounded-md; }
.btn-danger { @apply inline-flex items-center px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed; }
.filter-group { @apply flex-grow min-w-[200px]; }
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>
