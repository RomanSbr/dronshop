<template>
  <div class="app min-h-screen bg-white text-gray-800">
    <SeoMeta />
    <AppHeader />
    <main class="container mx-auto px-4 py-6 max-w-7xl">
      <router-view />
    </main>
    <SiteFooter />
    <NotificationsContainer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from './components/Header.vue'
import SiteFooter from './components/SiteFooter.vue'
import NotificationsContainer from './components/NotificationsContainer.vue'
import SeoMeta from './components/SeoMeta.vue'
import { useThemeStore } from './stores/theme'

const themeStore = useThemeStore()

// Инициализируем тему при монтировании приложения
onMounted(() => {
  themeStore.initTheme()
})
</script>

<style>
/* Глобальные стили можно оставить здесь если нужно */
</style>
