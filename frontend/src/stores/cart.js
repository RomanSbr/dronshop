import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../shared/api'
import { useNotificationsStore } from './notifications'

export const useCartStore = defineStore('cart', () => {
  // Состояние
  const items = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  // Геттеры
  const totalItems = computed(() => {
    return items.value.reduce((total, item) => total + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    return items.value.reduce((total, item) => total + item.price * item.quantity, 0)
  })

  const isEmpty = computed(() => {
    return items.value.length === 0
  })

  // Действия
  function addItem(product, quantity = 1) {
    const notificationsStore = useNotificationsStore()
    const existingItem = items.value.find(item => item.id === product.id)
    
    if (existingItem) {
      existingItem.quantity += quantity
      notificationsStore.success(
        'Корзина обновлена',
        `Товар "${product.name}" добавлен в корзину. Общее количество: ${existingItem.quantity}`
      )
    } else {
      items.value.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image,
        quantity
      })
      notificationsStore.success(
        'Товар добавлен в корзину',
        `"${product.name}" успешно добавлен в вашу корзину`
      )
    }
    
    saveToLocalStorage()
  }

  function removeItem(productId) {
    const notificationsStore = useNotificationsStore()
    const index = items.value.findIndex(item => item.id === productId)
    if (index !== -1) {
      const removedItem = items.value[index]
      items.value.splice(index, 1)
      saveToLocalStorage()
      notificationsStore.info(
        'Товар удален из корзины',
        `"${removedItem.name}" был удален из вашей корзины`
      )
    }
  }

  function updateQuantity(productId, quantity) {
    const item = items.value.find(item => item.id === productId)
    if (item) {
      if (quantity <= 0) {
        removeItem(productId)
      } else {
        item.quantity = quantity
        saveToLocalStorage()
      }
    }
  }

  function clearCart() {
    const notificationsStore = useNotificationsStore()
    if (items.value.length > 0) {
      items.value = []
      saveToLocalStorage()
      notificationsStore.info(
        'Корзина очищена',
        'Все товары были удалены из вашей корзины'
      )
    }
  }

  function saveToLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(items.value))
  }

  function loadFromLocalStorage() {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      try {
        items.value = JSON.parse(savedCart)
      } catch (e) {
        console.error('Ошибка при загрузке корзины из localStorage:', e)
        items.value = []
      }
    }
  }

  // Инициализация: загрузка корзины из localStorage при создании хранилища
  loadFromLocalStorage()

  return {
    // Состояние
    items,
    isLoading,
    error,
    
    // Геттеры
    totalItems,
    totalPrice,
    isEmpty,
    
    // Действия
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    loadFromLocalStorage
  }
})
