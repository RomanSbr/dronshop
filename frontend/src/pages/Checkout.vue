<template>
  <section class="checkout-page">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-2xl font-bold mb-6">{{ t('checkout.title') }}</h1>

      <div v-if="cartStore.isEmpty && !placedOrder" class="empty-cart">
        <div class="text-center py-12">
          <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <h2 class="mt-4 text-lg font-medium text-gray-900">{{ t('checkout.emptyTitle') }}</h2>
          <p class="mt-2 text-sm text-gray-500">{{ t('checkout.emptyDescription') }}</p>
          <div class="mt-6">
            <router-link to="/catalog" class="btn-primary">
              {{ t('checkout.backToCatalog') }}
            </router-link>
          </div>
        </div>
      </div>

      <div v-else class="checkout-content">
        <div class="progress-bar mb-8">
          <div class="flex justify-between">
            <div v-for="(step, index) in steps" :key="step.key" class="step-indicator">
              <div
                class="step-number flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium"
                :class="{
                  'bg-accent text-white': currentStep >= index,
                  'bg-gray-200 text-gray-500': currentStep < index
                }"
              >
                {{ index + 1 }}
              </div>
              <div class="step-label mt-2 text-sm" :class="{ 'font-medium': currentStep === index }">
                {{ step.label }}
              </div>
            </div>
          </div>
          <div class="progress-line mt-4 h-1 bg-gray-200 relative">
            <div
              class="absolute top-0 left-0 h-full bg-accent transition-all duration-300"
              :style="{ width: progressWidth }"></div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2 space-y-6">
            <form v-if="currentStep === 0" class="space-y-4" @submit.prevent="handleNext">
              <h2 class="text-xl font-semibold">{{ t('checkout.contact.title') }}</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <label class="form-group md:col-span-2">
                  <span class="form-label">{{ t('checkout.contact.email') }}*</span>
                  <input
                    type="email"
                    v-model="formData.email"
                    class="form-input"
                    required
                  />
                </label>
                <label class="form-group">
                  <span class="form-label">{{ t('checkout.contact.firstName') }}*</span>
                  <input
                    type="text"
                    v-model="formData.firstName"
                    class="form-input"
                    required
                  />
                </label>
                <label class="form-group">
                  <span class="form-label">{{ t('checkout.contact.lastName') }}*</span>
                  <input
                    type="text"
                    v-model="formData.lastName"
                    class="form-input"
                    required
                  />
                </label>
                <label class="form-group md:col-span-2">
                  <span class="form-label">{{ t('checkout.contact.phone') }}*</span>
                  <input
                    type="tel"
                    v-model="formData.phone"
                    class="form-input"
                    required
                  />
                </label>
              </div>
              <div class="actions flex justify-end gap-3">
                <button type="submit" class="btn-primary">
                  {{ t('checkout.steps.delivery') }}
                </button>
              </div>
            </form>

            <form v-else-if="currentStep === 1" class="space-y-4" @submit.prevent="handleNext">
              <h2 class="text-xl font-semibold">{{ t('checkout.delivery.title') }}</h2>

              <!-- Поля адреса скрыты для самовывоза -->
              <!--
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <label class="form-group md:col-span-2">
                  <span class="form-label">{{ t('checkout.delivery.address') }}*</span>
                  <input type="text" v-model="formData.address" class="form-input" required />
                </label>
                <label class="form-group">
                  <span class="form-label">{{ t('checkout.delivery.city') }}*</span>
                  <input type="text" v-model="formData.city" class="form-input" required />
                </label>
                <label class="form-group">
                  <span class="form-label">{{ t('checkout.delivery.postalCode') }}</span>
                  <input type="text" v-model="formData.postalCode" class="form-input" />
                </label>
              </div>
              -->

              <p class="text-sm text-gray-600">Самовывоз из пункта выдачи. Мы уточним адрес после подтверждения заказа.</p>
              <label class="form-group md:col-span-2">
                <span class="form-label">{{ t('checkout.delivery.comment') }}</span>
                <textarea v-model="formData.deliveryComment" class="form-input" rows="3"></textarea>
              </label>

              <fieldset class="space-y-3">
                <legend class="text-sm font-medium text-gray-700">{{ t('checkout.delivery.title') }}</legend>
                <label v-for="method in deliveryMethods" :key="method.id" class="delivery-option">
                  <input type="radio" class="radio" name="delivery" :value="method.id" v-model="formData.deliveryMethod" />
                  <div>
                    <div class="font-medium">{{ method.name }}</div>
                    <div class="text-sm text-gray-500">{{ method.description }}</div>
                  </div>
                </label>
              </fieldset>

              <div class="actions flex justify-between gap-3">
                <button type="button" class="btn-secondary" @click="handlePrev">
                  {{ t('checkout.steps.contact') }}
                </button>
                <button type="submit" class="btn-primary">
                  {{ t('checkout.steps.payment') }}
                </button>
              </div>
            </form>

            <form v-else-if="currentStep === 2" class="space-y-6" @submit.prevent="handleNext">
              <h2 class="text-xl font-semibold">{{ t('checkout.payment.title') }}</h2>

              <fieldset class="space-y-3">
                <legend class="text-sm font-medium text-gray-700">{{ t('checkout.payment.title') }}</legend>
                <label
                  v-for="method in paymentMethods"
                  :key="method.id"
                  class="delivery-option"
                >
                  <input
                    type="radio"
                    class="radio"
                    name="payment"
                    :value="method.id"
                    v-model="formData.paymentMethod"
                  />
                  <div>
                    <div class="font-medium">{{ method.name }}</div>
                    <div class="text-sm text-gray-500">{{ method.description }}</div>
                  </div>
                </label>
              </fieldset>

              <div class="actions flex justify-between gap-3">
                <button type="button" class="btn-secondary" @click="handlePrev" :disabled="isSubmitting">
                  {{ t('checkout.steps.delivery') }}
                </button>
                <button type="submit" class="btn-primary" :disabled="isSubmitting">
                  <span v-if="isSubmitting">{{ t('checkout.summary.processing') }}</span>
                  <span v-else>{{ t('checkout.summary.confirm') }}</span>
                </button>
              </div>
            </form>

            <div v-else class="space-y-4 text-center">
              <svg class="mx-auto h-16 w-16 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <h2 class="text-2xl font-semibold">{{ t('checkout.summary.successTitle') }}</h2>
              <p class="text-gray-600">
                {{ t('checkout.summary.successDescription', { number: orderNumber }) }}
              </p>
              <router-link to="/" class="btn-primary inline-block">{{ t('checkout.summary.newOrder') }}</router-link>
            </div>
          </div>

          <aside class="lg:col-span-1">
            <div class="order-summary bg-gray-50 p-6 rounded-lg sticky top-4 space-y-4">
              <h2 class="text-xl font-bold">{{ t('checkout.summary.title') }}</h2>

              <ul class="space-y-3 border-b border-gray-200 pb-4">
                <li v-for="item in summaryItems" :key="item.id" class="flex justify-between text-sm">
                  <span class="text-gray-600">{{ item.name }}</span>
                  <span class="font-medium">{{ formatPrice(item.total) }}</span>
                </li>
              </ul>

              <div class="flex justify-between text-sm">
                <span>{{ t('checkout.summary.items', { count: summaryCount }) }}</span>
                <span class="font-medium">{{ formatPrice(summaryTotal) }}</span>
              </div>

              <div class="flex justify-between text-sm">
                <span>{{ t('checkout.summary.delivery') }}</span>
                <span class="text-gray-500">{{ t('checkout.summary.deliveryValue') }}</span>
              </div>

              <div class="flex justify-between items-center text-lg font-bold">
                <span>{{ t('checkout.summary.total') }}</span>
                <span>{{ formatPrice(summaryTotal) }}</span>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import api from '../shared/api'
