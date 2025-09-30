<template>
  <section class="admin-product-detail">
    <AdminNavigation />

    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">{{ isNewProduct ? 'Создание товара' : 'Редактирование товара' }}</h1>
      <div class="flex gap-3">
        <button @click="goBack" class="btn-secondary">
          <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
          Назад
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-accent"></div>
      <p class="mt-2 text-gray-700">Загрузка данных...</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">
      <!-- Основная информация о товаре -->
      <div class="product-info bg-white p-6 rounded-lg shadow-sm">
        <h2 class="text-xl font-medium mb-4">Основная информация</h2>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Название товара*</label>
          <input v-model="product.name" class="input w-full" placeholder="Введите название товара" />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Категория</label>
          <select v-model="product.category_id" class="input w-full">
            <option :value="null">Выберите категорию</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Цена (₽)*</label>
          <input v-model.number="product.price" type="number" min="0" class="input w-full" placeholder="Введите цену" />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
          <textarea v-model="product.description" class="input w-full" rows="5" placeholder="Краткое описание товара"></textarea>
        </div>

        <div class="mb-6">
          <label class="flex items-center">
            <input type="checkbox" v-model="product.active" class="mr-2" />
            <span class="text-sm font-medium text-gray-700">Активен (показывать товар в каталоге)</span>
          </label>
        </div>

        <div class="flex justify-end">
          <button @click="saveProduct" class="btn-primary" :disabled="saving || !isFormValid">
            <span v-if="saving">Сохраняем...</span>
            <span v-else>Сохранить товар</span>
          </button>
          <button v-if="!isNewProduct" @click="deleteProduct" class="btn-danger" :disabled="saving">Удалить товар</button>
        </div>
      </div>

      <!-- Медиа и складские остатки -->
      <div class="product-media-inventory space-y-6">
        <!-- Изображения товара -->
        <div class="product-images bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-xl font-medium mb-4">Изображения товара</h2>

          <div v-if="!product.id" class="text-center py-4 text-gray-700">Сохраните товар, чтобы добавить изображения</div>

          <div v-else>
            <!-- Загрузка изображений -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Файл изображения</label>
              <div class="flex">
                <input type="file" ref="fileInput" accept="image/*" class="hidden" @change="handleFileChange" />
                <button @click="$refs.fileInput.click()" class="btn-secondary flex-grow" :disabled="uploading">
                  <span v-if="uploading">Загрузка...</span>
                  <span v-else>Выбрать файл</span>
                </button>
              </div>
            </div>

            <!-- Список изображений -->
            <div v-if="productImages.length > 0" class="images-grid grid grid-cols-2 gap-3">
              <div v-for="image in productImages" :key="image.id" class="image-item relative bg-gray-100 rounded-md overflow-hidden aspect-square">
                <img :src="image.url" :alt="'Image ' + (image.sort ?? 0)" class="w-full h-full object-cover" />
                <button @click="deleteImage(image)" class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 hover:bg-red-600" :disabled="deleting === image.id">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
              </div>
            </div>

            <div v-else class="text-center py-4 text-gray-700">Нет изображений</div>
          </div>
        </div>

        <!-- Складские остатки -->
        <div class="product-inventory bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-xl font-medium mb-4">Складские остатки</h2>

          <div v-if="!product.id" class="text-center py-4 text-gray-700">Сохраните товар, чтобы управлять остатками</div>

          <div v-else>
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Текущий остаток</label>
              <div class="flex">
                <input v-model.number="inventory.currentStock" type="number" min="0" class="input flex-grow" />
                <button @click="updateInventory" class="btn-primary ml-2" :disabled="!inventoryChanged || updatingInventory">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                </button>
              </div>
            </div>

            <div class="inventory-stats grid grid-cols-2 gap-4">
              <div class="stat bg-gray-50 p-3 rounded-md">
                <div class="text-sm text-gray-700">В резерве</div>
                <div class="text-xl font-medium">{{ inventory.reservedStock }}</div>
              </div>
              <div class="stat bg-gray-50 p-3 rounded-md">
                <div class="text-sm text-gray-700">Доступно</div>
                <div class="text-xl font-medium" :class="{
                    'text-red-600': inventory.availableStock <= 0,
                    'text-yellow-600': inventory.availableStock > 0 && inventory.availableStock <= 5,
                    'text-green-600': inventory.availableStock > 5
                  }">{{ inventory.availableStock }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../shared/api'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'

const route = useRoute()
const router = useRouter()
const productId = computed(() => (route.params.id === 'new' ? null : Number(route.params.id)))
const isNewProduct = computed(() => !productId.value)

const loading = ref(true)
const saving = ref(false)
const uploading = ref(false)
const deleting = ref(null)
const updatingInventory = ref(false)
const fileInput = ref(null)

const categories = ref([])
const product = reactive({ id: null, name: '', description: '', price: 0, category_id: null, active: true, images: [] })

const productImages = ref([])

const inventory = reactive({ currentStock: 0, reservedStock: 0, availableStock: 0, originalStock: 0 })

