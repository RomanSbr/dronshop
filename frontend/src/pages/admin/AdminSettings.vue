<template>
  <section class="admin-settings">
    <div class="container mx-auto px-4 py-6">
    <AdminNavigation />
    <h1 class="text-2xl font-bold mb-6">Настройки сайта</h1>
    
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-accent"></div>
      <p class="mt-2 text-gray-600">Загрузка настроек...</p>
    </div>
    
    <div v-else>
      <!-- Основные настройки -->
      <div class="settings-section bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 class="text-xl font-medium mb-4">Основные настройки</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="form-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Название сайта</label>
            <input 
              v-model="settings.site_name" 
              class="input w-full" 
              placeholder="Название сайта"
            />
            <small class="text-gray-500">Отображается в заголовке страницы и шапке сайта</small>
          </div>
          
          <div class="form-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Описание сайта</label>
            <textarea 
              v-model="settings.site_description" 
              class="input w-full" 
              rows="2"
              placeholder="Краткое описание сайта"
            ></textarea>
            <small class="text-gray-500">Используется для SEO и мета-тегов</small>
          </div>
        </div>
      </div>
      
      <!-- Контактная информация -->
      <div class="settings-section bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 class="text-xl font-medium mb-4">Контактная информация</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="form-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input 
              v-model="settings.contact_email" 
              class="input w-full" 
              type="email"
              placeholder="Email для связи"
            />
          </div>
          
          <div class="form-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Телефон</label>
            <input 
              v-model="settings.contact_phone" 
              class="input w-full" 
              placeholder="Контактный телефон"
            />
          </div>
        </div>
      </div>
      
      <!-- Информация о доставке и оплате -->
      <div class="settings-section bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 class="text-xl font-medium mb-4">Информация о доставке и оплате</h2>
        
        <div class="grid grid-cols-1 gap-6">
          <div class="form-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Информация о доставке</label>
            <textarea 
              v-model="settings.delivery_info" 
              class="input w-full" 
              rows="3"
              placeholder="Информация о способах доставки"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label class="block text-sm font-medium text-gray-700 mb-1">Информация об оплате</label>
            <textarea 
              v-model="settings.payment_info" 
              class="input w-full" 
              rows="3"
              placeholder="Информация о способах оплаты"
            ></textarea>
          </div>
        </div>
      </div>
      
      <!-- Дополнительные настройки -->
      <div class="settings-section bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 class="text-xl font-medium mb-4">Дополнительные настройки</h2>
        
        <div class="mb-4">
          <div class="flex justify-between items-center mb-2">
            <label class="block text-sm font-medium text-gray-700">Произвольные настройки</label>
            <button @click="addCustomSetting" class="btn-sm btn-secondary">
              Добавить настройку
            </button>
          </div>
          
          <div v-if="customSettings.length === 0" class="text-center py-4 bg-gray-50 rounded-md">
            <p class="text-gray-500">Нет дополнительных настроек</p>
          </div>
          
          <div v-else class="space-y-3">
            <div 
              v-for="(setting, index) in customSettings" 
              :key="index"
              class="custom-setting bg-gray-50 p-3 rounded-md"
            >
              <div class="grid grid-cols-[1fr_auto] gap-2">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <input 
                    v-model="setting.key" 
                    class="input" 
                    placeholder="Ключ"
                  />
                  <input 
                    v-model="setting.value" 
                    class="input" 
                    placeholder="Значение"
                  />
                </div>
                <button @click="removeCustomSetting(index)" class="btn-icon text-red-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
              <div class="mt-2">
                <input 
                  v-model="setting.description" 
                  class="input w-full" 
                  placeholder="Описание (необязательно)"
                />
              </div>
              <div class="mt-2 flex items-center">
                <input 
                  type="checkbox" 
                  :id="`public-${index}`" 
                  v-model="setting.is_public"
                  class="mr-2"
                />
                <label :for="`public-${index}`" class="text-sm">Публичная настройка</label>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Кнопки действий -->
      <div class="actions flex justify-end gap-3">
        <button @click="resetSettings" class="btn-secondary">
          Отменить изменения
        </button>
        <button @click="saveSettings" class="btn-primary" :disabled="saving">
          <span v-if="saving">Сохранение...</span>
          <span v-else>Сохранить настройки</span>
        </button>
      </div>
    </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../../shared/api'
