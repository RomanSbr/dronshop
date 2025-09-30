<template>
  <section class="admin-inventory">
    <div class="container mx-auto px-4 py-6">
      <AdminNavigation />
      <h1 class="text-2xl font-bold mb-6">Управление запасами</h1>

      <div class="filters bg-white p-4 rounded-lg shadow-sm mb-6">
        <div class="flex flex-wrap gap-4 items-end">
          <div class="filter-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Поиск по названию</label>
            <input v-model="filters.search" class="input" placeholder="Поиск по названию" @keyup.enter="loadInventory" />
          </div>

          <div class="filter-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Категория</label>
            <select v-model="filters.categoryId" class="input" @change="loadInventory">
              <option :value="null">Все категории</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
            </select>
          </div>

          <div class="filter-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Наличие</label>
            <select v-model="filters.stock" class="input" @change="loadInventory">
              <option :value="null">Любое</option>
              <option value="in-stock">В наличии</option>
              <option value="out-of-stock">Нет в наличии</option>
              <option value="low-stock">Мало (≤ 5)</option>
            </select>
          </div>

          <div class="filter-group ml-auto">
            <button @click="loadInventory" class="btn">
              <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              Обновить
            </button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-accent"></div>
        <p class="mt-2 text-gray-600">Загрузка остатков...</p>
      </div>

      <div v-else class="inventory-table bg-white rounded-lg shadow-sm overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Товар</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Категория</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Текущий остаток</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Резерв</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Доступно</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="items.length === 0">
              <td colspan="6" class="px-6 py-6 text-center text-sm text-gray-500">Записей не найдено</td>
            </tr>
            <tr v-for="item in filtered" :key="item.productId">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 bg-gray-100 rounded-md overflow-hidden flex items-center justify-center">
                    <img v-if="item.image" :src="item.image" :alt="item.productName" class="h-full w-full object-cover" />
                    <svg v-else class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  </div>
                  <div>
                    <div class="font-medium">{{ item.productName }}</div>
                    <div class="text-sm text-gray-500">{{ getCategoryName(item.category_id) }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ getCategoryName(item.category_id) }}</td>
              <td class="px-6 py-4">
                <input v-model.number="item.currentStock" type="number" min="0" class="input w-28" @change="recalc(item)" />
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ item.reservedStock }}</td>
              <td class="px-6 py-4 text-sm" :class="availableClass(item)">{{ item.availableStock }}</td>
              <td class="px-6 py-4 text-right">
                <div class="inline-flex gap-2">
                  <button class="btn-primary" @click="updateStock(item)" :disabled="item.__saving || item.currentStock < 0">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                  </button>
                  <button class="btn" @click="openProductDetails(item.productId)">Подробнее</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'
import api from '../../shared/api'

const router = useRouter()
const categories = ref([])
const items = ref([])
const loading = ref(true)

const filters = reactive({ search: '', categoryId: null, stock: null })

const filtered = computed(() => {
  let list = [...items.value]
  if (filters.search) {
    const q = filters.search.toLowerCase()
    list = list.filter((i) => i.productName?.toLowerCase().includes(q))
  }
  if (filters.categoryId) list = list.filter((i) => i.category_id === filters.categoryId)
  if (filters.stock === 'in-stock') list = list.filter((i) => (i.availableStock ?? 0) > 0)
  if (filters.stock === 'out-of-stock') list = list.filter((i) => (i.availableStock ?? 0) <= 0)
  if (filters.stock === 'low-stock') list = list.filter((i) => (i.availableStock ?? 0) > 0 && (i.availableStock ?? 0) <= 5)
  return list
})

async function loadCategories() {
  try {
    const { data } = await api.get('/categories')
    categories.value = Array.isArray(data) ? data : []
  } catch (e) {
    categories.value = []
  }
}

async function loadInventory() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/inventory')
    items.value = Array.isArray(data) ? data : []
    items.value.forEach((i) => (i.availableStock = Math.max(0, (i.currentStock ?? 0) - (i.reservedStock ?? 0))))
  } catch (e) {
    items.value = []
  } finally {
    loading.value = false
  }
}

function getCategoryName(categoryId) {
  if (!categoryId) return 'Все категории'
  const c = categories.value.find((x) => x.id === categoryId)
  return c ? c.name : 'Все категории'
}

function recalc(item) {
  if (item.currentStock < 0) item.currentStock = 0
  item.availableStock = Math.max(0, (item.currentStock ?? 0) - (item.reservedStock ?? 0))
}

function availableClass(item) {
  const v = item.availableStock ?? 0
  return v <= 0 ? 'text-red-600' : v <= 5 ? 'text-yellow-600' : 'text-green-600'
}

async function updateStock(item) {
  if (item.__saving) return
  item.__saving = true
  try {
    await api.put(`/admin/inventory/${item.productId}`, { current_stock: item.currentStock })
  } catch (e) {
    // можно добавить уведомление об ошибке
  } finally {
    item.__saving = false
  }
}

function openProductDetails(productId) {
  router.push(`/admin/products/${productId}`)
}

onMounted(() => {
  loadCategories()
  loadInventory()
})
</script>

<style scoped>
.input { @apply px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent; }
.btn { @apply inline-flex items-center px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity; }
.btn-primary { @apply px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed; }
.btn-secondary { @apply inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors; }
.filter-group { @apply flex-grow min-w-[200px]; }
</style>
