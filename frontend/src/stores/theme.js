import { defineStore } from 'pinia'
import { ref, watch, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // Состояние темы (light/dark/system)
  const theme = ref(localStorage.getItem('theme') || 'system')
  const isDark = ref(false)

  // Определяем текущую тему системы
  const systemTheme = computed(() => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  })

  // Вычисляем актуальную тему с учетом системных настроек
  const currentTheme = computed(() => {
    return theme.value === 'system' ? systemTheme.value : theme.value
  })

  // Применяем тему к документу
  function applyTheme() {
    const actualTheme = currentTheme.value
    
    if (actualTheme === 'dark') {
      document.documentElement.classList.add('dark-theme')
      document.documentElement.setAttribute('data-theme', 'dark')
      isDark.value = true
    } else {
      document.documentElement.classList.remove('dark-theme')
      document.documentElement.setAttribute('data-theme', 'light')
      isDark.value = false
    }
    
    // Сохраняем предпочтения пользователя
    localStorage.setItem('theme', theme.value)
  }

  // Переключатель темы
  function toggleTheme() {
    const themes = ['light', 'dark', 'system']
    const currentIndex = themes.indexOf(theme.value)
    const nextIndex = (currentIndex + 1) % themes.length
    setTheme(themes[nextIndex])
  }

  // Установка конкретной темы
  function setTheme(newTheme) {
    if (['light', 'dark', 'system'].includes(newTheme)) {
      theme.value = newTheme
      applyTheme()
    }
  }

  // Инициализация темы при создании хранилища
  function initTheme() {
    // Слушаем изменения системной темы
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    
    const handleSystemThemeChange = (e) => {
      if (theme.value === 'system') {
        applyTheme()
      }
    }
    
    mediaQuery.addEventListener('change', handleSystemThemeChange)
    
    // Применяем начальную тему
    applyTheme()
    
    // Очистка при уничтожении
    return () => {
      mediaQuery.removeEventListener('change', handleSystemThemeChange)
    }
  }

  // Следим за изменениями темы
  watch(theme, applyTheme)

  return {
    theme,
    isDark,
    currentTheme,
    systemTheme,
    toggleTheme,
    setTheme,
    initTheme
  }
})
