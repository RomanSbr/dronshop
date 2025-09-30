<template>
  <section class="favorites-page">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-2xl font-bold mb-6">{{ t('favorites.title') }}</h1>

      <div v-if="favoritesStore.isEmpty" class="empty-favorites">
        <div class="text-center py-12">
          <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1"
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            />
          </svg>
          <h2 class="mt-4 text-lg font-medium text-gray-900">{{ t('favorites.emptyTitle') }}</h2>
          <p class="mt-2 text-sm text-gray-500">{{ t('favorites.emptyDescription') }}</p>
          <div class="mt-6">
            <router-link to="/catalog" class="btn-primary">
              {{ t('favorites.backToCatalog') }}
            </router-link>
          </div>
        </div>
      </div>

      <div v-else>
        <div class="favorites-actions flex justify-between items-center mb-6">
          <div class="text-gray-500">
            {{ t('favorites.count', { count: favoritesStore.count, noun: getNounPluralForm(favoritesStore.count) }) }}
          </div>
          <button @click="clearFavorites" class="btn-secondary">
            {{ t('favorites.clear') }}
          </button>
        </div>

        <div class="favorites-grid grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          <div v-for="product in favoritesStore.items" :key="product.id" class="favorite-item">
            <div class="card border border-gray-200 rounded-lg overflow-hidden transition-shadow hover:shadow-md">
              <div class="thumb bg-gray-100 h-40 overflow-hidden relative">
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

                <button
                  @click="removeFromFavorites(product.id)"
                  class="remove-btn absolute top-2 right-2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-sm hover:bg-gray-100 transition-colors"
                  :aria-label="t('favorites.removed')"
                >
                  <svg class="w-5 h-5 text-red-500" fill="currentColor" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>

              <div class="info p-3">
                <router-link :to="`/product/${product.id}`" class="block">
                  <h3 class="product-name text-sm font-medium text-accent line-clamp-2 hover:underline">
                    {{ product.name }}
                  </h3>
                </router-link>

                <div class="price mt-1 font-bold">
                  {{ formatPrice(product.price) }}
                </div>

                <div class="actions mt-2">
                  <button
                    @click="addToCart(product)"
                    class="add-to-cart-btn w-full bg-accent text-white py-1.5 px-3 rounded hover:opacity-90 transition-opacity flex items-center justify-center"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    {{ t('favorites.addToCart') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useFavoritesStore } from '../stores/favorites'
import { useCartStore } from '../stores/cart'
import { useI18n } from '../shared/i18n'

const favoritesStore = useFavoritesStore()
const cartStore = useCartStore()
const { t, locale } = useI18n()

function formatPrice(value) {
  return `${value.toLocaleString()} ${t('common.rub')}`
}

function removeFromFavorites(productId) {
  favoritesStore.removeFromFavorites(productId)
}

function clearFavorites() {
  if (confirm(t('favorites.confirmClear'))) {
    favoritesStore.clearFavorites()
  }
}

function addToCart(product) {
  cartStore.addItem(product)
}

function getNounPluralForm(number) {
  if (locale.value === 'en') {
    return number === 1 ? 'item' : 'items'
  }
  const forms = ['товар', 'товара', 'товаров']
  const cases = [2, 0, 1, 1, 1, 2]
  return forms[number % 100 > 4 && number % 100 < 20 ? 2 : cases[Math.min(number % 10, 5)]]
}
</script>

<style scoped>
.btn-primary {
  @apply inline-block bg-accent text-white py-2 px-4 rounded-md text-center font-medium hover:opacity-90 transition-opacity;
}

.btn-secondary {
  @apply inline-block bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md text-center font-medium hover:bg-gray-50 transition-colors;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
