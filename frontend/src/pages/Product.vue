<template>
  <section v-if="product" class="product">
    <div class="container mx-auto px-4 py-8">
      <!-- Хлебные крошки -->
      <div class="breadcrumbs mb-6 text-sm">
        <router-link to="/" class="text-gray-500 hover:text-accent">Главная</router-link>
        <span class="mx-2 text-gray-400">/</span>
        <router-link to="/catalog" class="text-gray-500 hover:text-accent">Каталог</router-link>
        <span class="mx-2 text-gray-400">/</span>
        <span class="text-gray-700">{{ product.name }}</span>
      </div>
      
      <!-- Основная информация о товаре -->
      <div class="product-main grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <!-- Галерея с лайтбоксом -->
        <div class="product-gallery">
          <ImageLightbox 
            :images="product.images || []" 
            :initialIndex="0"
          />
        </div>
        
        <!-- Информация о товаре -->
        <div class="product-info">
          <h1 class="text-2xl font-bold mb-2">{{ product.name }}</h1>
          
          <!-- Наличие товара -->
          <div class="stock-status mb-4">
            <span 
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="{
                'bg-green-100 text-green-800': isAvailable,
                'bg-red-100 text-red-800': !isAvailable
              }"
            >
              <span 
                class="w-2 h-2 rounded-full mr-1.5"
                :class="{
                  'bg-green-500': isAvailable,
                  'bg-red-500': !isAvailable
                }"
              ></span>
              {{ isInStock ? 'В наличии' : 'Нет в наличии' }}
            </span>
          </div>
          
          <!-- Цена -->
          <div class="price text-3xl font-bold mb-4">
            {{ product.price.toLocaleString() }} ₽
          </div>
          
          <!-- Кнопки действий -->
          <div class="product-actions flex gap-4 mb-6">
            <button 
              @click="addToCart" 
              class="btn-primary flex-1 flex items-center justify-center"
              :disabled="!isAvailable"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              В корзину
            </button>
            
            <button 
              @click="toggleFavorite" 
              class="btn-secondary flex items-center justify-center"
              :class="{ 'text-red-500': isFavorite }"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="2" 
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                  :fill="isFavorite ? 'currentColor' : 'none'"
                />
              </svg>
              {{ isFavorite ? 'В избранном' : 'В избранное' }}
            </button>
          </div>
          
          <!-- Описание товара -->
          <div class="product-description mb-6">
            <h2 class="text-xl font-bold mb-2">Описание</h2>
            <p class="text-gray-700 whitespace-pre-wrap">{{ product.description }}</p>
          </div>
          
          <!-- Характеристики товара (если есть) -->
          <div v-if="product.specs" class="product-specs mb-6">
            <h2 class="text-xl font-bold mb-2">Характеристики</h2>
            <div class="specs-list">
              <div 
                v-for="(value, key) in product.specs" 
                :key="key" 
                class="spec-item flex py-2 border-b border-gray-100"
              >
                <div class="spec-name text-gray-500 w-1/3">{{ key }}</div>
                <div class="spec-value w-2/3">{{ value }}</div>
              </div>
            </div>
          </div>
          
          <!-- Доставка и оплата -->
          <div class="delivery-info bg-gray-50 p-4 rounded-lg">
            <h3 class="font-medium mb-2">Доставка и оплата</h3>
            <ul class="text-sm space-y-2">
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Бесплатная доставка при заказе от 5000 ₽</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Оплата картой или наличными при получении</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Возврат в течение 14 дней</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <!-- Отзывы -->
      <div class="product-reviews mb-12">
        <ProductReviews :productId="product.id" />
      </div>
      
      <!-- Похожие товары -->
      <div class="similar-products">
        <SimilarProducts 
          :productId="product.id" 
          :categoryId="product.category_id"
        />
      </div>
    </div>
  </section>
  
  <!-- Состояние загрузки -->
  <section v-else-if="isLoading" class="loading-state py-16">
    <div class="container mx-auto px-4 text-center">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-accent"></div>
      <p class="mt-4 text-gray-500">Загрузка информации о товаре...</p>
    </div>
  </section>
  
  <!-- Состояние ошибки -->
  <section v-else class="error-state py-16">
    <div class="container mx-auto px-4 text-center">
      <svg class="mx-auto h-16 w-16 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <h2 class="mt-4 text-xl font-bold text-gray-900">Товар не найден</h2>
      <p class="mt-2 text-gray-500">Запрашиваемый товар не существует или был удален</p>
      <div class="mt-6">
        <router-link to="/catalog" class="btn-primary">
          Перейти в каталог
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { useFavoritesStore } from '../stores/favorites'
import { useApiCacheStore } from '../stores/api-cache'
import { useNotificationsStore } from '../stores/notifications'
import ImageLightbox from '../components/product/ImageLightbox.vue'
import ProductReviews from '../components/product/ProductReviews.vue'
import SimilarProducts from '../components/product/SimilarProducts.vue'
import api from '../shared/api'

const route = useRoute()
const cartStore = useCartStore()
const favoritesStore = useFavoritesStore()
const apiCacheStore = useApiCacheStore()

// Availability by active flag (server does not expose stock yet)
const isAvailable = computed(() => {
  if (!product.value) return false
  return !!product.value.active
})

const product = ref(null)
const isLoading = ref(true)
const error = ref(null)

// Проверка наличия товара
const isInStock = computed(() => {
  if (!product.value) return false
  // В реальном приложении здесь была бы проверка наличия товара
  // Для демонстрации считаем, что товар в наличии
  return true
})

// Проверка, находится ли товар в избранном
const isFavorite = computed(() => {
  if (!product.value) return false
  return favoritesStore.isInFavorites(product.value.id)
})

// Добавление товара в корзину
function addToCart() {
  const notificationsStore = useNotificationsStore()
  if (product.value && isAvailable.value) {
    cartStore.addItem(product.value)
  } else if (!isAvailable.value) {
    notificationsStore.error(
      'Товар недоступен',
      'Этот товар временно отсутствует в продаже'
    )
  }
}

// Добавление/удаление товара из избранного
function toggleFavorite() {
  if (product.value) {
    favoritesStore.toggleFavorite(product.value)
  }
}

// Загрузка информации о товаре
async function loadProduct() {
  isLoading.value = true
  error.value = null
  
  try {
    const productId = route.params.id
    const cacheKey = `product-${productId}`
    
    const fetchProduct = async () => {
      const response = await api.get(`/products/${productId}`)
      return response.data
    }
    
    // Получаем данные с использованием кэширования
    const data = await apiCacheStore.cachedApiCall(fetchProduct, cacheKey)
    product.value = data
  } catch (err) {
    console.error('Ошибка при загрузке товара:', err)
    error.value = err
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadProduct()
})
</script>

<style scoped>
.btn-primary {
  @apply inline-block bg-accent text-white py-2 px-4 rounded-md text-center font-medium hover:opacity-90 transition-opacity;
}

.btn-secondary {
  @apply inline-block bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md text-center font-medium hover:bg-gray-50 transition-colors;
}

button:disabled {
  @apply opacity-50 cursor-not-allowed;
}
</style>
