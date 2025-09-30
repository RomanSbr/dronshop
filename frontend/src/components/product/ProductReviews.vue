<template>
  <div class="reviews-section">
    <h2 class="text-xl font-bold mb-4">Отзывы ({{ reviews.length }})</h2>
    
    <!-- Форма добавления отзыва -->
    <div v-if="!isReviewFormVisible" class="add-review-button mb-6">
      <button @click="showReviewForm" class="btn-primary">
        Написать отзыв
      </button>
    </div>
    
    <div v-if="isReviewFormVisible" class="review-form bg-gray-50 p-6 rounded-lg mb-6">
      <h3 class="text-lg font-medium mb-4">Ваш отзыв</h3>
      
      <form @submit.prevent="submitReview">
        <div class="form-group mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Оценка</label>
          <div class="rating-input flex items-center">
            <button 
              v-for="star in 5" 
              :key="star" 
              type="button"
              @click="newReview.rating = star"
              class="star-btn text-2xl focus:outline-none"
            >
              <span v-if="star <= newReview.rating" class="text-yellow-400">★</span>
              <span v-else class="text-gray-300">★</span>
            </button>
            <span class="ml-2 text-sm text-gray-500">{{ ratingLabels[newReview.rating - 1] || 'Выберите оценку' }}</span>
          </div>
        </div>
        
        <div class="form-group mb-4">
          <label for="reviewName" class="block text-sm font-medium text-gray-700 mb-1">Имя*</label>
          <input 
            type="text" 
            id="reviewName" 
            v-model="newReview.name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
            required
          >
        </div>
        
        <div class="form-group mb-4">
          <label for="reviewEmail" class="block text-sm font-medium text-gray-700 mb-1">Email*</label>
          <input 
            type="email" 
            id="reviewEmail" 
            v-model="newReview.email" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
            required
          >
          <small class="text-gray-500">Email не будет опубликован</small>
        </div>
        
        <div class="form-group mb-4">
          <label for="reviewTitle" class="block text-sm font-medium text-gray-700 mb-1">Заголовок*</label>
          <input 
            type="text" 
            id="reviewTitle" 
            v-model="newReview.title" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
            required
          >
        </div>
        
        <div class="form-group mb-4">
          <label for="reviewContent" class="block text-sm font-medium text-gray-700 mb-1">Отзыв*</label>
          <textarea 
            id="reviewContent" 
            v-model="newReview.content" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
            rows="4"
            required
          ></textarea>
        </div>
        
        <div class="form-group mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Достоинства</label>
          <textarea 
            v-model="newReview.pros" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
            rows="2"
          ></textarea>
        </div>
        
        <div class="form-group mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Недостатки</label>
          <textarea 
            v-model="newReview.cons" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accent"
            rows="2"
          ></textarea>
        </div>
        
        <div class="form-actions flex gap-3">
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            <span v-if="isSubmitting">Отправка...</span>
            <span v-else>Отправить отзыв</span>
          </button>
          <button type="button" @click="cancelReview" class="btn-secondary">
            Отмена
          </button>
        </div>
      </form>
    </div>
    
    <!-- Список отзывов -->
    <div v-if="reviews.length > 0" class="reviews-list">
      <div v-for="review in sortedReviews" :key="review.id" class="review-item border-b border-gray-200 pb-6 mb-6">
        <div class="review-header flex justify-between items-start mb-2">
          <div>
            <h3 class="text-lg font-medium">{{ review.title }}</h3>
            <div class="review-meta text-sm text-gray-500">
              {{ review.name }} • {{ formatDate(review.date) }}
            </div>
          </div>
          <div class="review-rating flex items-center">
            <div class="stars text-yellow-400 mr-2">
              <span v-for="i in 5" :key="i" class="star">
                <span v-if="i <= review.rating">★</span>
                <span v-else class="text-gray-300">★</span>
              </span>
            </div>
            <span class="rating-value font-medium">{{ review.rating }}/5</span>
          </div>
        </div>
        
        <div class="review-content mb-3">
          <p>{{ review.content }}</p>
        </div>
        
        <div v-if="review.pros" class="review-pros mb-2">
          <div class="text-sm font-medium text-green-600">Достоинства:</div>
          <p class="text-sm">{{ review.pros }}</p>
        </div>
        
        <div v-if="review.cons" class="review-cons mb-2">
          <div class="text-sm font-medium text-red-600">Недостатки:</div>
          <p class="text-sm">{{ review.cons }}</p>
        </div>
        
        <div class="review-actions flex items-center mt-3">
          <button 
            @click="toggleHelpful(review.id)" 
            class="helpful-btn flex items-center text-sm text-gray-500 hover:text-gray-700"
            :class="{ 'text-accent': review.isHelpful }"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
            </svg>
            <span>Полезно ({{ review.helpfulCount }})</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Если нет отзывов -->
    <div v-else-if="!isReviewFormVisible" class="no-reviews text-center py-8">
      <p class="text-gray-500">У этого товара пока нет отзывов.</p>
      <p class="mt-2">Будьте первым, кто оставит отзыв!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  productId: {
    type: Number,
    required: true
  },
  initialReviews: {
    type: Array,
    default: () => []
  }
})

