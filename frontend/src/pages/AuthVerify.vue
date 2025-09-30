<template>
  <section>
    <h1>Подтверждение</h1>
    <input class="input" v-model="code" placeholder="Код из SMS" />
    <button class="btn" :disabled="loading" @click="verify">Подтвердить</button>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import api from '../shared/api'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const code = ref('')
const loading = ref(false)

async function verify() {
  loading.value = true
  try {
    const phone = route.query.phone
    const { data } = await api.post('/auth/register', { phone, verificationCode: code.value })
    localStorage.setItem('accessToken', data.accessToken)
    localStorage.setItem('refreshToken', data.refreshToken)
    router.push('/profile')
  } finally {
    loading.value = false
  }
}
</script>
