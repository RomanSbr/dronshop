<template>
  <header class="site-header glass-effect sticky top-0 z-50 border-b border-white/10 backdrop-blur-xl">
    <div class="topbar hidden md:block bg-gradient-to-r from-accent-900/80 to-accent-800/80 text-white/90">
      <div class="container flex justify-between items-center py-2">
        <div class="flex gap-6 text-xs font-medium">
          <router-link to="/catalog" class="hover:text-white transition-colors duration-200">Каталог</router-link>
          <router-link to="/new" class="hover:text-white transition-colors duration-200">Новинки</router-link>
          <router-link to="/delivery" class="hover:text-white transition-colors duration-200">Доставка</router-link>
          <router-link to="/payment" class="hover:text-white transition-colors duration-200">Оплата</router-link>
          <router-link to="/about" class="hover:text-white transition-colors duration-200">О нас</router-link>
          <router-link to="/contacts" class="hover:text-white transition-colors duration-200">Контакты</router-link>
        </div>
        <div class="flex gap-4 text-xs items-center">
          <a href="https://t.me/" target="_blank" rel="noreferrer" class="hover:text-white transition-colors duration-200 flex items-center gap-1">
            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm.14 19.018c-.237 0-.47-.033-.696-.08l-3.26.93 1.376-3.242a5.077 5.077 0 01-.754-2.685c0-2.834 2.326-5.133 5.196-5.133 2.87 0 5.196 2.3 5.196 5.133 0 2.833-2.325 5.132-5.195 5.132h-.002c-.423 0-.833-.05-1.228-.145l-1.757.945.922-1.854z"/></svg>
            <span class="hidden lg:inline">Мы в TG</span>
            <span class="lg:hidden">TG</span>
          </a>
          <a href="tel:+79990000000" class="hover:text-white transition-colors duration-200 flex items-center gap-1">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
            +7 (999) 000-00-00
          </a>
        </div>
      </div>
    </div>

    <div class="mid py-3">
      <div class="container">
        <div class="midline flex items-center justify-between gap-4 md:gap-8">
          <button class="mobile-menu-btn md:hidden w-10 h-10 rounded-xl bg-white/10 backdrop-blur-sm border border-white/10 flex items-center justify-center hover:bg-white/20 transition-all duration-300 group" @click="mobileMenuOpen = !mobileMenuOpen" :aria-expanded="mobileMenuOpen" aria-label="Меню" aria-controls="mobile-menu">
            <div class="w-5 h-5 relative">
              <span class="absolute top-1/2 left-0 w-full h-0.5 bg-current transform -translate-y-1/2 transition-all duration-300" :class="{ 'rotate-45 translate-y-0': mobileMenuOpen }"></span>
              <span class="absolute top-1/2 left-0 w-full h-0.5 bg-current transform -translate-y-1/2 transition-all duration-300" :class="{ 'opacity-0': mobileMenuOpen }"></span>
              <span class="absolute top-1/2 left-0 w-full h-0.5 bg-current transform -translate-y-1/2 transition-all duration-300" :class="{ '-rotate-45 translate-y-0': mobileMenuOpen }"></span>
            </div>
          </button>

          <router-link to="/" class="brand flex items-center">
            <img src="/brand.svg" alt="GLORYAIR" class="h-9 md:h-10 transition-transform duration-300" />
          </router-link>

          <CatalogDropdown class="hidden md:block" />

          <div class="search flex-1 max-w-md">
            <div class="relative">
              <input v-model="q" @keyup.enter="goSearch" class="search-input w-full pl-12 pr-4 py-3 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 text-white placeholder-white/60 focus:bg-white/10 focus:border-accent-400 focus:ring-2 focus:ring-accent-400/20 transition-all duration-300" placeholder="Поиск по каталогу..." aria-label="Поиск" />
              <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-4 h-4 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              <button @click="goSearch" class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-accent-600 hover:bg-accent-700 text-white px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-300" aria-label="Поиск">Найти</button>
            </div>
          </div>

          <div class="icons flex flex-nowrap items-center gap-2 md:gap-3">
            <router-link to="/favorites" class="icon-action group relative p-3 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 hover:border-accent-400/30 transition-all duration-300" :class="{ 'text-accent-400': favoritesCount > 0 }" aria-label="Избранное">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
            </router-link>

            <div class="relative group">
              <router-link :to="isAuthenticated ? '/profile' : '/auth'" :title="isAuthenticated ? 'Профиль' : 'Войти'" class="icon-action p-3 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 hover:border-accent-400/30 transition-all duration-300" aria-label="Профиль">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                <span class="hidden md:inline ml-2 text-sm font-medium">{{ isAuthenticated ? 'Профиль' : 'Войти' }}</span>
              </router-link>
              <div v-if="isAuthenticated" class="absolute right-0 mt-2 w-48 bg-white/95 backdrop-blur-xl rounded-xl shadow-2xl py-2 z-10 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300">
                <router-link to="/profile" class="block px-4 py-2 text-sm text-gray-800 hover:bg-accent-50 hover:text-accent-600 transition-colors duration-200">Профиль</router-link>
                <router-link v-if="isAdmin" to="/admin" class="block px-4 py-2 text-sm text-gray-800 hover:bg-accent-50 hover:text-accent-600 transition-colors duration-200">Админка</router-link>
                <div class="my-1 h-px bg-gray-200/60"></div>
                <button @click="logout" class="w-full text-left block px-4 py-2 text-sm text-gray-800 hover:bg-red-50 hover:text-red-600 transition-colors duration-200">Выйти</button>
              </div>
            </div>

            <router-link to="/cart" class="icon-action group relative p-3 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 hover:border-accent-400/30 transition-all duration-300" :class="{ 'text-accent-400': cartItemsCount > 0 }" aria-label="Корзина">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
              <span v-if="cartItemsCount > 0" class="absolute -top-1 -right-1 bg-accent-600 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full shadow-lg">{{ cartItemsCount }}</span>
            </router-link>

            <ThemeToggle />
          </div>
        </div>
      </div>
    </div>

    <div id="mobile-menu" class="mobile-menu fixed inset-0 bg-black/80 backdrop-blur-xl z-50 transition-opacity duration-500" :class="{ 'opacity-100 pointer-events-auto': mobileMenuOpen, 'opacity-0 pointer-events-none': !mobileMenuOpen }" @click.self="mobileMenuOpen = false" role="dialog" aria-modal="true" :aria-hidden="!mobileMenuOpen">
      <div class="mobile-menu-content absolute top-0 left-0 h-full w-80 bg-white/95 backdrop-blur-xl transform transition-transform duration-500 ease-out-back" :class="{ 'translate-x-0': mobileMenuOpen, '-translate-x-full': !mobileMenuOpen }">
        <div class="mobile-menu-header flex items-center justify-between p-6 border-b border-gray-100/20">
          <h3 class="text-xl font-bold gradient-text">Меню</h3>
          <button @click="mobileMenuOpen = false" class="close-btn w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors duration-300" aria-label="Закрыть">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <div class="mobile-menu-sections overflow-y-auto h-full pb-20">
          <div class="mobile-menu-section p-6 border-b border-gray-100/20">
            <div class="mobile-menu-title text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wide">Категории</div>
            <div class="mobile-menu-links space-y-3">
              <router-link v-for="category in categories" :key="category.id" :to="{ path: '/catalog', query: { category: category.id } }" @click="mobileMenuOpen = false" class="mobile-menu-link block text-gray-800 hover:text-accent-600 transition-colors duration-200 py-2 font-medium">{{ category.name }}</router-link>
            </div>
          </div>

          <div class="mobile-menu-section p-6 border-b border-gray-100/20">
            <div class="mobile-menu-title text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wide">Компания</div>
            <div class="mobile-menu-links space-y-3">
              <router-link to="/new" @click="mobileMenuOpen = false" class="mobile-menu-link block text-gray-800 hover:text-accent-600 transition-colors duration-200 py-2 font-medium">Новинки</router-link>
              <router-link to="/delivery" @click="mobileMenuOpen = false" class="mobile-menu-link block text-gray-800 hover:text-accent-600 transition-colors duration-200 py-2 font-medium">Доставка</router-link>
              <router-link to="/payment" @click="mobileMenuOpen = false" class="mobile-menu-link block text-gray-800 hover:text-accent-600 transition-colors duration-200 py-2 font-medium">Оплата</router-link>
              <router-link to="/about" @click="mobileMenuOpen = false" class="mobile-menu-link block text-gray-800 hover:text-accent-600 transition-colors duration-200 py-2 font-medium">О нас</router-link>
              <router-link to="/contacts" @click="mobileMenuOpen = false" class="mobile-menu-link block text-gray-800 hover:text-accent-600 transition-colors duration-200 py-2 font-medium">Контакты</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'
