<template>
  <div class="pagination" v-if="totalPages > 1">
    <button 
      class="pagination-btn prev" 
      :disabled="currentPage === 1"
      @click="changePage(currentPage - 1)"
      aria-label="Предыдущая страница"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>
    
    <div class="pagination-pages">
      <!-- Первая страница -->
      <button 
        v-if="showFirstPage" 
        class="pagination-page" 
        :class="{ 'active': currentPage === 1 }"
        @click="changePage(1)"
      >
        1
      </button>
      
      <!-- Эллипсис в начале -->
      <span v-if="showStartEllipsis" class="pagination-ellipsis">...</span>
      
      <!-- Средние страницы -->
      <button 
        v-for="page in visiblePages" 
        :key="page" 
        class="pagination-page" 
        :class="{ 'active': currentPage === page }"
        @click="changePage(page)"
      >
        {{ page }}
      </button>
      
      <!-- Эллипсис в конце -->
      <span v-if="showEndEllipsis" class="pagination-ellipsis">...</span>
      
      <!-- Последняя страница -->
      <button 
        v-if="showLastPage" 
        class="pagination-page" 
        :class="{ 'active': currentPage === totalPages }"
        @click="changePage(totalPages)"
      >
        {{ totalPages }}
      </button>
    </div>
    
    <button 
      class="pagination-btn next" 
      :disabled="currentPage === totalPages"
      @click="changePage(currentPage + 1)"
      aria-label="Следующая страница"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  maxVisiblePages: {
    type: Number,
    default: 5
  }
});

const emit = defineEmits(['page-change']);

// Функция для изменения страницы
function changePage(page) {
  if (page >= 1 && page <= props.totalPages) {
    emit('page-change', page);
  }
}

// Вычисляем видимые страницы
const visiblePages = computed(() => {
  const { currentPage, totalPages, maxVisiblePages } = props;
  
  // Если общее количество страниц меньше или равно максимальному количеству видимых страниц,
  // показываем все страницы
  if (totalPages <= maxVisiblePages) {
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  }
  
  // Иначе вычисляем диапазон видимых страниц
  let startPage = Math.max(currentPage - Math.floor(maxVisiblePages / 2), 2);
  let endPage = Math.min(startPage + maxVisiblePages - 3, totalPages - 1);
  
  if (endPage - startPage < maxVisiblePages - 3) {
    startPage = Math.max(endPage - (maxVisiblePages - 3) + 1, 2);
  }
  
  return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
});

// Определяем, нужно ли показывать первую страницу
const showFirstPage = computed(() => {
  return props.totalPages > 1;
});

// Определяем, нужно ли показывать последнюю страницу
const showLastPage = computed(() => {
  return props.totalPages > 1 && props.totalPages !== 1;
});

// Определяем, нужно ли показывать эллипсис в начале
const showStartEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[0] > 2;
});

// Определяем, нужно ли показывать эллипсис в конце
const showEndEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[visiblePages.value.length - 1] < props.totalPages - 1;
});
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 1.5rem 0;
}

.pagination-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  background-color: white;
  color: #374151;
  transition: background-color 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #f9fafb;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-pages {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.pagination-page {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  background-color: white;
  color: #374151;
  transition: background-color 0.2s ease;
}

.pagination-page:hover:not(.active) {
  background-color: #f9fafb;
}

.pagination-page.active {
  background-color: var(--accent);
  color: white;
  border-color: var(--accent);
}

.pagination-ellipsis {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  color: #9ca3af;
}

/* Мобильная оптимизация */
@media (max-width: 640px) {
  .pagination-page, .pagination-btn {
    width: 2rem;
    height: 2rem;
  }
  
  .pagination-ellipsis {
    width: 1.5rem;
  }
}
</style>
