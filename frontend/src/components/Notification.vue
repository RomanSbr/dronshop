<template>
  <transition name="notification">
    <div 
      v-if="visible" 
      :class="['notification', type]"
      role="alert"
      aria-live="polite"
    >
      <div class="notification-content">
        <div class="notification-icon">
          <svg v-if="type === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="type === 'error'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg v-else-if="type === 'warning'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="notification-message">
          <p class="font-medium">{{ message }}</p>
          <p v-if="description" class="text-sm opacity-90">{{ description }}</p>
        </div>
      </div>
      <button 
        @click="close" 
        class="notification-close"
        aria-label="Закрыть уведомление"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  duration: {
    type: Number,
    default: 5000
  },
  autoClose: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])
const visible = ref(false)
let timeoutId = null

onMounted(() => {
  visible.value = true
  
  if (props.autoClose && props.duration > 0) {
    timeoutId = setTimeout(() => {
      close()
    }, props.duration)
  }
})

onUnmounted(() => {
  if (timeoutId) {
    clearTimeout(timeoutId)
  }
})

function close() {
  visible.value = false
  if (timeoutId) {
    clearTimeout(timeoutId)
    timeoutId = null
  }
  emit('close')
}
</script>

<style scoped>
.notification {
  @apply fixed top-4 right-4 z-50 max-w-sm w-full bg-white rounded-lg shadow-lg border-l-4 p-4 flex items-start justify-between;
  animation: slideIn 0.3s ease-out;
}

.notification.success {
  @apply border-green-500;
}

.notification.error {
  @apply border-red-500;
}

.notification.warning {
  @apply border-yellow-500;
}

.notification.info {
  @apply border-blue-500;
}

.notification-content {
  @apply flex items-start space-x-3 flex-1;
}

.notification-icon {
  @apply flex-shrink-0 mt-0.5;
}

.notification.success .notification-icon {
  @apply text-green-500;
}

.notification.error .notification-icon {
  @apply text-red-500;
}

.notification.warning .notification-icon {
  @apply text-yellow-500;
}

.notification.info .notification-icon {
  @apply text-blue-500;
}

.notification-message {
  @apply flex-1;
}

.notification-close {
  @apply ml-4 flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors;
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
