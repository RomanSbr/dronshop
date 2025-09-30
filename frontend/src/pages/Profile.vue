<template>
  <section class="profile">
    <div class="container mx-auto px-4 py-8">
      <div class="card">
        <!-- Hero -->
        <div class="card-hero">
          <div class="avatar" aria-hidden="true">{{ initials }}</div>
          <div class="hero-content">
            <h1 class="title">{{ displayName }}</h1>
            <p class="muted">{{ contactLabel }}</p>
            <div class="roles" v-if="roles.length">
              <span v-for="r in roles" :key="r" class="role">{{ r }}</span>
            </div>
          </div>
          <div class="hero-actions">
            <button class="btn ghost" @click="logout">Выйти</button>
            <router-link v-if="isAdmin" to="/admin" class="btn admin">Админ‑панель</router-link>
          </div>
        </div>

        <!-- Body -->
        <div class="profile-grid">
          <div class="panel">
            <h2 class="panel-title">Контакты</h2>
            <dl class="fields">
              <div class="row">
                <dt>E‑mail</dt>
                <dd>{{ me?.email || '—' }}</dd>
              </div>
              <div class="row">
                <dt>Телефон</dt>
                <dd>{{ prettyPhone }}</dd>
              </div>
            </dl>
          </div>

          <div class="panel">
            <h2 class="panel-title">Безопасность</h2>
            <p class="muted">Смена пароля и завершение сессий.</p>
            <div class="actions">
              <button class="btn" @click="changePassword">Сменить пароль</button>
              <button class="btn ghost" @click="logout">Завершить все сессии</button>
            </div>
          </div>

          <div class="panel md:col-span-2">
            <h2 class="panel-title">Мои заказы</h2>
            <div v-if="ordersLoading" class="muted">Загрузка заказов…</div>
            <div v-else-if="orders.length === 0" class="muted">Пока нет заказов.</div>
            <ul v-else class="orders">
              <li v-for="o in orders" :key="o.id" class="order">
                <div class="left">
                  <div class="num">{{ o.orderNumber }}</div>
                  <div class="date">{{ formatDate(o.createdAt) }}</div>
                </div>
                <div class="right">
                  <span class="status" :class="o.status">{{ mapStatus(o.status) }}</span>
                  <span class="amount">{{ formatAmount(o.totalAmount) }}</span>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../shared/api'

const router = useRouter()
const me = ref(null)
const orders = ref([])
const ordersLoading = ref(false)

const roles = computed(() => Array.isArray(me.value?.roles) ? me.value.roles : [])
const isAdmin = computed(() => roles.value.includes('admin'))

const displayName = computed(() => me.value?.name || me.value?.email || me.value?.phone || 'Профиль')
const contactLabel = computed(() => me.value?.email || me.value?.phone || '')
const initials = computed(() => {
  const txt = (me.value?.name || me.value?.email || 'U').trim()
  const parts = txt.replace(/@.*/, '').split(/\s|\.|_/).filter(Boolean)
  return (parts[0]?.[0] || 'U').toUpperCase() + (parts[1]?.[0] || '')
})
const prettyPhone = computed(() => {
  const p = me.value?.phone || ''
  if (!p || p.startsWith('email:')) return '—'
  return p.replace(/^(\+7)(\d{3})(\d{3})(\d{2})(\d{2})$/, '$1 ($2) $3‑$4‑$5') || p
})

function logout() {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  window.dispatchEvent(new Event('auth-changed'))
  router.push('/auth')
}

function changePassword() {
  alert('Смена пароля будет добавлена позднее.')
}

function mapStatus(s){ const d={ pending:'Ожидает', paid:'Оплачен', processing:'В обработке', shipped:'Отправлен', completed:'Завершён', cancelled:'Отменён' }; return d[s]||s }
function formatAmount(v){ return `${Number(v||0).toLocaleString()} ₽` }
function formatDate(v){ try { return new Date(v).toLocaleString('ru-RU') } catch { return v } }

onMounted(async () => {
  try {
    const { data } = await api.get('/auth/me')
    me.value = data
    ordersLoading.value = true
    try {
      const res = await api.get('/orders')
      orders.value = Array.isArray(res.data) ? res.data : []
    } finally { ordersLoading.value = false }
  } catch (e) {
    logout()
  }
})
</script>

<style scoped>
.card { @apply bg-white rounded-2xl shadow-xl overflow-hidden; }
.card-hero { @apply relative p-6 md:p-8 bg-gradient-to-r from-accent-600 to-accent-800 text-white flex items-center gap-6; }
.avatar { @apply w-16 h-16 md:w-20 md:h-20 rounded-full bg-white/20 flex items-center justify-center text-2xl font-bold; }
.hero-content { @apply flex-1 min-w-0; }
.title { @apply text-xl md:text-2xl font-bold truncate; }
.muted { @apply text-white/80; }
.roles { @apply mt-2 flex flex-wrap gap-2; }
.role { @apply px-2.5 py-0.5 rounded-full text-xs font-semibold bg-white/20 backdrop-blur-sm; }
.hero-actions { @apply flex items-center gap-2; }
.btn { @apply inline-flex items-center px-4 py-2 rounded-lg bg-white text-accent-700 font-medium hover:bg-white/90 transition-colors; }
.btn.ghost { @apply bg-white/10 text-white border border-white/30 hover:bg-white/20; }
.btn.admin { @apply bg-emerald-400 text-emerald-900 hover:bg-emerald-300; }

.profile-grid { @apply grid grid-cols-1 md:grid-cols-2 gap-6 p-6 md:p-8; }
.panel { @apply bg-gray-50 rounded-xl p-5 border border-gray-200; }
.panel-title { @apply text-base font-semibold text-gray-800 mb-3; }
.fields { @apply space-y-2; }
.row { @apply flex items-center justify-between text-sm text-gray-700; }
.actions { @apply flex gap-3 mt-2; }

.orders { @apply divide-y divide-gray-200; }
.order { @apply flex items-center justify-between py-3; }
.order .left { @apply flex items-baseline gap-3; }
.order .num { @apply font-semibold text-gray-800; }
.order .date { @apply text-sm text-gray-500; }
.order .right { @apply flex items-center gap-3; }
.order .status { @apply text-xs px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-700 capitalize; }
.order .status.paid { @apply bg-emerald-100 text-emerald-700; }
.order .status.processing { @apply bg-amber-100 text-amber-700; }
.order .status.shipped { @apply bg-blue-100 text-blue-700; }
.order .status.completed { @apply bg-gray-200 text-gray-700; }
.order .status.cancelled { @apply bg-red-100 text-red-700; }
.order .amount { @apply font-semibold text-gray-900; }
</style>
