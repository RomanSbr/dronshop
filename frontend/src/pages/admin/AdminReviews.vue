<template>
  <section class="admin-reviews">
    <div class="container mx-auto px-4 py-6">
    <AdminNavigation />
    <h1 class="text-2xl font-bold mb-6">Управление отзывами</h1>
    
    <!-- Фильтры -->
    <div class="filters bg-white p-4 rounded-lg shadow-sm mb-6">
      <div class="flex flex-wrap gap-4">
        <div class="filter-group">
          <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
          <select 
            v-model="filters.approved" 
            class="input"
            @change="loadReviews"
          >
            <option :value="null">Все отзывы</option>
            <option :value="false">Ожидают проверки</option>
            <option :value="true">Опубликованные</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label class="block text-sm font-medium text-gray-700 mb-1">Товар</label>
          <select 
            v-model="filters.productId" 
            class="input"
            @change="loadReviews"
          >
            <option :value="null">Все товары</option>
            <option v-for="product in products" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
        </div>
        
        <div class="filter-group ml-auto">
          <label class="block text-sm font-medium text-gray-700 mb-1">Действия</label>
          <button @click="loadReviews" class="btn">Обновить</button>
        </div>
      </div>
    </div>
    
    <!-- Список отзывов -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-accent"></div>
      <p class="mt-2 text-gray-600">Загрузка отзывов...</p>
    </div>
    
    <div v-else-if="reviews.length === 0" class="text-center py-8 bg-white rounded-lg shadow-sm">
      <p class="text-gray-600">Отзывы не найдены</p>
    </div>
    
    <div v-else class="reviews-list space-y-4">
      <div 
        v-for="review in reviews" 
        :key="review.id" 
        class="review-item bg-white p-4 rounded-lg shadow-sm"
        :class="{ 'border-l-4 border-yellow-400': !review.approved }"
      >
        <div class="flex justify-between items-start mb-3">
          <div>
            <h3 class="font-medium">{{ review.title }}</h3>
            <div class="text-sm text-gray-600">
              {{ review.name }} ({{ review.email }})
            </div>
            <div class="text-xs text-gray-500">
              {{ formatDate(review.created_at) }}
            </div>
          </div>
          
          <div class="flex items-center">
            <div class="rating text-yellow-400 mr-2">
              <span v-for="i in 5" :key="i" class="star">
                <span v-if="i <= review.rating">★</span>
                <span v-else class="text-gray-300">★</span>
              </span>
            </div>
            <span class="text-sm font-medium">{{ review.rating }}/5</span>
          </div>
        </div>
        
        <div class="review-content mb-3">
          <p>{{ review.content }}</p>
        </div>
        
        <div v-if="review.pros" class="review-pros mb-2">
          <div class="text-xs font-medium text-green-600">Достоинства:</div>
          <p class="text-sm">{{ review.pros }}</p>
        </div>
        
        <div v-if="review.cons" class="review-cons mb-2">
          <div class="text-xs font-medium text-red-600">Недостатки:</div>
          <p class="text-sm">{{ review.cons }}</p>
        </div>
        
        <div class="review-product text-xs text-gray-500 mb-3">
          Товар: {{ getProductName(review.product_id) }}
        </div>
        
        <div class="review-actions flex flex-wrap gap-2">
          <button 
            v-if="!review.approved" 
            @click="approveReview(review.id)" 
            class="btn-sm btn-success"
          >
            Опубликовать
          </button>
          
          <button 
            v-if="review.approved" 
            @click="rejectReview(review.id)" 
            class="btn-sm btn-warning"
          >
            Снять с публикации
          </button>
          
          <button 
            @click="deleteReview(review.id)" 
            class="btn-sm btn-danger"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../../shared/api'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'

const reviews = ref([])
const products = ref([])
const loading = ref(false)

const filters = reactive({
  approved: null,
  productId: null
})

// Загрузка отзывов
async function loadReviews() {
  loading.value = true
  
  try {
    const params = {}
    if (filters.approved !== null) params.approved = filters.approved
    if (filters.productId !== null) params.product_id = filters.productId
    
    const { data } = await api.get('/admin/reviews', { params })
    reviews.value = data
  } catch (error) {
    console.error('Ошибка при загрузке отзывов:', error)
    alert('Не удалось загрузить отзывы')
  } finally {
    loading.value = false
  }
}

// Загрузка товаров для фильтра
async function loadProducts() {
  try {
    const { data } = await api.get('/products', { params: { page_size: 100 } })
    products.value = data
  } catch (error) {
    console.error('Ошибка при загрузке товаров:', error)
  }
}

// Получение названия товара по ID
function getProductName(productId) {
  const product = products.value.find(p => p.id === productId)
  return product ? product.name : `Товар #${productId}`
}

// Форматирование даты
function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Одобрение отзыва
async function approveReview(reviewId) {
  try {
    await api.post(`/admin/reviews/${reviewId}/approve`)
    // Обновляем отзыв в списке
    const review = reviews.value.find(r => r.id === reviewId)
    if (review) review.approved = true
  } catch (error) {
    console.error('Ошибка при одобрении отзыва:', error)
    alert('Не удалось опубликовать отзыв')
  }
}

// Отклонение отзыва
async function rejectReview(reviewId) {
  try {
    await api.post(`/admin/reviews/${reviewId}/reject`)
    // Обновляем отзыв в списке
    const review = reviews.value.find(r => r.id === reviewId)
    if (review) review.approved = false
  } catch (error) {
    console.error('Ошибка при отклонении отзыва:', error)
    alert('Не удалось снять отзыв с публикации')
  }
}

// Удаление отзыва
async function deleteReview(reviewId) {
  if (!confirm('Вы уверены, что хотите удалить этот отзыв?')) return
  
  try {
    await api.delete(`/admin/reviews/${reviewId}`)
    // Удаляем отзыв из списка
    reviews.value = reviews.value.filter(r => r.id !== reviewId)
  } catch (error) {
    console.error('Ошибка при удалении отзыва:', error)
    alert('Не удалось удалить отзыв')
  }
}

// Загрузка данных при монтировании компонента
onMounted(() => {
  loadProducts()
  loadReviews()
})
</script>

<style scoped>
.input {
  @apply px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent;
}

.btn {
  @apply px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity;
}

.btn-sm {
  @apply px-3 py-1 text-sm rounded-md font-medium;
}

.btn-success {
  @apply bg-green-600 text-white hover:bg-green-700;
}

.btn-warning {
  @apply bg-yellow-500 text-white hover:bg-yellow-600;
}

.btn-danger {
  @apply bg-red-600 text-white hover:bg-red-700;
}

.filter-group {
  @apply flex-grow min-w-[200px];
}
</style>
