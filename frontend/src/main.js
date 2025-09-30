import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/base.css'
import './styles/dark-theme.css'
import { createI18n } from './shared/i18n'
import ru from './locales/ru.json'
import en from './locales/en.json'

const savedLocale = typeof window !== 'undefined' ? localStorage.getItem('locale') : null
const i18n = createI18n({
  locale: savedLocale || 'ru',
  fallbackLocale: 'en',
  messages: {
    ru,
    en
  }
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
