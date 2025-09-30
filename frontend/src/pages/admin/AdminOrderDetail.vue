<template>
  <section class="admin-order-detail">
    <div class="container mx-auto px-4 py-6">
      <AdminNavigation />

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-accent"></div>
        <p class="mt-3 text-gray-600">Загрузка заказа...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">
        {{ error }}
      </div>

      <div v-else-if="!order" class="bg-white border border-gray-200 rounded-lg p-6 text-center text-gray-500">
        Заказ не найден.
      </div>

      <div v-else class="space-y-6">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 class="text-2xl font-bold">Заказ {{ order.orderNumber }}</h1>
            <p class="text-gray-500">Создан: {{ formatDate(order.createdAt) }}</p>
          </div>
          <div class="flex flex-wrap items-center gap-3">
            <router-link to="/admin/orders" class="btn-secondary">К списку</router-link>
            <select v-model="statusForm.status" class="input">
              <option v-for="option in statusOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
            <button class="btn-primary" @click="updateStatus" :disabled="updating">
              <span v-if="updating">Сохраняем...</span>
              <span v-else>Обновить статус</span>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 space-y-4">
            <div class="bg-white rounded-lg shadow-sm border border-gray-200">
              <div class="border-b border-gray-200 px-6 py-4">
                <h2 class="text-lg font-semibold">Позиции</h2>
              </div>
              <div class="divide-y divide-gray-100">
                <div v-for="item in order.items" :key="item.productId" class="px-6 py-4 flex justify-between gap-4">
                  <div>
                    <div class="font-medium text-gray-900">{{ item.productName }}</div>
                    <div class="text-sm text-gray-500">ID: {{ item.productId }}</div>
                  </div>
                  <div class="text-right text-sm text-gray-600">
                    <div>{{ item.quantity }} × {{ formatCurrency(item.unitPrice) }}</div>
                    <div class="font-medium text-gray-900">{{ formatCurrency(item.totalPrice) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <aside class="space-y-4">
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 class="text-lg font-semibold mb-4">Содержимое</h2>
              <dl class="space-y-2 text-sm text-gray-600">
                <div class="flex justify-between">
                  <dt>Статус:</dt>
                  <dd class="font-medium">{{ formatStatus(order.status) }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt>Сумма:</dt>
                  <dd class="font-medium">{{ formatCurrency(order.totalAmount) }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt>Позиций:</dt>
                  <dd class="font-medium">{{ order.items.length }}</dd>
                </div>
              </dl>
            </div>

            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 class="text-lg font-semibold mb-4">Клиент</h2>
              <dl class="space-y-2 text-sm text-gray-600">
                <div><span class="font-medium">Имя:</span> {{ order.customer.firstName }} {{ order.customer.lastName }}</div>
                <div><span class="font-medium">Email:</span> {{ order.customer.email }}</div>
                <div><span class="font-medium">Телефон:</span> {{ order.customer.phone }}</div>
              </dl>
            </div>

            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 class="text-lg font-semibold mb-4">Доставка</h2>
              <dl class="space-y-2 text-sm text-gray-600">
                <div><span class="font-medium">Способ:</span> {{ formatDelivery(order.shipping.method) }}</div>
                <div v-if="order.shipping.address"><span class="font-medium">Адрес:</span> {{ order.shipping.address }}</div>
                <div v-if="order.shipping.city"><span class="font-medium">Город:</span> {{ order.shipping.city }}</div>
                <div v-if="order.shipping.postalCode"><span class="font-medium">Индекс:</span> {{ order.shipping.postalCode }}</div>
                <div v-if="order.shipping.comment"><span class="font-medium">Комментарий:</span> {{ order.shipping.comment }}</div>
              </dl>
            </div>
          </aside>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'
import api from '../../shared/api'

const route = useRoute()
const router = useRouter()
const order = ref(null)
const loading = ref(true)
const error = ref('')
const updating = ref(false)

const statusOptions = [
  { value: 'pending', label: 'Новый' },
  { value: 'processing', label: 'В обработке' },
  { value: 'paid', label: 'Оплачен' },
  { value: 'shipped', label: 'Отправлен' },
  { value: 'completed', label: 'Завершен' },
  { value: 'cancelled', label: 'Отменён' }
]

const statusForm = reactive({ status: 'pending' })

const orderId = computed(() => Number(route.params.id))

function formatStatus(status) {
  const match = statusOptions.find((option) => option.value === status)
  return match ? match.label : status
}

function formatDate(value) {
  if (!value) return '—'
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

function formatDelivery(method) {
  const labels = {
    courier: 'Курьер',
    pickup: 'Самовывоз',
    post: 'Почта'
  }
  return labels[method] || method
}

async function loadOrder() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get(`/admin/orders/${orderId.value}`)
    order.value = data
    statusForm.status = data.status
    statusForm.status = data.status
  } catch (err) {
    console.error('Failed to load order', err)
    if (err && err.response && err.response.status === 404) {
      error.value = 'Заказ не найден'
    } else {
      error.value = (err && err.response && err.response.data && err.response.data.detail) ? err.response.data.detail : 'Не удалось загрузить заказ'
    }
  } finally {
    loading.value = false
  }
}

async function updateStatus() {
  if (!order.value) return
  updating.value = true
  try {
    const { data } = await api.patch(`/admin/orders/${orderId.value}`, null, { params: { status: statusForm.status } })
    order.value = data
    statusForm.status = data.status
  } catch (err) {
    console.error('Failed to update order status', err)
    const message = (err && err.response && err.response.data && err.response.data.detail) ? err.response.data.detail : 'Не удалось обновить статус'
    alert(message)
  } finally {
    updating.value = false
  }
}

function ensureOrderExists() {
  if (!orderId.value || Number.isNaN(orderId.value)) {
    router.replace('/admin/orders')
  }
}

onMounted(() => {
  ensureOrderExists()
  loadOrder()
})
</script>

<style scoped>
.btn-primary {
  @apply inline-flex items-center px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors;
}

.input {
  @apply px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent;
}
</style>
