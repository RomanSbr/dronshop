<!-- Admin categories management -->
<template>
  <section class="admin-categories">
    <div class="container mx-auto px-4 py-6">
      <AdminNavigation />

      <div class="flex flex-wrap gap-3 items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold">Категории каталога</h1>
          <p class="text-sm text-gray-500">Управляйте структурой категорий и их вложенностью.</p>
        </div>
        <div class="flex gap-3">
          <button class="btn-secondary" @click="loadCategories" :disabled="loading">
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Обновить
          </button>
          <button class="btn-primary" @click="openCreate">
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Новая категория
          </button>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Название</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Slug</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Родитель</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="loading">
              <td colspan="4" class="px-6 py-6 text-center text-sm text-gray-500">
                <div class="flex items-center justify-center gap-3">
                  <span class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-accent"></span>
                  <span>Загружаем категории...</span>
                </div>
              </td>
            </tr>
            <tr v-else-if="tree.length === 0">
              <td colspan="4" class="px-6 py-6 text-center text-sm text-gray-500">Категории пока не найдены.</td>
            </tr>
            <tr v-else v-for="item in tree" :key="item.id">
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <span class="tree-dot" :style="{ marginLeft: item.level ? item.level * 16 + 'px' : '0px' }"></span>
                  <span class="font-medium">{{ item.name }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ item.slug }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ item.parent_id ? categoryNames.get(item.parent_id) || '-' : 'Корневая' }}</td>
              <td class="px-6 py-4">
                <div class="flex justify-end gap-2">
                  <button class="btn-sm btn-secondary" @click="openEdit(item)">Редактировать</button>
                  <button class="btn-sm btn-danger" @click="removeCategory(item)" :disabled="deletingId === item.id">
                    <span v-if="deletingId === item.id" class="inline-flex items-center gap-2">
                      <span class="loader"></span>Удаляем...
                    </span>
                    <span v-else>Удалить</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="modalOpen" class="modal-overlay">
      <div class="modal-card">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-xl font-semibold">{{ form.id ? 'Редактирование категории' : 'Новая категория' }}</h2>
            <p class="text-sm text-gray-500">Укажите название, slug и при необходимости выберите родителя.</p>
          </div>
          <button class="text-gray-400 hover:text-gray-600" @click="closeModal" :disabled="saving">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form class="space-y-4" @submit.prevent="handleSubmit">
          <label class="form-group">
            <span class="form-label">Название*</span>
            <input
              v-model="form.name"
              type="text"
              class="form-input"
              placeholder="Например, Готовые модели"
              :disabled="saving"
              required
            />
          </label>

          <div class="form-group">
            <div class="flex items-center justify-between">
              <span class="form-label">Slug*</span>
              <button type="button" class="text-sm text-accent hover:underline" @click="regenerateSlug" :disabled="saving">
                Сгенерировать
              </button>
            </div>
            <input
              v-model="form.slug"
              @input="slugTouched = true"
              type="text"
              class="form-input"
              placeholder="gotovye-modeli"
              :disabled="saving"
              required
            />
          </div>

          <label class="form-group">
            <span class="form-label">Родительская категория</span>
            <select v-model="parentSelection" class="form-input" :disabled="saving">
              <option value="">Корневая категория</option>
              <option v-for="option in parentOptions" :key="option.id" :value="String(option.id)">
                {{ option.name }}
              </option>
            </select>
          </label>

          <div class="flex justify-end gap-3 pt-2">
            <button type="button" class="btn-secondary" @click="closeModal" :disabled="saving">Отмена</button>
            <button type="submit" class="btn-primary" :disabled="saving">
              <span v-if="saving" class="inline-flex items-center gap-2">
                <span class="loader"></span>Сохраняем...
              </span>
              <span v-else>Сохранить</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import api from '../../shared/api'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'
import slugify from '../../shared/slugify'
import { useNotificationsStore } from '../../stores/notifications'

const notifications = useNotificationsStore()

const categories = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const saving = ref(false)
const deletingId = ref(null)
const slugTouched = ref(false)

const form = reactive({
  id: null,
  name: '',
  slug: '',
  parent_id: null
})

const categoryNames = computed(() => {
  const map = new Map()
  categories.value.forEach(cat => map.set(cat.id, cat.name))
  return map
})

const parentSelection = computed({
  get: () => (form.parent_id == null ? '' : String(form.parent_id)),
  set: value => {
    form.parent_id = value === '' ? null : Number(value)
  }
})

