<template>
  <div class="lightbox-wrapper">
    <!-- Превью изображений -->
    <div class="main-image-container" @click="openLightbox">
      <img :src="images[currentIndex]" alt="" class="main-image" />
      <div class="zoom-hint">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
        </svg>
        <span>Нажмите для увеличения</span>
      </div>
    </div>
    
    <div class="thumbnails">
      <button 
        v-if="images.length > 4" 
        class="nav-btn prev" 
        @click="scrollThumbnails('prev')"
        :disabled="thumbnailScrollPos <= 0"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      
      <div class="thumbnails-container" ref="thumbnailsContainer">
        <div 
          v-for="(src, i) in images" 
          :key="i" 
          class="thumbnail" 
          :class="{ active: i === currentIndex }"
          @click="setCurrentImage(i)"
        >
          <img :src="src" alt="" />
        </div>
      </div>
      
      <button 
        v-if="images.length > 4" 
        class="nav-btn next" 
        @click="scrollThumbnails('next')"
        :disabled="thumbnailScrollPos >= maxScrollPos"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
    
    <!-- Лайтбокс -->
    <div v-if="isLightboxOpen" class="lightbox-overlay" @click.self="closeLightbox">
      <div class="lightbox-content">
        <button class="close-btn" @click="closeLightbox">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        
        <div class="lightbox-image-container">
          <button 
            v-if="images.length > 1" 
            class="lightbox-nav prev" 
            @click="prevImage"
            :disabled="lightboxIndex === 0"
          >
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          
          <img :src="images[lightboxIndex]" alt="" class="lightbox-image" />
          
          <button 
            v-if="images.length > 1" 
            class="lightbox-nav next" 
            @click="nextImage"
            :disabled="lightboxIndex === images.length - 1"
          >
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
        
        <div class="lightbox-counter">
          {{ lightboxIndex + 1 }} / {{ images.length }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    required: true
  },
  initialIndex: {
    type: Number,
    default: 0
  }
})

const currentIndex = ref(props.initialIndex)
const isLightboxOpen = ref(false)
const lightboxIndex = ref(props.initialIndex)
const thumbnailsContainer = ref(null)
const thumbnailScrollPos = ref(0)
const maxScrollPos = ref(0)

// Устанавливаем текущее изображение
function setCurrentImage(index) {
  currentIndex.value = index
}

// Открываем лайтбокс
function openLightbox() {
  isLightboxOpen.value = true
  lightboxIndex.value = currentIndex.value
  document.body.style.overflow = 'hidden' // Блокируем прокрутку страницы
}

// Закрываем лайтбокс
function closeLightbox() {
  isLightboxOpen.value = false
  document.body.style.overflow = '' // Восстанавливаем прокрутку страницы
}

// Переход к предыдущему изображению в лайтбоксе
function prevImage() {
  if (lightboxIndex.value > 0) {
    lightboxIndex.value--
  }
}

// Переход к следующему изображению в лайтбоксе
function nextImage() {
  if (lightboxIndex.value < props.images.length - 1) {
    lightboxIndex.value++
  }
}

// Прокрутка миниатюр
function scrollThumbnails(direction) {
  const container = thumbnailsContainer.value
  const scrollAmount = 80 // Ширина миниатюры + отступ
  
  if (direction === 'prev') {
    thumbnailScrollPos.value = Math.max(0, thumbnailScrollPos.value - scrollAmount)
  } else {
    thumbnailScrollPos.value = Math.min(maxScrollPos.value, thumbnailScrollPos.value + scrollAmount)
  }
  
  container.scrollLeft = thumbnailScrollPos.value
}

// Обработка клавиш при открытом лайтбоксе
function handleKeyDown(e) {
  if (!isLightboxOpen.value) return
  
  if (e.key === 'Escape') {
    closeLightbox()
  } else if (e.key === 'ArrowLeft') {
    prevImage()
  } else if (e.key === 'ArrowRight') {
    nextImage()
  }
}

// Вычисляем максимальную позицию прокрутки для миниатюр
function updateMaxScrollPos() {
  if (thumbnailsContainer.value) {
    maxScrollPos.value = thumbnailsContainer.value.scrollWidth - thumbnailsContainer.value.clientWidth
  }
}

// Следим за изменением индекса текущего изображения
watch(currentIndex, (newIndex) => {
  // Прокручиваем к выбранной миниатюре, если она не видна
  if (thumbnailsContainer.value) {
    const thumbnailWidth = 80 // Ширина миниатюры + отступ
    const containerWidth = thumbnailsContainer.value.clientWidth
    const scrollPos = thumbnailsContainer.value.scrollLeft
    const thumbnailPos = newIndex * thumbnailWidth
    
    if (thumbnailPos < scrollPos) {
      // Миниатюра слева от видимой области
      thumbnailScrollPos.value = thumbnailPos
      thumbnailsContainer.value.scrollLeft = thumbnailScrollPos.value
    } else if (thumbnailPos + thumbnailWidth > scrollPos + containerWidth) {
      // Миниатюра справа от видимой области
      thumbnailScrollPos.value = thumbnailPos - containerWidth + thumbnailWidth
      thumbnailsContainer.value.scrollLeft = thumbnailScrollPos.value
    }
  }
})

// Добавляем обработчик клавиш при монтировании компонента
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('resize', updateMaxScrollPos)
  updateMaxScrollPos()
})

// Удаляем обработчик клавиш при размонтировании компонента
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('resize', updateMaxScrollPos)
})
</script>

<style scoped>
.lightbox-wrapper {
  width: 100%;
}

.main-image-container {
  position: relative;
  width: 100%;
  border-radius: 0.75rem;
  overflow: hidden;
  cursor: zoom-in;
}

.main-image {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
}

.zoom-hint {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4b5563;
}

.thumbnails {
  display: flex;
  align-items: center;
  margin-top: 0.75rem;
  position: relative;
}

.thumbnails-container {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
  flex: 1;
}

.thumbnails-container::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.thumbnail {
  flex: 0 0 auto;
  width: 72px;
  height: 72px;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s, border-color 0.2s;
}

.thumbnail:hover {
  opacity: 0.9;
}

.thumbnail.active {
  border-color: var(--accent);
  opacity: 1;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.nav-btn {
  flex: 0 0 auto;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1;
}

.nav-btn:hover:not(:disabled) {
  background-color: #f9fafb;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-btn.prev {
  margin-right: 0.5rem;
}

.nav-btn.next {
  margin-left: 0.5rem;
}

/* Лайтбокс */
.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.lightbox-content {
  position: relative;
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.close-btn {
  position: absolute;
  top: -2.5rem;
  right: 0;
  color: white;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 2;
}

.lightbox-image-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.lightbox-nav:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.3);
}

.lightbox-nav:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.lightbox-nav.prev {
  left: 1rem;
}

.lightbox-nav.next {
  right: 1rem;
}

.lightbox-counter {
  color: white;
  text-align: center;
  margin-top: 1rem;
  font-size: 0.875rem;
}
</style>
