import { defineStore } from 'pinia'
import { computed, reactive, ref } from 'vue'
import api from '../shared/api'
import { useApiCacheStore } from './api-cache'

const FALLBACK_HERO_SLIDES = [
  {
    id: 'fpv',
    image: 'https://storage.yandexcloud.net/droneshop/hero-fpv.jpg',
    link: '/catalog?segment=fpv',
    titleKey: 'home.heroSlides.fpv.title',
    subtitleKey: 'home.heroSlides.fpv.subtitle',
    ctaKey: 'home.heroSlides.fpv.cta'
  },
  {
    id: 'cine',
    image: 'https://storage.yandexcloud.net/droneshop/hero-cinema.jpg',
    link: '/catalog?segment=cinema',
    titleKey: 'home.heroSlides.cine.title',
    subtitleKey: 'home.heroSlides.cine.subtitle',
    ctaKey: 'home.heroSlides.cine.cta'
  },
  {
    id: 'micro',
    image: 'https://storage.yandexcloud.net/droneshop/hero-micro.jpg',
    link: '/catalog?segment=micro',
    titleKey: 'home.heroSlides.micro.title',
    subtitleKey: 'home.heroSlides.micro.subtitle',
    ctaKey: 'home.heroSlides.micro.cta'
  }
]

const FALLBACK_PROMO_BLOCKS = [
  {
    id: 'training',
    image: 'https://storage.yandexcloud.net/droneshop/hero-training.jpg',
    link: '/services/training',
    titleKey: 'home.promoBlocks.training.title',
    descriptionKey: 'home.promoBlocks.training.description',
    ctaKey: 'home.promoBlocks.training.cta'
  },
  {
    id: 'service',
    image: 'https://storage.yandexcloud.net/droneshop/hero-service.jpg',
    link: '/services/service-center',
    titleKey: 'home.promoBlocks.service.title',
    descriptionKey: 'home.promoBlocks.service.description',
    ctaKey: 'home.promoBlocks.service.cta'
  }
]

function createAsyncState() {
  return reactive({
    status: 'idle',
    error: null,
    loaded: false
  })
}

export const useContentStore = defineStore('content', () => {
  const apiCacheStore = useApiCacheStore()

  const heroSlides = ref([])
  const heroState = createAsyncState()

  const promoBlocks = ref([])
  const promoState = createAsyncState()

  async function fetchHeroSlides({ force = false } = {}) {
    if (heroState.loaded && !force) return heroSlides.value

    heroState.status = 'loading'
    heroState.error = null

    try {
      if (force) apiCacheStore.clearCacheItem('content-hero')

      const data = await apiCacheStore.cachedApiCall(
        async () => {
          const response = await api.get('/content/hero')
          return response.data
        },
        'content-hero'
      )

      heroSlides.value = Array.isArray(data) && data.length ? data : FALLBACK_HERO_SLIDES
    } catch (error) {
      heroSlides.value = FALLBACK_HERO_SLIDES
      heroState.error = error
    } finally {
      heroState.status = 'success'
      heroState.loaded = true
    }

    return heroSlides.value
  }

  async function fetchPromoBlocks({ force = false } = {}) {
    if (promoState.loaded && !force) return promoBlocks.value

    promoState.status = 'loading'
    promoState.error = null

    try {
      if (force) apiCacheStore.clearCacheItem('content-promo')

      const data = await apiCacheStore.cachedApiCall(
        async () => {
          const response = await api.get('/content/promo')
          return response.data
        },
        'content-promo'
      )

      promoBlocks.value = Array.isArray(data) && data.length ? data : FALLBACK_PROMO_BLOCKS
    } catch (error) {
      promoBlocks.value = FALLBACK_PROMO_BLOCKS
      promoState.error = error
    } finally {
      promoState.status = 'success'
      promoState.loaded = true
    }

    return promoBlocks.value
  }

  const isHeroLoading = computed(() => heroState.status === 'loading')
  const isPromoLoading = computed(() => promoState.status === 'loading')

  return {
    heroSlides,
    heroState,
    isHeroLoading,
    fetchHeroSlides,
    promoBlocks,
    promoState,
    isPromoLoading,
    fetchPromoBlocks
  }
})
