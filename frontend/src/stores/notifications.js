import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref([])
  const nextId = ref(1)

  function showNotification(options) {
    const id = nextId.value++
    const notification = {
      id,
      message: options.message,
      description: options.description || '',
      type: options.type || 'info',
      duration: options.duration || 5000,
      autoClose: options.autoClose !== false
    }

    notifications.value.push(notification)

    // Автоматическое удаление через указанное время
    if (notification.autoClose && notification.duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, notification.duration)
    }

    return id
  }

  function removeNotification(id) {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }

  function clearAll() {
    notifications.value = []
  }

  // Вспомогательные методы для разных типов уведомлений
  function success(message, description = '', options = {}) {
    return showNotification({
      message,
      description,
      type: 'success',
      ...options
    })
  }

  function error(message, description = '', options = {}) {
    return showNotification({
      message,
      description,
      type: 'error',
      ...options
    })
  }

  function warning(message, description = '', options = {}) {
    return showNotification({
      message,
      description,
      type: 'warning',
      ...options
    })
  }

  function info(message, description = '', options = {}) {
    return showNotification({
      message,
      description,
      type: 'info',
      ...options
    })
  }

  return {
    notifications,
    showNotification,
    removeNotification,
    clearAll,
    success,
    error,
    warning,
    info
  }
})