import { useCartStore } from '../stores/cart'
import { useI18n } from '../shared/i18n'

const cartStore = useCartStore()
const { t } = useI18n()

const currentStep = ref(0)
const isSubmitting = ref(false)
const orderNumber = ref('')
const placedOrder = ref(null)

const formData = reactive({
  email: '',
  firstName: '',
  lastName: '',
  phone: '',
  address: '',
  city: '',
  postalCode: '',
  deliveryComment: '',
  deliveryMethod: 'pickup',
  paymentMethod: 'cash'
})

const steps = computed(() => [
  { key: 'contact', label: t('checkout.steps.contact') },
  { key: 'delivery', label: t('checkout.steps.delivery') },
  { key: 'payment', label: t('checkout.steps.payment') },
  { key: 'confirm', label: t('checkout.steps.confirm') }
])

const deliveryMethods = computed(() => [
  /*{
    id: 'courier',
    name: t('checkout.delivery.methods.courier.name'),
    description: t('checkout.delivery.methods.courier.description')
  },*/
  {
    id: 'pickup',
    name: t('checkout.delivery.methods.pickup.name'),
    description: t('checkout.delivery.methods.pickup.description')
  }
  /*,{
    id: 'post',
    name: t('checkout.delivery.methods.post.name'),
    description: t('checkout.delivery.methods.post.description')
  }*/
])

