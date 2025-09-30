<template>
  <section class="admin-orders">
    <div class="container mx-auto px-4 py-6">
      <AdminNavigation />

      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold">Заказы</h1>
          <p class="text-gray-500">Просматривайте и управляйте заказами.</p>
        </div>
        <div class="flex gap-3">
          <button class="btn-secondary" @click="fetchOrders" :disabled="loading">
            <span v-if="loading">Загрузка...</span>
            <span v-else>Обновить</span>
          </button>
        </div>
      </div>

      <div v-if="loading" class="text-center py-10">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-accent"></div>
        <p class="mt-3 text-gray-600">Загрузка заказов...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">{{ error }}</div>

      <div v-else-if="orders.length === 0" class="bg-white border border-gray-200 rounded-lg p-6 text-center text-gray-500">Заказы не найдены.</div>

      <div v-else class="bg-white rounded-lg shadow-sm overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="table-header">№</th>
              <th class="table-header">Статус</th>
              <th class="table-header">Итого</th>
              <th class="table-header">Товаров</th>
              <th class="table-header">Создан</th>
              <th class="table-header"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50 transition">
              <td class="table-cell font-medium text-gray-900">{{ order.orderNumber }}</td>
              <td class="table-cell"><span class="status-pill">{{ formatStatus(order.status) }}</span></td>
              <td class="table-cell">{{ formatCurrency(order.totalAmount) }}</td>
              <td class="table-cell">{{ order.itemsCount }}</td>
              <td class="table-cell text-sm text-gray-500">{{ formatDate(order.createdAt) }}</td>
              <td class="table-cell text-right"><router-link :to="`/admin/orders/${order.id}`" class="text-accent hover:underline">Подробнее</router-link></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'
import api from '../../shared/api'

const orders = ref([])
const loading = ref(false)
const error = ref('')

const statusLabels = {
  pending: 'Pending',
  paid: 'Paid',
  processing: 'Processing',
  shipped: 'Shipped',
  completed: 'Completed',
  cancelled: 'Cancelled',
}

function formatStatus(status) {
  return statusLabels[status] || status
}

function formatDate(value) {
  if (!value) return '-'
  try {
    return new Date(value).toLocaleString('ru-RU')
  } catch (error) {
    return value
  }
}

function formatCurrency(value) {
  const amount = Number(value ?? 0)
  return `${amount.toLocaleString('ru-RU')} ₽`
}

async function fetchOrders() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/admin/orders')
    orders.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Failed to load orders', err)
    error.value = err?.response?.data?.detail || 'Failed to load orders'
  } finally {
    loading.value = false
  }
}

onMounted(fetchOrders)
</script>

<style scoped>
.btn-secondary { @apply inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed; }
.table-header { @apply px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider; }
.table-cell { @apply px-4 py-3 text-sm text-gray-700 align-middle; }
.status-pill { @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-gray-100 text-gray-700; }
</style>
