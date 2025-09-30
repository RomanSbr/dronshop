<template>
  <section class="product-section">
    <div class="section-head">
      <div>
        <h3 class="section-title">{{ title }}</h3>
        <p v-if="subtitle" class="section-subtitle">{{ subtitle }}</p>
      </div>
      <router-link
        :to="{ path: '/catalog', query: moreQuery }"
        class="section-link"
      >
        {{ t("common.more") }}
      </router-link>
    </div>

    <AsyncState :loading="loading" :error="error" :retry="load">
      <template #loading>
        <div class="grid-container" role="list">
          <SkeletonLoader
            v-for="i in 4"
            :key="`section-skeleton-${i}`"
            type="product-card"
            class="skeleton"
          />
        </div>
      </template>

      <template #default>
        <div v-if="items.length" class="grid-container" role="list">
          <ProductCard
            v-for="product in items"
            :key="product.id"
            :product="product"
            role="listitem"
          />
        </div>
        <p v-else class="empty">{{ t("common.error") }}</p>
      </template>
    </AsyncState>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import AsyncState from "./AsyncState.vue";
import ProductCard from "./ProductCard.vue";
import SkeletonLoader from "./SkeletonLoader.vue";
import api from "../shared/api";
import { useI18n } from "../shared/i18n";

const props = defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: "" },
  params: { type: Object, default: () => ({}) },
  moreQuery: { type: Object, default: () => ({}) },
});

const { t } = useI18n();

const items = ref([]);
const loading = ref(false);
const error = ref(null);

async function load() {
  loading.value = true;
  error.value = null;
  try {
    const { data } = await api.get("/products", {
      params: {
        page_size: 8,
        ...props.params,
      },
    });
    items.value = Array.isArray(data) ? data : data.items || [];
  } catch (e) {
    error.value = e;
  } finally {
    loading.value = false;
  }
}

onMounted(load);

watch(
  () => props.params,
  () => {
    load();
  },
  { deep: true },
);
</script>

<style scoped>
.product-section {
  @apply space-y-6;
}

.section-head {
  @apply flex items-center justify-between gap-4;
}

.section-title {
  @apply text-2xl font-semibold text-gray-900;
}

.section-subtitle {
  @apply text-sm text-gray-500;
}

.section-link {
  @apply text-sm font-medium text-accent-600 hover:text-accent-700 transition;
}

.grid-container {
  @apply grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 items-stretch;
}

.skeleton {
  @apply h-72 rounded-xl;
}

.empty {
  @apply text-sm text-gray-500;
}
</style>
