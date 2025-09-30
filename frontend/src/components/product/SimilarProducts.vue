<template>
  <div class="similar-products">
    <h2 class="text-xl font-bold mb-4">Похожие товары</h2>
    
    <div v-if="isLoading" class="loading-state py-8 text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-accent"></div>
      <p class="mt-2 text-gray-500">Загрузка похожих товаров...</p>
    </div>
    
    <div v-else-if="error" class="error-state py-8 text-center">
      <p class="text-red-500">{{ error }}</p>
    </div>
    
    <div v-else-if="products.length === 0" class="empty-state py-8 text-center">
      <p class="text-gray-500">Похожие товары не найдены</p>
    </div>
    
    <div v-else class="products-grid grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div v-for="product in products" :key="product.id" class="product-card">
        <div class="card border border-gray-200 rounded-lg overflow-hidden transition-shadow hover:shadow-md">
          <div class="thumb bg-gray-100 h-40 overflow-hidden">
            <router-link :to="`/product/${product.id}`">
              <img 
                v-if="product.image" 
                :src="product.image" 
                :alt="product.name" 
                class="w-full h-full object-cover transition-transform hover:scale-105"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </router-link>
          </div>
          
          <div class="info p-3">
            <router-link :to="`/product/${product.id}`" class="block">
              <h3 class="product-name text-sm font-medium text-accent line-clamp-2 hover:underline">
                {{ product.name }}
              </h3>
            </router-link>
            
            <div class="price mt-1 font-bold">
              {{ product.price.toLocaleString() }} ₽
            </div>
            
            <div class="actions mt-2 flex gap-2">
              <button 
                @click="addToCart(product)" 
                class="add-to-cart-btn flex-1 bg-accent text-white text-xs py-1 px-2 rounded hover:opacity-90 transition-opacity flex items-center justify-center"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                В корзину
              </button>
              
              <button 
                @click="toggleFavorite(product)" 
                class="favorite-btn w-8 h-8 flex items-center justify-center border border-gray-200 rounded hover:bg-gray-50 transition-colors"
                :class="{ 'text-red-500': isFavorite(product.id) }"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    stroke-width="2" 
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                    :fill="isFavorite(product.id) ? 'currentColor' : 'none'"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCartStore } from '../../stores/cart'
import { useFavoritesStore } from '../../stores/favorites'
import { useApiCacheStore } from '../../stores/api-cache'
import api from '../../shared/api'

const props = defineProps({
  productId: {
    type: Number,
    required: true
  },
  categoryId: {
    type: Number,
    required: true
  },
  limit: {
    type: Number,
    default: 4
  }
})

const products = ref([])
const isLoading = ref(true)
const error = ref(null)

const cartStore = useCartStore()
const favoritesStore = useFavoritesStore()
const apiCacheStore = useApiCacheStore()

// Добавление товара в корзину
function addToCart(product) {
  cartStore.addItem(product)
}

// Добавление/удаление товара из избранного
function toggleFavorite(product) {
  favoritesStore.toggleFavorite(product)
}

// Проверка, находится ли товар в избранном
function isFavorite(productId) {
  return favoritesStore.isInFavorites(productId)
}

// Загрузка похожих товаров
async function loadSimilarProducts() {
  isLoading.value = true
  error.value = null
  
  try {
    // Формируем ключ для кэша
    const cacheKey = `similar-products-${props.categoryId}-${props.productId}`
    
    // Используем кэширующую функцию из хранилища API-кэша
    const fetchProducts = async () => {
      // В реальном приложении здесь был бы запрос к API для получения похожих товаров
      // Например: const response = await api.get(`/products/similar/${props.productId}`)
      
      // Для демонстрации используем запрос к API для получения товаров из той же категории
      const response = await api.get('/products', {
        params: {
          category: props.categoryId,
          page: 1,
          page_size: props.limit + 1 // Запрашиваем на 1 больше, чтобы исключить текущий товар
        }
      })
      
      // Фильтруем текущий товар из результатов
      return response.data.filter(product => product.id !== props.productId).slice(0, props.limit)
    }
    
    // Получаем данные с использованием кэширования
    const result = await apiCacheStore.cachedApiCall(fetchProducts, cacheKey)
    
    products.value = result
  } catch (err) {
    console.error('Ошибка при загрузке похожих товаров:', err)
    error.value = 'Не удалось загрузить похожие товары. Пожалуйста, попробуйте позже.'
  } finally {
    isLoading.value = false
  }
}

// Загружаем похожие товары при монтировании компонента
onMounted(() => {
  loadSimilarProducts()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