import { useFavoritesStore } from '../stores/favorites'
import { useApiCacheStore } from '../stores/api-cache'
import ThemeToggle from './ThemeToggle.vue'
import CatalogDropdown from './catalog/CatalogDropdown.vue'
import api from '../shared/api'

const q = ref('')
const router = useRouter()
const cartStore = useCartStore()
const favoritesStore = useFavoritesStore()
const apiCacheStore = useApiCacheStore()
const mobileMenuOpen = ref(false)
const categories = ref([])
const isAdmin = ref(false)

function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1]
    if (!base64Url) return null
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64.padEnd(base64.length + (4 - (base64.length % 4)) % 4, '='))
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (e) {
    return null
  }
}

function isAccessTokenValid() {
  const t = localStorage.getItem('accessToken')
  if (!t) return false
  const payload = parseJwt(t)
  if (!payload || !payload.exp) return false
  const now = Math.floor(Date.now() / 1000)
  return payload.exp > now
}

const authState = ref(isAccessTokenValid())
const isAuthenticated = computed(() => authState.value)

function handleAuthChanged() {
  authState.value = isAccessTokenValid()
  if (!authState.value) {
    isAdmin.value = false
  } else {
    checkAdminRole()
  }
}

function logout() {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  authState.value = false
  isAdmin.value = false
  window.dispatchEvent(new Event('auth-changed'))
  router.push('/auth')
}

