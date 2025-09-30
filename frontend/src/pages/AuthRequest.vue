<template>
  <section>
    <h1>Вход / регистрация</h1>
    <input v-model="phone" class="input" placeholder="Например +7..." />
    <button class="btn" :disabled="loading" @click="send">Получить код</button>
    <div v-if="debugCode" class="pill" style="margin-top: 8px;">Test code: {{ debugCode }}</div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import api from '../shared/api'
import { useRouter } from 'vue-router'

const phone = ref('')
const loading = ref(false)
const debugCode = ref('')
const router = useRouter()

async function send() {
  loading.value = true
  try {
    const { data } = await api.post('/auth/request-code', { phone: phone.value })
    debugCode.value = data.debugCode
    router.push({ path: '/auth/verify', query: { phone: phone.value } })
  } finally {
    loading.value = false
  }
}
</script>