import AdminNavigation from '../../components/admin/AdminNavigation.vue'

const loading = ref(true)
const saving = ref(false)
const settings = reactive({
  site_name: '',
  site_description: '',
  contact_email: '',
  contact_phone: '',
  delivery_info: '',
  payment_info: '',
})

const customSettings = ref([])
const originalSettings = ref({})

// Загрузка настроек
async function loadSettings() {
  loading.value = true
  
  try {
    const { data } = await api.get('/settings', { params: { include_private: true } })
    
    // Разделяем настройки на основные и произвольные
    const mainSettingKeys = Object.keys(settings)
    
    data.forEach(setting => {
      if (mainSettingKeys.includes(setting.key)) {
        settings[setting.key] = setting.value || ''
      } else {
        customSettings.value.push({
          key: setting.key,
          value: setting.value || '',
          description: setting.description || '',
          is_public: setting.is_public
        })
      }
    })
    
    // Сохраняем оригинальные значения для возможности отмены изменений
    originalSettings.value = {
      ...JSON.parse(JSON.stringify(settings)),
      customSettings: JSON.parse(JSON.stringify(customSettings.value))
    }
    
  } catch (error) {
    console.error('Ошибка при загрузке настроек:', error)
    alert('Не удалось загрузить настройки сайта')
  } finally {
    loading.value = false
  }
}

// Добавление произвольной настройки
function addCustomSetting() {
  customSettings.value.push({
    key: '',
    value: '',
    description: '',
    is_public: true
  })
}

// Удаление произвольной настройки
function removeCustomSetting(index) {
  customSettings.value.splice(index, 1)
}

// Сброс настроек к исходным значениям
function resetSettings() {
  // Восстанавливаем основные настройки
  Object.keys(settings).forEach(key => {
    settings[key] = originalSettings.value[key] || ''
  })
  
  // Восстанавливаем произвольные настройки
  customSettings.value = JSON.parse(JSON.stringify(originalSettings.value.customSettings || []))
}

// Сохранение настроек
async function saveSettings() {
  if (saving.value) return
  
  saving.value = true
  
  try {
    // Формируем объект со всеми настройками
    const allSettings = { ...settings }
    
    // Добавляем произвольные настройки
    for (const setting of customSettings.value) {
      if (setting.key && setting.key.trim()) {
        // Сначала создаем или обновляем настройку
        await api.put(`/settings/${setting.key}`, {
          value: setting.value,
          description: setting.description,
          is_public: setting.is_public
        })
      }
    }
    
    // Обновляем основные настройки одним запросом
    await api.post('/settings/batch', allSettings)
    
    alert('Настройки успешно сохранены')
    
    // Обновляем оригинальные значения
    originalSettings.value = {
      ...JSON.parse(JSON.stringify(settings)),
      customSettings: JSON.parse(JSON.stringify(customSettings.value))
    }
    
  } catch (error) {
    console.error('Ошибка при сохранении настроек:', error)
    alert('Не удалось сохранить настройки сайта')
  } finally {
    saving.value = false
  }
}

// Загрузка данных при монтировании компонента
onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.input {
  @apply px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent;
}

.btn-primary {
  @apply px-4 py-2 bg-accent text-white rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors;
}

.btn-sm {
  @apply px-3 py-1 text-sm rounded-md font-medium;
}

.btn-icon {
  @apply p-2 rounded-md hover:bg-gray-200 transition-colors;
}
</style>
