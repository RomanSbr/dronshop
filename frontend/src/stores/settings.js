import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  // Состояние
  const theme = ref('light') // 'light' или 'dark'
  const notifications = ref(true)
  const language = ref('ru')

  // Геттеры
  const isDarkTheme = computed(() => theme.value === 'dark')

  // Действия
  function setTheme(newTheme) {
    if (newTheme === 'light' || newTheme === 'dark') {
      theme.value = newTheme
      
      // Применяем тему к документу
      if (newTheme === 'dark') {
        document.documentElement.classList.add('dark-theme')
      } else {
        document.documentElement.classList.remove('dark-theme')
      }
      
      saveToLocalStorage()
    }
  }

  function toggleTheme() {
    setTheme(theme.value === 'light' ? 'dark' : 'light')
  }

  function setNotifications(enabled) {
    notifications.value = enabled
    saveToLocalStorage()
  }

  function setLanguage(lang) {
    language.value = lang
    saveToLocalStorage()
  }

  function saveToLocalStorage() {
    localStorage.setItem('settings', JSON.stringify({
      theme: theme.value,
      notifications: notifications.value,
      language: language.value
    }))
  }

  function loadFromLocalStorage() {
    const savedSettings = localStorage.getItem('settings')
    if (savedSettings) {
      try {
        const settings = JSON.parse(savedSettings)
        theme.value = settings.theme || 'light'
        notifications.value = settings.notifications !== undefined ? settings.notifications : true
        language.value = settings.language || 'ru'
        
        // Применяем тему при загрузке
        if (theme.value === 'dark') {
          document.documentElement.classList.add('dark-theme')
        }
      } catch (e) {
        console.error('Ошибка при загрузке настроек из localStorage:', e)
      }
    } else {
      // Проверяем предпочтения системы для темы
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        setTheme('dark')
      }
    }
  }

  // Инициализация: загрузка настроек из localStorage при создании хранилища
  loadFromLocalStorage()

  return {
    // Состояние
    theme,
    notifications,
    language,
    
    // Геттеры
    isDarkTheme,
    
    // Действия
    setTheme,
    toggleTheme,
    setNotifications,
    setLanguage,
    loadFromLocalStorage
  }
})
