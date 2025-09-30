<template>
  <section class="cart-page">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-2xl font-bold mb-6">{{ t('cart.title') }}</h1>

      <div v-if="cartStore.isEmpty" class="empty-cart">
        <div class="text-center py-12">
          <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <h2 class="mt-4 text-lg font-medium text-gray-900">{{ t('cart.emptyTitle') }}</h2>
          <p class="mt-2 text-sm text-gray-500">{{ t('cart.emptyDescription') }}</p>
          <div class="mt-6">
            <router-link to="/catalog" class="btn-primary">
              {{ t('cart.backToCatalog') }}
            </router-link>
          </div>
        </div>
      </div>

      <div v-else class="cart-content">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2">
            <div class="cart-items">
              <div v-for="item in cartStore.items" :key="item.id" class="cart-item">
                <div class="flex items-center gap-4 p-4 border border-gray-200 rounded-lg mb-4">
                  <div class="item-image">
                    <img :src="item.image" :alt="item.name" class="w-20 h-20 object-cover rounded-md" />
                  </div>

                  <div class="item-details flex-grow">
                    <router-link :to="`/product/${item.id}`" class="item-name text-lg font-medium text-accent hover:underline">
                      {{ item.name }}
                    </router-link>
                    <div class="item-price text-gray-700">{{ formatPrice(item.price) }}</div>
                  </div>

                  <div class="item-quantity flex items-center">
                    <button
                      @click="decreaseQuantity(item.id)"
                      class="quantity-btn w-8 h-8 flex items-center justify-center border border-gray-300 rounded-l-md"
                      :disabled="item.quantity <= 1"
                    >
                      <span class="text-lg">–</span>
                    </button>
                    <input
                      type="number"
                      v-model.number="item.quantity"
                      min="1"
                      @change="updateQuantity(item.id, item.quantity)"
                      class="quantity-input w-12 h-8 text-center border-t border-b border-gray-300"
                    />
                    <button
                      @click="increaseQuantity(item.id)"
                      class="quantity-btn w-8 h-8 flex items-center justify-center border border-gray-300 rounded-r-md"
                    >
                      <span class="text-lg">+</span>
                    </button>
                  </div>

                  <div class="item-total font-medium">
                    {{ formatPrice(item.price * item.quantity) }}
                  </div>

                  <button @click="removeItem(item.id)" class="remove-btn text-red-500 hover:text-red-700">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="lg:col-span-1">
            <div class="order-summary bg-gray-50 p-6 rounded-lg sticky top-4">
              <h2 class="text-xl font-bold mb-4">{{ t('cart.summaryTitle') }}</h2>

              <div class="summary-row flex justify-between mb-2">
                <span>{{ t('cart.summaryItems', { count: cartStore.totalItems }) }}</span>
                <span>{{ formatPrice(cartStore.totalPrice) }}</span>
              </div>

              <div class="summary-row flex justify-between mb-2">
                <span>{{ t('cart.summaryDelivery') }}</span>
                <span>{{ t('cart.summaryDeliveryValue') }}</span>
              </div>

              <div class="summary-total flex justify-between font-bold text-lg mt-4 pt-4 border-t border-gray-300">
                <span>{{ t('cart.summaryTotal') }}</span>
                <span>{{ formatPrice(cartStore.totalPrice) }}</span>
              </div>

              <router-link to="/checkout" class="btn-primary w-full mt-6">
                {{ t('cart.checkoutCta') }}
              </router-link>

              <button @click="clearCart" class="btn-secondary w-full mt-3">
                {{ t('cart.clear') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useCartStore } from '../stores/cart'
import { useI18n } from '../shared/i18n'

const cartStore = useCartStore()
const { t } = useI18n()

function formatPrice(value) {
  return `${value.toLocaleString()} ${t('common.rub')}`
}

function increaseQuantity(productId) {
  const item = cartStore.items.find((item) => item.id === productId)
  if (item) {
    cartStore.updateQuantity(productId, item.quantity + 1)
  }
}

function decreaseQuantity(productId) {
  const item = cartStore.items.find((item) => item.id === productId)
  if (item && item.quantity > 1) {
    cartStore.updateQuantity(productId, item.quantity - 1)
  }
}

function updateQuantity(productId, quantity) {
  const newQuantity = Math.max(1, quantity)
  cartStore.updateQuantity(productId, newQuantity)
}

function removeItem(productId) {
  cartStore.removeItem(productId)
}

function clearCart() {
  if (confirm(t('cart.confirmClear'))) {
    cartStore.clearCart()
  }
}
</script>

<style scoped>
.btn-primary {
  @apply inline-block bg-accent text-white py-2 px-4 rounded-md text-center font-medium hover:opacity-90 transition-opacity;
}

.btn-secondary {
  @apply inline-block bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md text-center font-medium hover:bg-gray-50 transition-colors;
}

.quantity-btn:disabled {
  @apply opacity-50 cursor-not-allowed;
}

.quantity-input::-webkit-inner-spin-button,
.quantity-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.quantity-input {
  -moz-appearance: textfield;
}
</style>
