import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useApiCacheStore = defineStore('apiCache', () => {
  // Состояние
  const cache = ref({})
  const cacheTTL = ref(5 * 60 * 1000) // 5 минут в миллисекундах

  // Действия
  function setCacheItem(key, data) {
    cache.value[key] = {
      data,
      timestamp: Date.now()
    }
  }

  function getCacheItem(key) {
    const item = cache.value[key]
    if (!item) return null

    // Проверяем, не устарел ли кэш
    if (Date.now() - item.timestamp > cacheTTL.value) {
      // Кэш устарел, удаляем его
      delete cache.value[key]
      return null
    }

    return item.data
  }

  function clearCache() {
    cache.value = {}
  }

  function clearCacheItem(key) {
    if (cache.value[key]) {
      delete cache.value[key]
    }
  }

  function setCacheTTL(ttl) {
    cacheTTL.value = ttl
  }

  // Функция для кэширования результатов API-запросов
  async function cachedApiCall(apiFunction, cacheKey, ...args) {
    // Проверяем кэш
    const cachedData = getCacheItem(cacheKey)
    if (cachedData) {
      return cachedData
    }

    // Если данных нет в кэше или они устарели, делаем запрос
    try {
      const result = await apiFunction(...args)
      // Кэшируем результат
      setCacheItem(cacheKey, result)
      return result
    } catch (error) {
      throw error
    }
  }

  return {
    // Действия
    setCacheItem,
    getCacheItem,
    clearCache,
    clearCacheItem,
    setCacheTTL,
    cachedApiCall
  }
})
