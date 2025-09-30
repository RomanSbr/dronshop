import { computed, inject, reactive, watch } from 'vue'

const I18N_SYMBOL = Symbol('i18n')

function resolvePath(object, path) {
  return path.split('.').reduce((acc, part) => (acc && acc[part] !== undefined ? acc[part] : undefined), object)
}

function formatValue(value, params = {}) {
  if (typeof value !== 'string') return value
  return value.replace(/\{(\w+)\}/g, (_, key) => (params[key] ?? `{${key}}`))
}

function syncDomLocale(locale) {
  if (typeof document === 'undefined') return
  document.documentElement.lang = locale
}

export function createI18n({ locale = 'ru', fallbackLocale = 'en', messages = {} } = {}) {
  const state = reactive({
    locale,
    fallbackLocale,
    messages
  })

  function getMessage(key, params) {
    const current = resolvePath(state.messages[state.locale] || {}, key)
    if (current !== undefined) {
      return formatValue(current, params)
    }
    const fallback = resolvePath(state.messages[state.fallbackLocale] || {}, key)
    if (fallback !== undefined) {
      return formatValue(fallback, params)
    }
    return key
  }

  const api = {
    locale: computed(() => state.locale),
    fallbackLocale: computed(() => state.fallbackLocale),
    setLocale(next) {
      state.locale = next
      if (typeof window !== 'undefined') {
        localStorage.setItem('locale', next)
      }
      syncDomLocale(next)
    },
    t(key, params) {
      return getMessage(key, params)
    },
    loadLocaleMessages(locale, messages) {
      state.messages[locale] = messages
    }
  }

  watch(
    () => state.locale,
    (next) => {
      syncDomLocale(next)
    },
    { immediate: true }
  )

  return {
    install(app) {
      app.provide(I18N_SYMBOL, api)
      app.config.globalProperties.$t = api.t
      syncDomLocale(state.locale)
    },
    api
  }
}

export function useI18n() {
  const ctx = inject(I18N_SYMBOL)
  if (!ctx) {
    throw new Error('useI18n must be used after installing createI18n')
  }
  return ctx
}


