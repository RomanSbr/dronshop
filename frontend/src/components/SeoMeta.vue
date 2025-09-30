<template>
  <!-- Этот компонент не рендерит видимый контент, только управляет мета-тегами -->
</template>

<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  title: {
    type: String,
    default: 'DronShop - Магазин дронов и комплектующих'
  },
  description: {
    type: String,
    default: 'Интернет-магазин дронов и комплектующих с доставкой по всей России. Качественные товары, быстрая доставка, профессиональная консультация.'
  },
  keywords: {
    type: String,
    default: 'дроны, квадрокоптеры, FPV, радиоуправление, комплектующие для дронов, аккумуляторы для дронов, моторы для дронов'
  },
  image: {
    type: String,
    default: '/brand.svg'
  },
  canonical: {
    type: String,
    default: ''
  }
})

const route = useRoute()

// Функция для обновления мета-тегов
function updateMetaTags() {
  const { title, description, keywords, image, canonical } = props
  
  // Title
  document.title = title
  
  // Meta description
  let metaDescription = document.querySelector('meta[name="description"]')
  if (!metaDescription) {
    metaDescription = document.createElement('meta')
    metaDescription.name = 'description'
    document.head.appendChild(metaDescription)
  }
  metaDescription.content = description
  
  // Meta keywords
  let metaKeywords = document.querySelector('meta[name="keywords"]')
  if (!metaKeywords) {
    metaKeywords = document.createElement('meta')
    metaKeywords.name = 'keywords'
    document.head.appendChild(metaKeywords)
  }
  metaKeywords.content = keywords
  
  // Open Graph
  const ogTags = [
    { property: 'og:title', content: title },
    { property: 'og:description', content: description },
    { property: 'og:image', content: image },
    { property: 'og:url', content: window.location.href },
    { property: 'og:type', content: 'website' }
  ]
  
  ogTags.forEach(tag => {
    let metaTag = document.querySelector(`meta[property="${tag.property}"]`)
    if (!metaTag) {
      metaTag = document.createElement('meta')
      metaTag.setAttribute('property', tag.property)
      document.head.appendChild(metaTag)
    }
    metaTag.content = tag.content
  })
  
  // Twitter Card
  const twitterTags = [
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: title },
    { name: 'twitter:description', content: description },
    { name: 'twitter:image', content: image }
  ]
  
  twitterTags.forEach(tag => {
    let metaTag = document.querySelector(`meta[name="${tag.name}"]`)
    if (!metaTag) {
      metaTag = document.createElement('meta')
      metaTag.name = tag.name
      document.head.appendChild(metaTag)
    }
    metaTag.content = tag.content
  })
  
  // Canonical link
  if (canonical) {
    let linkCanonical = document.querySelector('link[rel="canonical"]')
    if (!linkCanonical) {
      linkCanonical = document.createElement('link')
      linkCanonical.rel = 'canonical'
      document.head.appendChild(linkCanonical)
    }
    linkCanonical.href = canonical
  }
}

// Обновляем мета-теги при монтировании и изменении пропсов
updateMetaTags()
watch(() => props, updateMetaTags, { deep: true })

// Обновляем мета-теги при изменении маршрута
watch(() => route.fullPath, () => {
  setTimeout(updateMetaTags, 100) // Небольшая задержка для обновления DOM
})
</script>
