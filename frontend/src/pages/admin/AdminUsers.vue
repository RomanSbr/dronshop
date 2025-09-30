<template>
  <section class="admin-users">
    <div class="container mx-auto px-4 py-6">
      <AdminNavigation />
      <h1 class="text-2xl font-bold mb-4">Пользователи</h1>
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="th">ID</th>
              <th class="th">Телефон</th>
              <th class="th">E-mail</th>
              <th class="th">Роли</th>
              <th class="th">Статус</th>
              <th class="th text-right">Действия</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="u in users" :key="u.id">
              <td class="td">{{ u.id }}</td>
              <td class="td">{{ u.phone || '-' }}</td>
              <td class="td">{{ u.email || '-' }}</td>
              <td class="td">{{ (u.roles || []).join(', ') }}</td>
              <td class="td">{{ u.is_blocked ? 'Заблокирован' : 'Активен' }}</td>
              <td class="td text-right">
                <div class="flex justify-end gap-2">
                  <button class="btn-sm" @click="toggleAdmin(u)">{{ isAdmin(u) ? 'Снять админа' : 'Назначить админом' }}</button>
                  <button class="btn-sm" @click="toggleBlock(u)">{{ u.is_blocked ? 'Разблокировать' : 'Заблокировать' }}</button>
                  <button class="btn-sm danger" @click="remove(u)">Удалить</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'
import api from '../../shared/api'

const users = ref([])

function isAdmin(u) { return Array.isArray(u.roles) && u.roles.includes('admin') }

async function load() {
  const { data } = await api.get('/admin/users')
  users.value = data
}

async function toggleAdmin(u) {
  await api.patch(`/admin/users/${u.id}`, null, { params: { action: isAdmin(u) ? 'remove_admin' : 'make_admin' } })
  await load()
}

async function toggleBlock(u) {
  await api.patch(`/admin/users/${u.id}`, null, { params: { action: u.is_blocked ? 'unblock' : 'block' } })
  await load()
}

async function remove(u) {
  if (!confirm(`Удалить пользователя #${u.id}?`)) return
  await api.delete(`/admin/users/${u.id}`)
  await load()
}

onMounted(load)
</script>

<style scoped>
.th { @apply px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider; }
.td { @apply px-4 py-2 text-sm text-gray-700; }
.btn-sm { @apply px-3 py-1.5 rounded-md border border-gray-300 text-gray-700 hover:bg-gray-50; }
.btn-sm.danger { @apply border-red-300 text-red-600 hover:bg-red-50; }
</style>

