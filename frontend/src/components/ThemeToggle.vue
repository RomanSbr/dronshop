<template>
  <button
    @click="toggleTheme"
    class="theme-toggle"
    :aria-label="`Переключить тему: ${nextThemeName}`"
    :title="`Текущая тема: ${currentThemeName}. Нажмите для переключения на ${nextThemeName}`"
  >
    <svg v-if="currentTheme === 'light'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
    
    <svg v-else-if="currentTheme === 'dark'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
    </svg>
    
    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
    </svg>
    
    <span class="theme-label">{{ currentThemeName }}</span>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useThemeStore } from '../stores/theme'

const themeStore = useThemeStore()

const currentTheme = computed(() => themeStore.currentTheme)

const themeNames = {
  light: 'Светлая',
  dark: 'Темная',
  system: 'Системная'
}

const nextThemes = {
  light: 'dark',
  dark: 'system',
  system: 'light'
}

const currentThemeName = computed(() => themeNames[themeStore.theme])
const nextThemeName = computed(() => themeNames[nextThemes[themeStore.theme]])

function toggleTheme() {
  themeStore.toggleTheme()
}
</script>

<style scoped>
.theme-toggle {
  @apply flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-all duration-200;
}

.theme-toggle:focus {
  @apply outline-none ring-2 ring-accent-500 ring-offset-2;
}

.theme-label {
  @apply text-sm font-medium hidden sm:inline;
}

/* Темная тема */
.dark-theme .theme-toggle {
  @apply border-gray-600 bg-gray-800 text-gray-200 hover:bg-gray-700 hover:text-white;
}

/* Адаптивность */
@media (max-width: 640px) {
  .theme-toggle {
    @apply p-2;
  }
  
  .theme-label {
    @apply hidden;
  }
}

/* Анимация переключения */
.theme-toggle {
  @apply transition-colors duration-300;
}

.theme-toggle svg {
  @apply transition-transform duration-300;
}

.theme-toggle:hover svg {
  @apply transform scale-110;
}

/* Состояния доступности */
.theme-toggle:focus-visible {
  @apply ring-2 ring-accent-500 ring-offset-2 ring-offset-white;
}

.dark-theme .theme-toggle:focus-visible {
  @apply ring-offset-gray-900;
}
</style>
