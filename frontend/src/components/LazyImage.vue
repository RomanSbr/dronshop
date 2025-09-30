<template>
  <div class="lazy-image" :class="{ 'loaded': isLoaded, 'error': hasError }">
    <!-- Blur placeholder -->
    <div 
      v-if="showPlaceholder && !isLoaded" 
      class="placeholder"
      :style="{ 
        backgroundColor: placeholderColor,
        backgroundImage: `url('${placeholderSrc}')` 
      }"
    />
    
    <!-- РћСЃРЅРѕРІРЅРѕРµ РёР·РѕР±СЂР°Р¶РµРЅРёРµ -->
    <img
      ref="imageRef"
      :src="isLoaded ? src : undefined"
      :data-src="src"
      :alt="alt"
      :width="width"
      :height="height"
      :class="imgClass"
      :style="imgStyle"
      @load="handleLoad"
      @error="handleError"
      v-bind="$attrs"
    />
    
    <!-- Fallback РїСЂРё РѕС€РёР±РєРµ -->
    <div 
      v-if="hasError && fallbackSrc" 
      class="fallback"
      :style="{ backgroundImage: `url('${fallbackSrc}')` }"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: ''
  },
  width: {
    type: [String, Number],
    default: null
  },
  height: {
    type: [String, Number],
    default: null
  },
  threshold: {
    type: Number,
    default: 0
  },
  rootMargin: {
    type: String,
    default: '0px 0px 100px 0px'
  },
  placeholderSrc: {
    type: String,
    default: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PC9zdmc+'
  },
  placeholderColor: {
    type: String,
    default: '#f3f4f6'
  },
  fallbackSrc: {
    type: String,
    default: null
  },
  eager: {
    type: Boolean,
    default: false
  },
  imgClass: {
    type: [String, Object, Array],
    default: ''
  },
  imgStyle: {
    type: [String, Object],
    default: ''
  }
})

const emit = defineEmits(['load', 'error'])

const imageRef = ref(null)
const isLoaded = ref(props.eager)
const hasError = ref(false)
const observer = ref(null)

const showPlaceholder = computed(() => {
  return !isLoaded.value && props.placeholderSrc
})

// РћР±СЂР°Р±РѕС‚С‡РёРє СѓСЃРїРµС€РЅРѕР№ Р·Р°РіСЂСѓР·РєРё
function handleLoad() {
  isLoaded.value = true
  hasError.value = false
  emit('load')
}

// РћР±СЂР°Р±РѕС‚С‡РёРє РѕС€РёР±РєРё Р·Р°РіСЂСѓР·РєРё
function handleError() {
  hasError.value = true
  emit('error')
}

// РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ Intersection Observer
function initObserver() {
  if (typeof IntersectionObserver === 'undefined' || props.eager) {
    // Р•СЃР»Рё IntersectionObserver РЅРµ РїРѕРґРґРµСЂР¶РёРІР°РµС‚СЃСЏ РёР»Рё eager=true, Р·Р°РіСЂСѓР¶Р°РµРј СЃСЂР°Р·Сѓ
    isLoaded.value = true
    return
  }

  observer.value = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          loadImage()
          observer.value.unobserve(entry.target)
        }
      })
    },
    {
      threshold: props.threshold,
      rootMargin: props.rootMargin
    }
  )

  if (imageRef.value) {
    observer.value.observe(imageRef.value)
  }
}

// Р—Р°РіСЂСѓР·РєР° РёР·РѕР±СЂР°Р¶РµРЅРёСЏ
function loadImage() {
  if (isLoaded.value) return

  const img = new Image()
  img.src = props.src
  img.onload = handleLoad
  img.onerror = handleError
}

// РћС‡РёСЃС‚РєР° observer
function cleanupObserver() {
  if (observer.value) {
    observer.value.disconnect()
    observer.value = null
  }
}

// РџСЂРё РјРѕРЅС‚РёСЂРѕРІР°РЅРёРё
onMounted(() => {
  if (props.eager) {
    loadImage()
  } else {
    initObserver()
  }
})

// РџСЂРё СЂР°Р·РјРѕРЅС‚РёСЂРѕРІР°РЅРёРё
onUnmounted(() => {
  cleanupObserver()
})

// РџСЂРё РёР·РјРµРЅРµРЅРёРё src
watch(() => props.src, (newSrc, oldSrc) => {
  if (newSrc !== oldSrc) {
    isLoaded.value = false
    hasError.value = false
    cleanupObserver()
    
    if (props.eager) {
      loadImage()
    } else {
      setTimeout(() => {
        if (imageRef.value) {
          initObserver()
        }
      }, 0)
    }
  }
})
</script>

<style scoped>
.lazy-image {
  position: relative;
  overflow: hidden;
}

.lazy-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s ease;
}

.lazy-image:not(.loaded) img {
  opacity: 0;
}

.lazy-image.loaded img {
  opacity: 1;
}

.placeholder,
.fallback {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  filter: blur(10px);
  transition: opacity 0.3s ease;
}

.lazy-image.loaded .placeholder,
.lazy-image.loaded .fallback {
  opacity: 0;
  pointer-events: none;
}

.fallback {
  filter: none;
  background-color: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* РђРЅРёРјР°С†РёСЏ shimmer РґР»СЏ placeholder */
.placeholder {
  background: linear-gradient(
    90deg,
    var(--bg-tertiary) 0%,
    var(--bg-secondary) 50%,
    var(--bg-tertiary) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* РђРґР°РїС‚РёРІРЅС‹Рµ СѓР»СѓС‡С€РµРЅРёСЏ */
@media (prefers-reduced-motion: reduce) {
  .lazy-image img,
  .placeholder,
  .fallback {
    transition: none;
  }
  
  .placeholder {
    animation: none;
  }
}
</style>

