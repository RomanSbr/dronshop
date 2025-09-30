import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useNotificationsStore } from './notifications'

export const useFavoritesStore = defineStore('favorites', () => {
  // Состояние
  const items = ref([])

  // Геттеры
  const count = computed(() => items.value.length)
  
  const isEmpty = computed(() => items.value.length === 0)

  // Действия
  function addToFavorites(product) {
    const notificationsStore = useNotificationsStore()
    if (!isInFavorites(product.id)) {
      items.value.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image
      })
      saveToLocalStorage()
      notificationsStore.success(
        'Добавлено в избранное',
        `"${product.name}" добавлен в ваш список избранного`
      )
    }
  }

  function removeFromFavorites(productId) {
    const notificationsStore = useNotificationsStore()
    const index = items.value.findIndex(item => item.id === productId)
    if (index !== -1) {
      const removedItem = items.value[index]
      items.value.splice(index, 1)
      saveToLocalStorage()
      notificationsStore.info(
        'Удалено из избранного',
        `"${removedItem.name}" удален из вашего списка избранного`
      )
    }
  }

  function toggleFavorite(product) {
    if (isInFavorites(product.id)) {
      removeFromFavorites(product.id)
    } else {
      addToFavorites(product)
    }
  }

  function isInFavorites(productId) {
    return items.value.some(item => item.id === productId)
  }

  function clearFavorites() {
    const notificationsStore = useNotificationsStore()
    if (items.value.length > 0) {
      items.value = []
      saveToLocalStorage()
      notificationsStore.info(
        'Избранное очищено',
        'Все товары были удалены из вашего списка избранного'
      )
    }
  }

  function saveToLocalStorage() {
    localStorage.setItem('favorites', JSON.stringify(items.value))
  }

  function loadFromLocalStorage() {
    const savedFavorites = localStorage.getItem('favorites')
    if (savedFavorites) {
      try {
        items.value = JSON.parse(savedFavorites)
      } catch (e) {
        console.error('Ошибка при загрузке избранного из localStorage:', e)
        items.value = []
      }
    }
  }

  // Инициализация: загрузка избранного из localStorage при создании хранилища
  loadFromLocalStorage()

  return {
    // Состояние
    items,
    
    // Геттеры
    count,
    isEmpty,
    
    // Действия
    addToFavorites,
    removeFromFavorites,
    toggleFavorite,
    isInFavorites,
    clearFavorites,
    loadFromLocalStorage
  }
})