const cartItemsCount = computed(() => cartStore.totalItems)
const favoritesCount = computed(() => favoritesStore.count)

async function checkAdminRole() {
  try {
    const { data } = await api.get('/auth/me')
    isAdmin.value = Array.isArray(data?.roles) && data.roles.includes('admin')
  } catch (e) {
    isAdmin.value = false
  }
}

function goSearch() {
  if (!q.value.trim()) return
  router.push({ path: '/catalog', query: { q: q.value } })
  q.value = ''
  mobileMenuOpen.value = false
}

async function loadCategories() {
  try {
    const fetchCategories = async () => (await api.get('/categories')).data
    categories.value = await apiCacheStore.cachedApiCall(fetchCategories, 'header-categories')
  } catch (error) {
    categories.value = []
  }
}

function toggleBodyScroll(isLocked) {
  document.body.style.overflow = isLocked ? 'hidden' : ''
}

watch(mobileMenuOpen, (v) => toggleBodyScroll(v))

onMounted(() => {
  loadCategories()
  if (isAuthenticated.value) checkAdminRole()
  window.addEventListener('auth-changed', handleAuthChanged)
  window.addEventListener('storage', handleAuthChanged)
})

onUnmounted(() => {
  window.removeEventListener('auth-changed', handleAuthChanged)
  window.removeEventListener('storage', handleAuthChanged)
})
</script>

<style scoped>
.site-header { @apply bg-white/80 backdrop-blur-xl border-b border-white/20; }
.topbar { @apply bg-gradient-to-r from-accent-900/80 to-accent-800/80; }
.mid { @apply py-3; }
.midline { @apply flex items-center justify-between gap-4 md:gap-8; }
.brand img { @apply h-9 md:h-10 transition-transform duration-300; }
.search-input { @apply bg-white border border-gray-300 text-gray-800 placeholder-gray-400 focus:bg-white focus:border-accent-400 focus:ring-2 focus:ring-accent-400/20; }
:deep(.dark-theme) .search-input { @apply bg-white/5 backdrop-blur-sm border border-white/10 text-white placeholder-white/60 focus:bg-white/10 focus:border-accent-400; }
.icon-action { @apply inline-flex items-center justify-center shrink-0 bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 hover:border-accent-400/30 transition-all duration-300; }
.mobile-menu { @apply bg-black/80 backdrop-blur-xl; }
.mobile-menu-content { @apply bg-white/95 backdrop-blur-xl; }
.mobile-menu-header { @apply border-b border-gray-100/20; }
.mobile-menu-section { @apply border-b border-gray-100/20; }
.mobile-menu-link { @apply text-gray-800 hover:text-accent-600 transition-colors duration-200; }
@media (max-width: 768px) {
  .search { @apply order-last mt-4; }
  .midline { @apply flex-wrap; }
  .icons { @apply order-first; }
}
@media (max-width: 640px) {
  .mid { @apply py-2; }
  .search-input { @apply py-2 text-sm; }
  .icon-action { @apply p-2; }
  .icon-action span:not([class*="absolute"]) { @apply hidden; }
}
</style>
