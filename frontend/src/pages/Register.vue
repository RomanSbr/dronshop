<template>
  <section class="auth container mx-auto max-w-md py-10">
    <h1 class="text-2xl font-bold mb-6">Регистрация</h1>
    <form class="space-y-4" @submit.prevent="submit">
      <div class="row">
        <label class="label">Способ регистрации</label>
        <select v-model="contactType" class="input">
          <option value="phone">По телефону</option>
          <option value="email">По e-mail</option>
        </select>
      </div>
      <div class="row">
        <label class="label" v-if="contactType==='phone'">Телефон (+7XXXXXXXXXX)</label>
        <label class="label" v-else>E-mail</label>
        <input v-model="contactValue" :type="contactType==='email' ? 'email' : 'tel'" class="input" required />
      </div>
      <div class="row">
        <label class="label">Пароль</label>
        <input v-model="password" type="password" class="input" minlength="8" required />
      </div>
      <div class="row">
        <label class="label">Подтверждение пароля</label>
        <input v-model="passwordConfirm" type="password" class="input" minlength="8" required />
      </div>
      <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
      <button class="btn" type="submit" :disabled="loading">{{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}</button>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../shared/api'

const contactType = ref('phone')
const contactValue = ref('')
const password = ref('')
const passwordConfirm = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()

async function submit() {
  error.value = ''
  if (password.value !== passwordConfirm.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  loading.value = true
  try {
    const { data } = await api.post('/auth/register-password', {
      contact_type: contactType.value,
      contact_value: contactValue.value.trim(),
      password: password.value,
      password_confirm: passwordConfirm.value
    })
    localStorage.setItem('accessToken', data.accessToken)
    localStorage.setItem('refreshToken', data.refreshToken)
    router.push('/profile')
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Не удалось зарегистрировать'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.row { @apply flex flex-col gap-1; }
.label { @apply text-sm text-gray-700; }
.input { @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent; }
.btn { @apply inline-flex items-center px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity; }
</style>

