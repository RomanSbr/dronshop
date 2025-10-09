<template>
  <div v-if="open" class="auth-overlay" role="dialog" aria-modal="true" @click.self="onClose">
    <div class="auth-modal" role="document">
      <button type="button" class="close" @click="onClose" aria-label="Закрыть">
        <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18L18 6M6 6l12 12"/></svg>
      </button>

      <div class="brand">
        <img src="/header-logo.png" alt="GLORYAIR" class="brand-logo" />
        <span class="brand-id">ID</span>
      </div>

      <template v-if="step === 'phone'">
        <h2 class="title">Введите номер телефона</h2>
        <p class="subtitle">Мы отправим код. Он придёт в СМС</p>

        <form class="form" @submit.prevent="requestCode">
          <label class="phone-field">
            <span class="prefix">+7</span>
            <input
              ref="phoneInput"
              v-model="phone"
              type="tel"
              inputmode="numeric"
              placeholder="999 999 99 99"
              class="phone-input"
              autocomplete="tel"
              aria-label="Номер телефона"
              @input="normalizePhone"
            />
          </label>

          <button class="btn-buy w-full justify-center" type="submit" :disabled="loading || !isValidPhone">Войти</button>
        </form>

        <div class="divider"><span>Или</span></div>

        <div class="links">
          <button type="button" class="link" @click="$emit('switch','email')">Войти по почте</button>
          <button type="button" class="link" @click="$emit('help')">Не могу войти</button>
        </div>
      </template>

      <template v-else>
        <h2 class="title">Введите код из пуш-уведомления</h2>
        <p class="subtitle">Мы отправим код. Код может прийти на почту или в СМС</p>

        <form class="form" @submit.prevent="verifyCode">
          <input
            ref="codeInput"
            v-model="code"
            inputmode="numeric"
            placeholder="Код из сообщения"
            class="code-input"
            aria-label="Код из сообщения"
          />
          <button class="btn-buy w-full justify-center" type="submit" :disabled="loading || !code">Войти</button>
        </form>

        <div class="links">
          <button type="button" class="link" @click="$emit('switch','email')">Войти по почте</button>
          <button type="button" class="link" @click="$emit('help')">Не могу войти</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import api from '../../shared/api'

const props = defineProps({
  open: { type: Boolean, default: false }
})
const emit = defineEmits(['close', 'success', 'switch', 'help'])

const phone = ref('')
const code = ref('')
const loading = ref(false)
const step = ref('phone') // 'phone' | 'code'
const phoneInput = ref(null)
const codeInput = ref(null)

const isValidPhone = computed(() => phone.value.replace(/\D/g, '').length === 10)

function normalizePhone() {
  // Accept only digits and format as 999 999 99 99
  const digits = phone.value.replace(/\D/g, '').slice(0, 10)
  const parts = []
  if (digits.length > 0) parts.push(digits.slice(0, 3))
  if (digits.length > 3) parts.push(digits.slice(3, 6))
  if (digits.length > 6) parts.push(digits.slice(6, 8))
  if (digits.length > 8) parts.push(digits.slice(8, 10))
  phone.value = parts.join(' ')
}

async function requestCode() {
  if (!isValidPhone.value || loading.value) return
  loading.value = true
  try {
    const payload = { phone: `+7${phone.value.replace(/\D/g, '')}` }
    await api.post('/auth/request-code', payload)
    step.value = 'code'
    setTimeout(() => codeInput.value?.focus(), 50)
  } catch (e) {
    // keep UX silent here; page can show toast if needed
  } finally {
    loading.value = false
  }
}

async function verifyCode() {
  if (!code.value || loading.value) return
  loading.value = true
  try {
    const payload = { phone: `+7${phone.value.replace(/\D/g, '')}`, verificationCode: code.value }
    const { data } = await api.post('/auth/register', payload)
    localStorage.setItem('accessToken', data.accessToken)
    localStorage.setItem('refreshToken', data.refreshToken)
    window.dispatchEvent(new Event('auth-changed'))
    emit('success')
    emit('close')
  } catch (e) {
    // could add error state if needed
  } finally {
    loading.value = false
  }
}

function onEsc(e) { if (e.key === 'Escape') emit('close') }
const onClose = () => emit('close')

watch(() => props.open, (v) => {
  document.body.style.overflow = v ? 'hidden' : ''
  if (v) {
    step.value = 'phone'
    code.value = ''
    setTimeout(() => phoneInput.value?.focus(), 50)
  }
})

onMounted(() => window.addEventListener('keydown', onEsc))
onBeforeUnmount(() => window.removeEventListener('keydown', onEsc))
</script>

<style scoped>
.auth-overlay { position: fixed; inset: 0; background: rgba(2,6,23,.6); backdrop-filter: blur(4px); display: grid; place-items: center; z-index: 60; }
.auth-modal { width: 100%; max-width: 420px; background: #fff; border-radius: 20px; padding: 28px 24px; position: relative; box-shadow: 0 20px 60px rgba(2,6,23,.3); }
.close { position: absolute; top: 12px; right: 12px; width: 36px; height: 36px; border-radius: 10px; border: 1px solid #e5e7eb; background: #fff; display: inline-flex; align-items: center; justify-content: center; }
.brand { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.brand-logo { height: 26px; width: auto; display: block; }
.brand-id { font-weight: 700; letter-spacing: .02em; color: #0b2a5b; font-style: italic; font-size: calc(1em + 5px); }
.title { font-size: 26px; font-weight: 800; line-height: 1.2; color: #374151; margin-top: 8px; }
.subtitle { color: #6b7280; margin: 8px 0 16px; }
.form { display: grid; gap: 14px; }
.phone-field { display: flex; align-items: center; border: 1px solid #cbd5e1; border-radius: 14px; overflow: hidden; }
.prefix { background: #4b5563; color: #fff; padding: 10px 14px; font-weight: 700; letter-spacing: .02em; }
.phone-input { flex: 1; padding: 12px 14px; outline: none; border: 0; font-size: 16px; }
.code-input { width: 100%; border: 1px solid #cbd5e1; border-radius: 14px; padding: 12px 14px; font-size: 16px; }
.divider { display: flex; align-items: center; gap: 8px; color: #9ca3af; font-size: 12px; margin: 12px 0; }
.divider::before, .divider::after { content: ''; height: 1px; flex: 1; background: #e5e7eb; }
.links { display: grid; gap: 8px; text-align: center; }
.link { color: #0b2a5b; font-weight: 600; }
@media (max-width: 480px) { .auth-modal { margin: 0 12px; } }
</style>
