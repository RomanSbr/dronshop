<template>
  <section class="auth-page">
    <div class="auth-shell">
      <div class="auth-card">
        <aside class="auth-aside" aria-hidden="true">
          <span class="auth-eyebrow">{{ t('auth.heroLabel') }}</span>
          <h1 class="auth-title">{{ t('auth.heroTitle') }}</h1>
          <p class="auth-subtitle">{{ t('auth.heroSubtitle') }}</p>

          <ul class="auth-highlights">
            <li v-for="item in highlights" :key="item" class="auth-highlight">
              <span class="bullet"></span>
              <span>{{ item }}</span>
            </li>
          </ul>

          <div class="auth-meta">
            <img src="/brand.svg" alt="GLORYAIR" class="auth-meta-logo" />
            <span>{{ t('auth.heroMeta') }}</span>
          </div>
        </aside>

        <div class="auth-main">
          <div class="auth-header">
            <h2 class="auth-heading">{{ t('auth.loginTitle') }}</h2>
            <p class="auth-description">{{ t('auth.loginSubtitle') }}</p>
          </div>

          <div class="auth-tabs" role="tablist">
            <button
              class="auth-tab"
              :class="{ active: mode === 'sms' }"
              role="tab"
              type="button"
              :aria-selected="mode === 'sms'"
              @click="switchMode('sms')"
            >
              {{ t('auth.smsTab') }}
            </button>
            <button
              class="auth-tab"
              :class="{ active: mode === 'password' }"
              role="tab"
              type="button"
              :aria-selected="mode === 'password'"
              @click="switchMode('password')"
            >
              {{ t('auth.passwordTab') }}
            </button>
          </div>

          <form v-if="mode === 'sms' && !isVerifyStep" class="auth-form" @submit.prevent="requestCode">
            <label class="field">
              <span class="field-label">{{ t('auth.phoneLabel') }}</span>
              <input
                id="phone"
                v-model="phone"
                type="tel"
                class="field-input"
                :placeholder="t('auth.phonePlaceholder')"
                autocomplete="tel"
                required
              />
            </label>

            <button class="btn-primary" type="submit" :disabled="loading || !isValidPhone">
              <span v-if="loading">{{ t('auth.loading') }}</span>
              <span v-else>{{ t('auth.sendCode') }}</span>
            </button>

            <p v-if="debugCode" class="debug-pill">
              <span class="debug-label">{{ t('auth.debugCode') }}:</span>
              <span class="debug-value">{{ debugCode }}</span>
            </p>
          </form>

          <form v-else-if="mode === 'sms'" class="auth-form" @submit.prevent="verifyCode">
            <label class="field">
              <span class="field-label">{{ t('auth.codeLabel') }}</span>
              <input
                id="code"
                v-model="code"
                inputmode="numeric"
                class="field-input"
                :placeholder="t('auth.codePlaceholder')"
                required
              />
            </label>

            <div class="form-actions">
              <button class="btn-primary" type="submit" :disabled="loading || !code">
                <span v-if="loading">{{ t('auth.loading') }}</span>
                <span v-else>{{ t('auth.verify') }}</span>
              </button>
              <button class="btn-secondary" type="button" @click="resetForm">{{ t('auth.reset') }}</button>
            </div>
          </form>

          <form v-else class="auth-form" @submit.prevent="loginPassword">
            <div class="field-group">
              <label class="field field-select">
                <span class="sr-only">{{ t('auth.loginIdentifier') }}</span>
                <select v-model="pwdType" class="field-input select">
                  <option value="email">E-mail</option>
                  <option value="phone">{{ t('auth.phoneLabel') }}</option>
                </select>
              </label>
              <label class="field flex-1">
                <span class="sr-only">{{ t('auth.loginIdentifier') }}</span>
                <input
                  v-model="pwdValue"
                  :type="pwdType === 'email' ? 'email' : 'tel'"
                  class="field-input"
                  :placeholder="pwdType === 'email' ? t('auth.emailPlaceholder') : t('auth.phonePlaceholder')"
                  autocomplete="username"
                  required
                />
              </label>
            </div>

            <label class="field">
              <span class="field-label">{{ t('auth.passwordLabel') }}</span>
              <input
                v-model="pwdPassword"
                type="password"
                class="field-input"
                :placeholder="t('auth.passwordPlaceholder')"
                autocomplete="current-password"
                required
              />
            </label>

            <button class="btn-primary" type="submit" :disabled="loading || !pwdValue || !pwdPassword">
              <span v-if="loading">{{ t('auth.loading') }}</span>
              <span v-else>{{ t('auth.passwordSubmit') }}</span>
            </button>

            <p class="auth-footnote">
              {{ t('auth.noAccount') }}
              <router-link to="/register" class="auth-link">{{ t('auth.register') }}</router-link>
            </p>
          </form>

          <p v-if="error" class="auth-error" role="alert">{{ error }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import api from '../shared/api'
import { useI18n } from '../shared/i18n'

const router = useRouter()
const { t } = useI18n()

const mode = ref('sms')
const phone = ref('')
const code = ref('')
const loading = ref(false)
const error = ref('')
const debugCode = ref('')
const isVerifyStep = ref(false)

const pwdType = ref('email')
const pwdValue = ref('')
const pwdPassword = ref('')

const highlights = computed(() => [
  t('auth.highlightDelivery'),
  t('auth.highlightSupport'),
  t('auth.highlightBonus')
])

const isValidPhone = computed(() => phone.value.trim().length >= 10)

function switchMode(nextMode) {
  if (mode.value === nextMode) return
  mode.value = nextMode
  error.value = ''
  loading.value = false
}

async function requestCode() {
  if (!isValidPhone.value || loading.value) return

  error.value = ''
  loading.value = true

  try {
    const { data } = await api.post('/auth/request-code', { phone: phone.value })
    debugCode.value = data.debugCode
    isVerifyStep.value = true
  } catch (err) {
    console.error('Code request failed', err)
    error.value = t('auth.requestError')
  } finally {
    loading.value = false
  }
}

async function verifyCode() {
  if (!code.value || loading.value) return

  error.value = ''
  loading.value = true

  try {
    const { data } = await api.post('/auth/register', {
      phone: phone.value,
      verificationCode: code.value
    })

    localStorage.setItem('accessToken', data.accessToken)
    localStorage.setItem('refreshToken', data.refreshToken)

    window.dispatchEvent(new Event('auth-changed'))

    router.push('/profile')
  } catch (err) {
    console.error('Verification failed', err)
    error.value = err?.response?.status === 400 ? t('auth.verifyError') : t('auth.unknownError')
  } finally {
    loading.value = false
  }
}

function resetForm() {
  isVerifyStep.value = false
  code.value = ''
  error.value = ''
}

async function loginPassword() {
  if (loading.value) return
  error.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/auth/login-password', {
      contact_type: pwdType.value,
      contact_value: pwdValue.value.trim(),
      password: pwdPassword.value
    })
    localStorage.setItem('accessToken', data.accessToken)
    localStorage.setItem('refreshToken', data.refreshToken)
    window.dispatchEvent(new Event('auth-changed'))
    router.push('/profile')
  } catch (e) {
    error.value = e?.response?.data?.detail || t('auth.passwordError')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { @apply py-10 lg:py-16 bg-gradient-to-b from-slate-50 via-white to-white; }
.auth-shell { @apply container mx-auto px-4; }
.auth-card { @apply grid gap-0 bg-white/90 backdrop-blur-md border border-white/60 shadow-2xl rounded-3xl overflow-hidden lg:grid-cols-[1fr,minmax(0,1fr)]; }
.auth-aside { @apply hidden lg:flex flex-col gap-8 bg-gradient-to-br from-accent-700 to-accent-500 text-white p-10 relative; }
.auth-eyebrow { @apply text-xs uppercase tracking-[0.3em] text-white/70; }
.auth-title { @apply text-3xl font-semibold; }
.auth-subtitle { @apply text-base text-white/80 max-w-sm; }
.auth-highlights { @apply space-y-3; }
.auth-highlight { @apply flex items-start gap-3 text-sm text-white/85; }
.auth-highlight .bullet { @apply mt-1 h-2 w-2 rounded-full bg-white/80 shadow; }
.auth-meta { @apply flex items-center gap-3 text-sm text-white/80; }
.auth-meta-logo { @apply h-6 w-auto drop-shadow; }

.auth-main { @apply p-6 sm:p-8 lg:p-10 flex flex-col gap-6; }
.auth-header { @apply space-y-1; }
.auth-heading { @apply text-2xl font-semibold text-slate-900; }
.auth-description { @apply text-sm text-slate-500; }

.auth-tabs { @apply inline-flex items-center justify-start p-1 bg-slate-100 rounded-full shadow-inner w-full max-w-md; }
.auth-tab { @apply flex-1 rounded-full px-4 py-2 text-sm font-semibold text-slate-500 transition-all duration-200; }
.auth-tab.active { @apply bg-white text-slate-900 shadow; }

.auth-form { @apply space-y-4; }
.field { @apply flex flex-col gap-1; }
.field-group { @apply flex flex-col sm:flex-row gap-3; }
.field-label { @apply text-xs font-semibold uppercase tracking-wide text-slate-500; }
.field-input { @apply w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-800 shadow-sm focus:border-accent-400 focus:outline-none focus:ring-2 focus:ring-accent-200 transition; }
.field-select { @apply sm:w-40; }
.field-input.select {
  @apply appearance-none pr-8;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23334155'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-size: 18px;
  background-position: calc(100% - 12px) center;
}

.btn-primary { @apply w-full inline-flex items-center justify-center rounded-xl bg-accent-600 text-white font-semibold py-3 px-4 shadow hover:bg-accent-700 focus:outline-none focus:ring-2 focus:ring-accent-200 disabled:opacity-60 disabled:cursor-not-allowed transition; }
.btn-secondary { @apply inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 font-semibold py-3 px-4 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-accent-200 transition; }
.form-actions { @apply flex flex-col sm:flex-row gap-3; }
.auth-footnote { @apply text-sm text-slate-500 text-center; }
.auth-link { @apply text-accent-600 hover:underline font-medium; }
.auth-error { @apply text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl px-4 py-3; }
.debug-pill { @apply text-xs inline-flex items-center gap-2 bg-slate-100 text-slate-600 rounded-full px-3 py-1; }
.debug-label { @apply font-medium; }
.debug-value { @apply font-semibold; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }

@media (max-width: 1023px) {
  .auth-card { @apply rounded-2xl; }
}
</style>
