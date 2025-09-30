<template>
  <nav class="breadcrumbs" aria-label="breadcrumb">
    <ol class="breadcrumbs-list">
      <li class="breadcrumb-item">
        <router-link to="/" class="breadcrumb-link home">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
        </router-link>
      </li>
      <li 
        v-for="(crumb, index) in breadcrumbs" 
        :key="index" 
        class="breadcrumb-item"
        :class="{ 'active': index === breadcrumbs.length - 1 }"
      >
        <span class="separator" aria-hidden="true">/</span>
        <router-link 
          v-if="index < breadcrumbs.length - 1" 
          :to="crumb.path" 
          class="breadcrumb-link"
        >
          {{ crumb.name }}
        </router-link>
        <span v-else class="current">{{ crumb.name }}</span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
  // Дополнительные хлебные крошки, которые можно передать извне
  additionalCrumbs: {
    type: Array,
    default: () => []
  }
});

const route = useRoute();

// Генерируем хлебные крошки на основе текущего маршрута
const breadcrumbs = computed(() => {
  const pathSegments = route.path.split('/').filter(segment => segment);
  const result = [];
  
  // Добавляем базовые хлебные крошки на основе маршрута
  let currentPath = '';
  
  for (const segment of pathSegments) {
    currentPath += `/${segment}`;
    
    // Преобразуем сегмент пути в удобочитаемое название
    let name = segment.charAt(0).toUpperCase() + segment.slice(1);
    
    // Специальные случаи для определенных маршрутов
    switch (segment) {
      case 'catalog':
        name = 'Каталог';
        break;
      case 'product':
        name = 'Товар';
        break;
      case 'cart':
        name = 'Корзина';
        break;
      case 'checkout':
        name = 'Оформление заказа';
        break;
      case 'profile':
        name = 'Профиль';
        break;
      case 'admin':
        name = 'Админ';
        break;
    }
    
    result.push({
      name,
      path: currentPath
    });
  }
  
  // Добавляем дополнительные хлебные крошки, если они есть
  return [...result, ...props.additionalCrumbs];
});
</script>

<style scoped>
.breadcrumbs {
  margin-bottom: 1rem;
}

.breadcrumbs-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding: 0;
  margin: 0;
  list-style: none;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
}

.breadcrumb-link {
  color: var(--accent);
  transition: color 0.2s ease;
}

.breadcrumb-link:hover {
  color: rgba(0, 37, 89, 0.8); /* var(--accent) с прозрачностью 0.8 */
}

.breadcrumb-link.home {
  display: flex;
  align-items: center;
  justify-content: center;
}

.separator {
  margin: 0 0.5rem;
  color: #9ca3af; /* gray-400 */
}

.current {
  color: #4b5563; /* gray-600 */
  font-weight: 500;
}

.active {
  pointer-events: none;
}
</style>