const reviews = ref(props.initialReviews.length > 0 ? props.initialReviews : [
  // Демо-отзывы для тестирования
  {
    id: 1,
    productId: props.productId,
    name: 'Алексей',
    email: 'alexey@example.com',
    title: 'Отличный дрон!',
    content: 'Купил этот дрон для съемки видео. Качество съемки на высоте, батарея держится долго. Очень доволен покупкой!',
    pros: 'Качество съемки, время работы батареи, простое управление',
    cons: 'Немного шумный при полете',
    rating: 5,
    date: new Date('2025-08-01'),
    helpfulCount: 3,
    isHelpful: false
  },
  {
    id: 2,
    productId: props.productId,
    name: 'Мария',
    email: 'maria@example.com',
    title: 'Хороший, но есть недостатки',
    content: 'В целом дрон неплохой, но есть некоторые проблемы с подключением к приложению. Иногда приходится перезапускать.',
    pros: 'Компактный размер, хорошая камера',
    cons: 'Проблемы с подключением, не очень стабильный в ветреную погоду',
    rating: 3,
    date: new Date('2025-07-15'),
    helpfulCount: 1,
    isHelpful: false
  }
])

const isReviewFormVisible = ref(false)
const isSubmitting = ref(false)

const ratingLabels = [
  'Ужасно',
  'Плохо',
  'Нормально',
  'Хорошо',
  'Отлично'
]

// Новый отзыв
const newReview = ref({
  name: '',
  email: '',
  title: '',
  content: '',
  pros: '',
  cons: '',
  rating: 0
})

// Сортировка отзывов: сначала новые
const sortedReviews = computed(() => {
  return [...reviews.value].sort((a, b) => new Date(b.date) - new Date(a.date))
})

// Показать форму отзыва
function showReviewForm() {
  isReviewFormVisible.value = true
}

// Отмена написания отзыва
function cancelReview() {
  isReviewFormVisible.value = false
  resetReviewForm()
}

// Сброс формы отзыва
function resetReviewForm() {
  newReview.value = {
    name: '',
    email: '',
    title: '',
    content: '',
    pros: '',
    cons: '',
    rating: 0
  }
}

// Отправка отзыва
async function submitReview() {
  if (newReview.value.rating === 0) {
    alert('Пожалуйста, выберите оценку')
    return
  }
  
  try {
    isSubmitting.value = true
    
    // В реальном приложении здесь был бы API-запрос для сохранения отзыва
    // const response = await api.post(`/products/${props.productId}/reviews`, newReview.value)
    
    // Имитация задержки запроса
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Добавляем отзыв в список
    const review = {
      id: Date.now(), // Генерируем временный ID
      productId: props.productId,
      ...newReview.value,
      date: new Date(),
      helpfulCount: 0,
      isHelpful: false
    }
    
    reviews.value.unshift(review)
    
    // Скрываем форму и сбрасываем её
    isReviewFormVisible.value = false
    resetReviewForm()
    
  } catch (error) {
    console.error('Ошибка при отправке отзыва:', error)
    alert('Произошла ошибка при отправке отзыва. Пожалуйста, попробуйте еще раз.')
  } finally {
    isSubmitting.value = false
  }
}

// Отметить отзыв как полезный
function toggleHelpful(reviewId) {
  const review = reviews.value.find(r => r.id === reviewId)
  if (review) {
    if (review.isHelpful) {
      review.helpfulCount--
      review.isHelpful = false
    } else {
      review.helpfulCount++
      review.isHelpful = true
    }
    
    // В реальном приложении здесь был бы API-запрос для сохранения оценки отзыва
    // api.post(`/reviews/${reviewId}/helpful`, { helpful: review.isHelpful })
  }
}

// Форматирование даты
function formatDate(date) {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}
</script>

<style scoped>
.btn-primary {
  @apply inline-block bg-accent text-white py-2 px-4 rounded-md text-center font-medium hover:opacity-90 transition-opacity;
}

.btn-secondary {
  @apply inline-block bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md text-center font-medium hover:bg-gray-50 transition-colors;
}

button:disabled {
  @apply opacity-50 cursor-not-allowed;
}

.star-btn {
  @apply cursor-pointer;
}

.star-btn:hover ~ .star-btn span {
  @apply text-gray-300;
}
</style>
