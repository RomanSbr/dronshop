<template>
  <div class="skeleton-loader" :class="classes" :style="styles">
    <!-- Базовый скелетон -->
    <div v-if="type === 'basic'" class="skeleton-basic" :style="{ height }"></div>
    
    <!-- Скелетон карточки товара -->
    <div v-else-if="type === 'product-card'" class="skeleton-product-card">
      <div class="skeleton-image"></div>
      <div class="skeleton-content">
        <div class="skeleton-title"></div>
        <div class="skeleton-price"></div>
        <div class="skeleton-actions">
          <div class="skeleton-button"></div>
          <div class="skeleton-button"></div>
        </div>
      </div>
    </div>
    
    <!-- Скелетон текста -->
    <div v-else-if="type === 'text'" class="skeleton-text">
      <div v-for="i in lines" :key="i" class="skeleton-line" :class="{ 'short': i === lines && lastLineShort }"></div>
    </div>
    
    <!-- Кастомный скелетон -->
    <div v-else-if="type === 'custom'" class="skeleton-custom">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'basic',
    validator: (value) => ['basic', 'product-card', 'text', 'custom'].includes(value)
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '20px'
  },
  borderRadius: {
    type: String,
    default: '4px'
  },
  lines: {
    type: Number,
    default: 3
  },
  lastLineShort: {
    type: Boolean,
    default: true
  },
  animated: {
    type: Boolean,
    default: true
  }
})

const classes = computed(() => ({
  'animated': props.animated
}))

const styles = computed(() => ({
  width: props.width,
  borderRadius: props.borderRadius
}))
</script>

<style scoped>
.skeleton-loader {
  background-color: var(--bg-tertiary);
  overflow: hidden;
  position: relative;
}

.skeleton-loader.animated::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.4) 50%,
    transparent 100%
  );
  animation: shimmer 1.5s infinite;
}

.skeleton-basic {
  width: 100%;
  background-color: var(--bg-secondary);
  border-radius: inherit;
}

.skeleton-product-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-image {
  width: 100%;
  height: 200px;
  background-color: var(--bg-secondary);
  border-radius: 8px;
}

.skeleton-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-title {
  width: 80%;
  height: 16px;
  background-color: var(--bg-secondary);
  border-radius: 4px;
}

.skeleton-price {
  width: 60%;
  height: 20px;
  background-color: var(--bg-secondary);
  border-radius: 4px;
}

.skeleton-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.skeleton-button {
  flex: 1;
  height: 36px;
  background-color: var(--bg-secondary);
  border-radius: 6px;
}

.skeleton-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-line {
  width: 100%;
  height: 12px;
  background-color: var(--bg-secondary);
  border-radius: 4px;
}

.skeleton-line.short {
  width: 60%;
}

.skeleton-line:nth-child(2) {
  width: 90%;
}

.skeleton-line:nth-child(3) {
  width: 70%;
}

/* Анимация shimmer */
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(200%);
  }
}

/* Адаптивные стили */
@media (max-width: 768px) {
  .skeleton-product-card {
    gap: 8px;
  }
  
  .skeleton-image {
    height: 160px;
  }
  
  .skeleton-actions {
    flex-direction: column;
  }
}

/* Поддержка reduced motion */
@media (prefers-reduced-motion: reduce) {
  .skeleton-loader.animated::before {
    animation: none;
  }
}

/* Темная тема */
@media (prefers-color-scheme: dark) {
  .skeleton-loader {
    background-color: var(--bg-tertiary);
  }
  
  .skeleton-basic,
  .skeleton-image,
  .skeleton-title,
  .skeleton-price,
  .skeleton-button,
  .skeleton-line {
    background-color: var(--bg-secondary);
  }
}
</style>
