<template>
  <div class="auth-page">
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 class="text-2xl font-bold mb-4 text-center">Вход</h1>

        <div class="tabs mb-5">
          <button class="tab" :class="{active: mode==='sms'}" @click="mode='sms'">По телефону (СМС)</button>
          <button class="tab" :class="{active: mode==='password'}" @click="mode='password'">E-mail/телефон + пароль</button>
        </div>

        <!-- SMS login -->
        <div v-if="mode==='sms' && !isVerifyStep" class="phone-step">
          <div class="mb-4">
            <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('auth.phoneLabel') }}
            </label>
            <input
              id="phone"
              v-model="phone"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
              :placeholder="t('auth.phonePlaceholder')"
            />
          </div>

          <button
            class="w-full btn-primary mb-4"
            :disabled="loading || !isValidPhone"
            @click="requestCode"
          >
            <span v-if="loading">{{ t('auth.loading') }}</span>
            <span v-else>{{ t('auth.sendCode') }}</span>
          </button>

          <div v-if="debugCode" class="bg-gray-100 p-3 rounded-md text-center mb-4">
            <span class="text-sm text-gray-600">{{ t('auth.debugCode') }}:</span>
            <span class="font-bold ml-2">{{ debugCode }}</span>
          </div>
        </div>

        <div v-else-if="mode==='sms'" class="verify-step">
          <div class="mb-4">
            <label for="code" class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('auth.codeLabel') }}
            </label>
            <input
              id="code"
              v-model="code"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
              :placeholder="t('auth.codePlaceholder')"
            />
          </div>

          <div class="flex gap-3 mb-4">
            <button
              class="flex-1 btn-primary"
              :disabled="loading || !code"
              @click="verifyCode"
            >
              <span v-if="loading">{{ t('auth.loading') }}</span>
              <span v-else>{{ t('auth.verify') }}</span>
            </button>

            <button class="btn-secondary" @click="resetForm">
              {{ t('auth.reset') }}
            </button>
          </div>
        </div>

        <!-- Password login -->
        <div v-else class="pwd-step space-y-4">
          <div class="flex gap-2">
            <select v-model="pwdType" class="w-36 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent">
              <option value="email">E-mail</option>
              <option value="phone">Телефон</option>
            </select>
            <input v-model="pwdValue" :type="pwdType==='email' ? 'email' : 'tel'" class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent" :placeholder="pwdType==='email' ? 'email@domain.com' : '+7XXXXXXXXXX'" />
          </div>
          <div>
            <input v-model="pwdPassword" type="password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent" placeholder="Пароль" />
          </div>
          <button class="w-full btn-primary" :disabled="loading || !pwdValue || !pwdPassword" @click="loginPassword">Войти</button>
          <div class="text-center text-sm">
            Нет аккаунта? <router-link to="/register" class="text-accent hover:underline">Регистрация</router-link>
          </div>
        </div>

        <div v-if="error" class="error-message p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm mt-4">
          {{ error }}
        </div>

        <div class="text-center mt-6">
          <router-link to="/auth/dev" class="text-sm text-gray-500 hover:text-accent">
            {{ t('auth.devLink') }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../shared/api'
import { useI18n } from '../shared/i18n'

const router = useRouter()
const { t } = useI18n()

const mode = ref('sms') // 'sms' | 'password'
const phone = ref('')
const code = ref('')
const loading = ref(false)
const error = ref('')
const debugCode = ref('')
const isVerifyStep = ref(false)

// password login state
const pwdType = ref('email')
const pwdValue = ref('')
const pwdPassword = ref('')

const isValidPhone = computed(() => phone.value.trim().length >= 10)

async function requestCode() {
  if (!isValidPhone.value) return

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
  if (!code.value) return

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
    error.value = e?.response?.data?.detail || 'Неверные данные для входа'
  } finally { loading.value = false }
}
</script>

<style scoped>
.btn-primary {
  @apply bg-accent text-white py-2 px-4 rounded-md text-center font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md text-center font-medium hover:bg-gray-50 transition-colors;
}

.tabs { @apply grid grid-cols-2 gap-2; }
.tab { @apply py-2 rounded-md border border-gray-200 text-gray-700; }
.tab.active { @apply bg-accent text-white border-accent; }
</style>