const paymentMethods = computed(() => [
  /*{
    id: 'card',
    name: t('checkout.payment.methods.card.name'),
    description: t('checkout.payment.methods.card.description')
  },*/
  {
    id: 'cash',
    name: t('checkout.payment.methods.cash.name'),
    description: t('checkout.payment.methods.cash.description')
  }
  /*,{
    id: 'online',
    name: t('checkout.payment.methods.online.name'),
    description: t('checkout.payment.methods.online.description')
  }*/
])

const progressWidth = computed(() => {
  if (steps.value.length <= 1) return '0%'
  const ratio = currentStep.value / (steps.value.length - 1)
  return `${Math.min(100, Math.max(0, ratio * 100))}%`
})

const summaryItems = computed(() => {
  if (placedOrder.value && placedOrder.value.items) {
    return placedOrder.value.items.map((item) => ({
      id: item.productId,
      name: item.productName,
      total: item.totalPrice,
      quantity: item.quantity
    }))
  }
  return cartStore.items.map((item) => ({
    id: item.id,
    name: item.name,
    total: item.price * item.quantity,
    quantity: item.quantity
  }))
})

const summaryCount = computed(() => {
  if (placedOrder.value && placedOrder.value.items) {
    return placedOrder.value.items.reduce((total, item) => total + item.quantity, 0)
  }
  return cartStore.totalItems
})

const summaryTotal = computed(() => {
  if (placedOrder.value && typeof placedOrder.value.totalAmount === 'number') {
    return placedOrder.value.totalAmount
  }
  return cartStore.totalPrice
})

function formatPrice(value) {
  return `${value.toLocaleString()} ${t('common.rub')}`
}

function handlePrev() {
  currentStep.value = Math.max(0, currentStep.value - 1)
}

async function handleNext() {
  if (currentStep.value === steps.value.length - 2) {
    await placeOrder()
  } else {
    currentStep.value = Math.min(steps.value.length - 1, currentStep.value + 1)
  }
}

async function placeOrder() {
  try {
    isSubmitting.value = true

    const orderData = {
      customer: {
        email: formData.email,
        firstName: formData.firstName,
        lastName: formData.lastName,
        phone: formData.phone
      },
      shipping: {
        method: formData.deliveryMethod,
        address: formData.address,
        city: formData.city,
        postalCode: formData.postalCode,
        comment: formData.deliveryComment
      },
      payment: {
        method: formData.paymentMethod
      },
      items: cartStore.items.map((item) => ({
        productId: item.id,
        quantity: item.quantity,
        price: item.price
      })),
      totalAmount: cartStore.totalPrice
    }

    const { data } = await api.post('/orders', orderData)

    placedOrder.value = data
    orderNumber.value = data.orderNumber || ''
    cartStore.clearCart()
    currentStep.value = steps.value.length - 1
  } catch (error) {
    console.error('Checkout failed', error)
    const message = (error && error.response && error.response.data && error.response.data.detail) ? error.response.data.detail : t('checkout.errors.failed')
    alert(message)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.btn-primary {
  @apply inline-block bg-accent text-white py-2 px-4 rounded-md text-center font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply inline-block bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md text-center font-medium hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed;
}

.form-input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.delivery-option {
  @apply flex gap-3 p-4 border border-gray-200 rounded-lg cursor-pointer hover:border-accent transition;
}

.delivery-option .radio {
  @apply mt-1;
}

.progress-bar {
  position: relative;
}

.progress-line {
  @apply rounded-full overflow-hidden;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

button:disabled {
  @apply opacity-50 cursor-not-allowed;
}
</style>
