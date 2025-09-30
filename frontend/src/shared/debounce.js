import { ref, watch, onUnmounted } from 'vue'

/**
 * Р¤СѓРЅРєС†РёСЏ debounce РґР»СЏ РѕРіСЂР°РЅРёС‡РµРЅРёСЏ С‡Р°СЃС‚РѕС‚С‹ РІС‹Р·РѕРІРѕРІ С„СѓРЅРєС†РёРё
 * @param {Function} func - Р¤СѓРЅРєС†РёСЏ РґР»СЏ РІС‹РїРѕР»РЅРµРЅРёСЏ
 * @param {number} wait - Р’СЂРµРјСЏ РѕР¶РёРґР°РЅРёСЏ РІ РјРёР»Р»РёСЃРµРєСѓРЅРґР°С…
 * @param {boolean} immediate - Р’С‹РїРѕР»РЅРёС‚СЊ РЅРµРјРµРґР»РµРЅРЅРѕ РїСЂРё РїРµСЂРІРѕРј РІС‹Р·РѕРІРµ
 * @returns {Function} Р”РµР±Р°СѓРЅСЃ-С„СѓРЅРєС†РёСЏ
 */
export function debounce(func, wait, immediate = false) {
  let timeout = null
  
  return function executedFunction(...args) {
    const later = () => {
      timeout = null
      if (!immediate) func.apply(this, args)
    }
    
    const callNow = immediate && !timeout
    
    if (timeout) {
      clearTimeout(timeout)
    }
    
    timeout = setTimeout(later, wait)
    
    if (callNow) {
      func.apply(this, args)
    }
  }
}

/**
 * Р”РµР±Р°СѓРЅСЃ РґР»СЏ Vue Composition API
 * @param {any} value - РћС‚СЃР»РµР¶РёРІР°РµРјРѕРµ Р·РЅР°С‡РµРЅРёРµ
 * @param {number} delay - Р—Р°РґРµСЂР¶РєР° РІ РјРёР»Р»РёСЃРµРєСѓРЅРґР°С…
 * @returns {import('vue').Ref} Р”РµР±Р°СѓРЅСЃ-СЂРµР°РєС‚РёРІРЅР°СЏ СЃСЃС‹Р»РєР°
 */
export function useDebounce(value, delay = 300) {
  const debouncedValue = ref(value.value)
  
  let timeout = null
  
  watch(value, (newValue) => {
    if (timeout) {
      clearTimeout(timeout)
    }
    
    timeout = setTimeout(() => {
      debouncedValue.value = newValue
    }, delay)
  })
  
  onUnmounted(() => {
    if (timeout) {
      clearTimeout(timeout)
    }
  })
  
  return debouncedValue
}

/**
 * Р”РµР±Р°СѓРЅСЃ РґР»СЏ РѕР±СЂР°Р±РѕС‚С‡РёРєРѕРІ СЃРѕР±С‹С‚РёР№
 * @param {Function} handler - РћР±СЂР°Р±РѕС‚С‡РёРє СЃРѕР±С‹С‚РёСЏ
 * @param {number} delay - Р—Р°РґРµСЂР¶РєР° РІ РјРёР»Р»РёСЃРµРєСѓРЅРґР°С…
 * @returns {Function} Р”РµР±Р°СѓРЅСЃ-РѕР±СЂР°Р±РѕС‚С‡РёРє
 */
export function debounceHandler(handler, delay = 300) {
  let timeout = null
  
  return function(...args) {
    if (timeout) {
      clearTimeout(timeout)
    }
    
    timeout = setTimeout(() => {
      handler.apply(this, args)
    }, delay)
  }
}

/**
 * Р”РµР±Р°СѓРЅСЃ РґР»СЏ РїРѕРёСЃРєРѕРІС‹С… Р·Р°РїСЂРѕСЃРѕРІ СЃ РѕС‚РјРµРЅРѕР№ РїСЂРµРґС‹РґСѓС‰РёС…
 * @param {Function} searchFunc - Р¤СѓРЅРєС†РёСЏ РїРѕРёСЃРєР°
 * @param {number} delay - Р—Р°РґРµСЂР¶РєР° РІ РјРёР»Р»РёСЃРµРєСѓРЅРґР°С…
 * @returns {Object} РћР±СЉРµРєС‚ СЃ РјРµС‚РѕРґР°РјРё РґР»СЏ СѓРїСЂР°РІР»РµРЅРёСЏ РїРѕРёСЃРєРѕРј
 */
export function createDebouncedSearch(searchFunc, delay = 300) {
  let timeout = null
  let abortController = null
  
  const executeSearch = async (query, ...args) => {
    // РћС‚РјРµРЅСЏРµРј РїСЂРµРґС‹РґСѓС‰РёР№ Р·Р°РїСЂРѕСЃ
    if (abortController) {
      abortController.abort()
    }
    
    abortController = new AbortController()
    
    try {
      await searchFunc(query, { signal: abortController.signal }, ...args)
    } catch (error) {
      if (error.name !== 'AbortError') {
        throw error
      }
    }
  }
  
  const debouncedSearch = (query, ...args) => {
    if (timeout) {
      clearTimeout(timeout)
    }
    
    return new Promise((resolve) => {
      timeout = setTimeout(async () => {
        try {
          const result = await executeSearch(query, ...args)
          resolve(result)
        } catch (error) {
          resolve(Promise.reject(error))
        }
      }, delay)
    })
  }
  
  const cancel = () => {
    if (timeout) {
      clearTimeout(timeout)
      timeout = null
    }
    if (abortController) {
      abortController.abort()
      abortController = null
    }
  }
  
  return {
    search: debouncedSearch,
    cancel
  }
}

export default debounce