const isFormValid = computed(() => product.name && product.price > 0)
const inventoryChanged = computed(() => inventory.currentStock !== inventory.originalStock)

function syncProductImages() { product.images = productImages.value.map(img => img.url) }

function hydrateProduct(data) {
  product.id = data.id
  product.name = data.name || ''
  product.description = data.description || ''
  product.price = data.price || 0
  product.category_id = data.category_id
  product.active = data.active
  const gallery = Array.isArray(data.gallery) ? data.gallery : []
  if (gallery.length) { productImages.value = gallery }
  else {
    const fallback = Array.isArray(data.images) ? data.images : []
    productImages.value = fallback.map((url, index) => ({ id: -(index + 1), url, sort: index }))
  }
  syncProductImages()
}

async function loadProduct() {
  if (!productId.value) { loading.value = false; return }
  loading.value = true
  try {
    const { data } = await api.get(`/admin/products/${productId.value}`)
    hydrateProduct(data)
    await loadInventory()
  } catch (error) {
    console.error('Failed to load product', error)
    alert('Не удалось загрузить товар')
  } finally { loading.value = false }
}

async function loadInventory() {
  if (!productId.value) return
  try {
    const { data } = await api.get('/admin/inventory')
    const productInventory = data.find(item => item.productId === productId.value)
    if (productInventory) {
      inventory.currentStock = productInventory.currentStock
      inventory.reservedStock = productInventory.reservedStock
      inventory.availableStock = productInventory.availableStock
      inventory.originalStock = productInventory.currentStock
    }
  } catch (error) { console.error('Failed to load inventory', error) }
}

async function loadCategories() {
  try { const { data } = await api.get('/categories'); categories.value = data }
  catch (error) { console.error('Failed to load categories', error) }
}

async function saveProduct() {
  if (!isFormValid.value) return
  saving.value = true
  try {
    const payload = { name: product.name, description: product.description, price: product.price, category_id: product.category_id, active: product.active }
    let response
    if (isNewProduct.value) { response = await api.post('/admin/products', payload); hydrateProduct(response.data); await router.replace(`/admin/products/${response.data.id}`); await loadInventory() }
    else { response = await api.put(`/admin/products/${productId.value}`, payload); hydrateProduct(response.data) }
    alert('Товар сохранён')
  } catch (error) { console.error('Failed to save product', error); alert('Не удалось сохранить товар') }
  finally { saving.value = false }
}

async function handleFileChange(event) {
  const file = event.target.files[0]
  if (!file) return
  if (!file.type.startsWith('image/')) { alert('Можно загружать только изображения'); return }
  uploading.value = true
  try {
    const formData = new FormData(); formData.append('file', file)
    const { data } = await api.post(`/admin/products/${product.id}/upload-image`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    if (data.image) productImages.value = [...productImages.value, data.image]
    else if (data.image_url) productImages.value = [...productImages.value, { id: Date.now(), url: data.image_url, sort: productImages.value.length }]
    syncProductImages(); if (fileInput.value) fileInput.value.value = ''
  } catch (error) { console.error('Failed to upload image', error); alert('Не удалось загрузить изображение') }
  finally { uploading.value = false }
}

async function deleteImage(image) {
  if (!image || !image.id) return
  if (image.id <= 0) { alert('Legacy image cannot be deleted automatically. Remove the file manually.'); return }
  deleting.value = image.id
  try { await api.delete('/admin/products/' + product.id + '/images/' + image.id); productImages.value = productImages.value.filter(item => item.id !== image.id); syncProductImages() }
  catch (error) { console.error('Failed to delete image', error); alert('Не удалось удалить изображение') }
  finally { deleting.value = null }
}

async function updateInventory() {
  if (!inventoryChanged.value) return
  updatingInventory.value = true
  try { await api.put(`/admin/inventory/${product.id}`, { current_stock: inventory.currentStock }); inventory.originalStock = inventory.currentStock; inventory.availableStock = Math.max(0, (inventory.currentStock ?? 0) - (inventory.reservedStock ?? 0)); alert('Остаток обновлён') }
  catch (error) { console.error('Failed to update inventory', error); alert('Не удалось обновить остаток') }
  finally { updatingInventory.value = false }
}

function goBack() { router.push('/admin/products') }

onMounted(() => { loadCategories(); loadProduct() })

async function deleteProduct() {
  if (!productId.value) return
  if (!confirm(`Удалить товар "${product.name}" (ID: ${productId.value})? Это действие нельзя отменить.`)) return
  saving.value = true
  try {
    await api.delete(`/admin/products/${productId.value}`)
    alert('Товар удалён')
    router.push('/admin/products')
  } catch (error) {
    console.error('Failed to delete product', error)
    alert(error?.response?.data?.detail || 'Не удалось удалить товар')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.input { @apply px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent; }
.btn-primary { @apply px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed; }
.btn-secondary { @apply inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors; }
.btn-danger { @apply inline-flex items-center px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed; }
</style>
