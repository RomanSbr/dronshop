<template>
  <section class="admin-index">
    <div class="container mx-auto px-4 py-6">
      <AdminNavigation />
      <h1 class="text-2xl font-bold mb-6">Панель администратора</h1>

      <div class="welcome bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 class="text-xl font-medium mb-4">Добро пожаловать, {{ userName }}!</h2>
        <p class="mb-4">Вы вошли как <span class="font-medium">{{ isAdmin ? 'администратор' : 'покупатель' }}</span>.</p>

        <div v-if="isAdmin" class="admin-info">
          <p class="mb-4">Как администратор, вы можете управлять следующими разделами:</p>
          <ul class="list-disc pl-5 mb-4 space-y-2">
            <li>
              <router-link to="/admin/products" class="text-accent hover:underline">
                Товары
              </router-link>
              — добавление, редактирование и публикация товаров
            </li>
            <li>
              <router-link to="/admin/inventory" class="text-accent hover:underline">
                Остатки
              </router-link>
              — фактический остаток товара на складе
            </li>
            <li>
              <router-link to="/admin/orders" class="text-accent hover:underline">
                Заказы
              </router-link>
              — управление заказами и статусами отгрузки
            </li>
            <li>
              <router-link to="/admin/reviews" class="text-accent hover:underline">
                Отзывы
              </router-link>
              — модерация и ответы на отзывы покупателей
            </li>
            <li>
              <router-link to="/admin/settings" class="text-accent hover:underline">
                Настройки
              </router-link>
              — основные параметры сайта и витрины
            </li>
          </ul>
        </div>

        <div v-else class="buyer-info">
          <p class="mb-4">Как покупатель вы можете:</p>
          <ul class="list-disc pl-5 mb-4 space-y-2">
            <li>
              <router-link to="/catalog" class="text-accent hover:underline">
                Просматривать каталог товаров
              </router-link>
            </li>
            <li>
              <router-link to="/cart" class="text-accent hover:underline">
                Оформлять корзину и заказы
              </router-link>
            </li>
            <li>
              <router-link to="/favorites" class="text-accent hover:underline">
                Управлять избранным
              </router-link>
            </li>
            <li>
              <router-link to="/profile" class="text-accent hover:underline">
                Просматривать профиль
              </router-link>
            </li>
          </ul>
          <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
            <p class="text-yellow-700">
              Для доступа в админку используйте test‑аккаунт ниже.
            </p>
          </div>
        </div>

        <div class="mt-6">
          <div class="bg-gray-50 border border-gray-200 rounded-xl p-4">
            <h3 class="font-medium mb-2">Как выдать права администратора</h3>
            <p class="text-sm text-gray-600">
              Создайте или отредактируйте пользователя в разделе «Пользователи» и назначьте ему роль
              администратора. При необходимости обратитесь к ответственному за безопасность — прямой вход
              по тестовым учетным данным отключён.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../shared/api'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'

const router = useRouter()
const user = ref(null)
const loading = ref(true)

const userName = computed(() => {
  if (!user.value) return 'Гость'
  return user.value.name || `Пользователь ${user.value.phone}`
})

const isAdmin = computed(() => {
  if (!user.value || !user.value.roles) return false
  return user.value.roles.includes('admin')
})

async function loadUserData() {
  loading.value = true
  try {
    const { data } = await api.get('/auth/me')
    user.value = data
  } catch (error) {
    console.error('Failed to load user data:', error)
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    router.push('/auth')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
.btn-secondary {
  @apply inline-block px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors;
}

code {
  @apply bg-gray-100 px-2 py-0.5 rounded text-sm font-mono;
}
</style>