const descendantsOfCurrent = computed(() => {
  if (!form.id) return new Set()
  const byParent = new Map()
  categories.value.forEach(cat => {
    const parent = cat.parent_id == null ? null : cat.parent_id
    if (!byParent.has(parent)) byParent.set(parent, [])
    byParent.get(parent).push(cat)
  })
  const visited = new Set()
  const stack = [form.id]
  while (stack.length) {
    const current = stack.pop()
    const children = byParent.get(current) || []
    for (const child of children) {
      if (!visited.has(child.id)) {
        visited.add(child.id)
        stack.push(child.id)
      }
    }
  }
  return visited
})

const parentOptions = computed(() => {
  return categories.value
    .filter(cat => cat.id !== form.id && !descendantsOfCurrent.value.has(cat.id))
    .sort((a, b) => a.name.localeCompare(b.name, 'ru'))
})

const tree = computed(() => {
  const byParent = new Map()
  categories.value.forEach(cat => {
    const parent = cat.parent_id == null ? null : cat.parent_id
    if (!byParent.has(parent)) byParent.set(parent, [])
    byParent.get(parent).push(cat)
  })
  const result = []
  const traverse = (parentId, level) => {
    const nodes = (byParent.get(parentId) || []).sort((a, b) => a.name.localeCompare(b.name, 'ru'))
    nodes.forEach(node => {
      result.push({ ...node, level })
      traverse(node.id, level + 1)
    })
  }
  traverse(null, 0)
  return result
})

watch(() => form.name, value => {
  if (!slugTouched.value && !form.id) {
    form.slug = slugify(value || '')
  }
})

function resetForm() {
  form.id = null
  form.name = ''
  form.slug = ''
  form.parent_id = null
  slugTouched.value = false
}

function openCreate() {
  resetForm()
  modalOpen.value = true
}

function openEdit(category) {
  form.id = category.id
  form.name = category.name
  form.slug = category.slug
  form.parent_id = category.parent_id
  slugTouched.value = true
  modalOpen.value = true
}

function closeModal() {
  if (saving.value) return
  modalOpen.value = false
  resetForm()
}

function regenerateSlug() {
  form.slug = slugify(form.name || '')
  slugTouched.value = true
}

async function loadCategories() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/categories')
    categories.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Ошибка при загрузке категорий', error)
    notifications.error('Не удалось загрузить категории', error?.response?.data?.detail || '')
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  if (!form.name.trim()) {
    notifications.error('Введите название категории')
    return
  }
  if (!form.slug.trim()) {
    form.slug = slugify(form.name)
  }
  const payload = {
    name: form.name.trim(),
    slug: form.slug.trim(),
    parent_id: form.parent_id
  }
  saving.value = true
  try {
    if (form.id) {
      await api.put(`/admin/categories/${form.id}`, payload)
      notifications.success('Категория обновлена')
    } else {
      await api.post('/admin/categories', payload)
      notifications.success('Категория создана')
    }
    await loadCategories()
    closeModal()
  } catch (error) {
    console.error('Ошибка при сохранении категории', error)
    notifications.error('Не удалось сохранить категорию', error?.response?.data?.detail || '')
  } finally {
    saving.value = false
  }
}

async function removeCategory(category) {
  if (deletingId.value || !confirm(`Удалить категорию "${category.name}"?`)) {
    return
  }
  deletingId.value = category.id
  try {
    await api.delete(`/admin/categories/${category.id}`)
    notifications.success('Категория удалена')
    await loadCategories()
  } catch (error) {
    console.error('Ошибка при удалении категории', error)
    notifications.error('Не удалось удалить категорию', error?.response?.data?.detail || '')
  } finally {
    deletingId.value = null
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.btn-primary {
  @apply inline-flex items-center px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity disabled:opacity-60 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors disabled:opacity-60 disabled:cursor-not-allowed;
}

.btn-danger {
  @apply inline-flex items-center px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed;
}

.btn-sm {
  @apply px-3 py-1 text-sm rounded-md;
}

.form-group {
  @apply flex flex-col gap-1;
}

.form-label {
  @apply text-sm font-medium text-gray-700;
}

.form-input {
  @apply px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent;
}

.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 px-4;
}

.modal-card {
  @apply bg-white w-full max-w-xl rounded-lg shadow-xl p-6;
}

.loader {
  @apply animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white;
}

.tree-dot {
  @apply block w-2 h-2 rounded-full bg-accent mr-3;
}
</style>
