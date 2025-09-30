<template>
  <article
    class="product-card group relative h-full flex flex-col"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div class="thumb">
      <router-link :to="productLink" class="block" :aria-label="product.name">
        <LazyImage
          v-if="product.image"
          :src="product.image"
          :alt="product.name"
          :width="300"
          :height="300"
          img-class="thumb-image"
        />
        <div v-else class="thumb-placeholder" aria-hidden="true">
          <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>

        <div class="thumb-overlay"></div>
      </router-link>

      <div class="badges">
        <span v-if="isNew" class="badge badge-new">{{ t("common.new") }}</span>
        <span v-if="isHit" class="badge badge-hit">{{ t("common.hit") }}</span>
        <span v-if="isOutOfStock" class="badge badge-out">{{
          t("common.outOfStock")
        }}</span>
      </div>

      <button
        class="favorite-btn"
        type="button"
        :class="{ active: isFavorite }"
        :aria-label="favoriteLabel"
        :aria-pressed="isFavorite"
        @click.prevent="toggleFavorite"
      >
        <svg
          class="favorite-icon"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            :fill="isFavorite ? 'currentColor' : 'none'"
          />
        </svg>
        <span class="favorite-tooltip">{{ favoriteLabel }}</span>
      </button>
      <!-- Ховер‑оверлей только по изображению -->
      <div class="hover-panel hidden md:flex">
        <div class="hover-content">
          <h4 class="hover-title">{{ product.name }}</h4>
          <p class="hover-text">{{ hoverDescription }}</p>
          <router-link :to="productLink" class="hover-details">
            {{ t('common.viewDetails') }}
          </router-link>
        </div>
      </div>
    </div>

    <div class="info flex-1">
      <router-link :to="productLink" class="title-link">
        <h3 class="title">{{ product.name }}</h3>
      </router-link>

      <div class="price">
        <span class="price-current">{{ formattedPrice }}</span>
        <span v-if="product.old_price" class="price-old">
          {{ formattedOldPrice }}
        </span>
      </div>

    </div>

    <!-- Small floating add-to-cart button that expands on hover -->
    <button
      type="button"
      class="fly-cart"
      :disabled="isOutOfStock"
      :aria-disabled="isOutOfStock"
      @click="addToCart"
    >
      <svg class="fly-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4m-8 2a2 2 0 11-4 0 2 2 0 014 0"/>
      </svg>
      <span class="fly-label">{{ t('common.addToCart') }}</span>
    </button>
  </article>
</template>

<script setup>
import { computed, ref } from "vue";
import { useCartStore } from "../stores/cart";
import { useFavoritesStore } from "../stores/favorites";
import { useI18n } from "../shared/i18n";
import LazyImage from "./LazyImage.vue";

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["quick-view"]);

const cartStore = useCartStore();
const favoritesStore = useFavoritesStore();
const { t } = useI18n();

const isHovered = ref(false);

const productLink = computed(() => `/product/${props.product.id}`);

const isOutOfStock = computed(() => {
  if (props.product.in_stock !== undefined) {
    return !props.product.in_stock;
  }
  if (props.product.stock !== undefined) {
    return props.product.stock <= 0;
  }
  return props.product.active === false;
});

const isNew = computed(() => {
  if (!props.product.created_at) return false;
  const createdDate = new Date(props.product.created_at);
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  return createdDate > thirtyDaysAgo;
});

const isHit = computed(() =>
  Boolean(
    props.product.is_hit ||
      (props.product.sales_count && props.product.sales_count > 25),
  ),
);

const isFavorite = computed(() =>
  favoritesStore.isInFavorites(props.product.id),
);

const favoriteLabel = computed(() =>
  isFavorite.value
    ? t("common.removeFromFavorites")
    : t("common.addToFavorites"),
);

const formattedPrice = computed(() => formatCurrency(props.product.price));
const formattedOldPrice = computed(() =>
  formatCurrency(props.product.old_price),
);

const hoverDescription = computed(
  () =>
    props.product.short_description ||
    props.product.description?.slice(0, 120) ||
    "",
);

function formatCurrency(value) {
  if (value === null || value === undefined) return "";
  return `${Number(value).toLocaleString()} ${t("common.rub")}`;
}

function addToCart() {
  if (isOutOfStock.value) return;
  cartStore.addItem(props.product);
}

function toggleFavorite() {
  favoritesStore.toggleFavorite(props.product);
}
</script>

<style scoped>
.product-card {
  @apply bg-white rounded-2xl overflow-hidden shadow-lg transform transition-transform duration-300 ease-out hover:scale-105 hover:shadow-2xl;
}

.thumb {
  @apply relative overflow-hidden rounded-t-2xl;
}

.thumb-image {
  @apply w-full h-56 md:h-60 object-cover transition-transform duration-700;
}

.thumb-placeholder {
  @apply w-full h-56 md:h-60 flex items-center justify-center bg-gray-100;
}

.thumb-overlay {
  @apply absolute inset-0 bg-gradient-to-t from-black/10 via-transparent to-transparent opacity-0 transition-opacity duration-300;
}

.group:hover .thumb-overlay {
  @apply opacity-100;
}

/* quick-view removed */

.badges {
  @apply absolute top-3 left-3 flex flex-col gap-2 z-10;
}

.badge {
  @apply px-3 py-1.5 rounded-full text-xs font-bold shadow-lg text-white;
}

.badge-new {
  @apply bg-gradient-to-r from-blue-500 to-blue-600;
}

.badge-hit {
  @apply bg-gradient-to-r from-amber-500 to-amber-600;
}

.badge-out {
  @apply bg-gradient-to-r from-red-500 to-red-600;
}

.favorite-btn {
  @apply absolute top-3 right-3 w-10 h-10 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-lg transition-transform duration-300;
}

.favorite-btn:hover {
  @apply scale-110;
}

.favorite-btn.active {
  @apply text-red-500 bg-red-50;
}

.favorite-icon {
  @apply w-5 h-5 transition-colors duration-300;
}

.favorite-tooltip {
  @apply absolute -bottom-8 left-1/2 -translate-x-1/2 bg-black/80 text-white text-xs px-2 py-1 rounded opacity-0 transition-opacity duration-300 whitespace-nowrap;
}

.favorite-btn:hover .favorite-tooltip {
  @apply opacity-100;
}

.info {
  @apply p-4 flex flex-col gap-3 border-t border-gray-100;
  padding-bottom: 1rem; /* reserve a bit of space by default */
  transition: padding-bottom 200ms ease;
}

/* When hovering the card, add extra bottom padding so the fly-cart doesn't overlap price */
.group:hover .info { padding-bottom: 3.25rem; }

.title-link {
  @apply group/title block;
}

.title {
  @apply font-semibold text-gray-900 line-clamp-2 text-sm md:text-base leading-tight mb-2 transition-colors duration-300;
  /* резервируем высоту под 2 строки, чтобы карточки были одинаковой высоты */
  min-height: 2.5rem; /* ~2 строки для text-sm */
}
@media (min-width: 768px) {
  .title { min-height: 3rem; } /* ~2 строки для text-base */
}

.group\/title:hover .title {
  @apply text-accent-600;
}

.price {
  @apply text-lg font-bold text-accent-600 mb-4 flex items-center gap-2;
  min-height: 1.75rem; /* резерв под одну строку */
}

.price-old {
  @apply text-sm text-gray-400 line-through font-normal;
}

.actions {
  @apply mt-auto flex gap-2;
}

.cart-btn {
  @apply flex-1 inline-flex items-center justify-center bg-gradient-to-r from-accent-600 to-accent-700 text-white py-3 px-4 rounded-xl font-medium transition-all duration-300;
}

.cart-btn:disabled,
.cart-btn[aria-disabled="true"] {
  @apply opacity-50 cursor-not-allowed;
}

.details-btn {
  @apply flex items-center justify-center bg-white border border-gray-200 text-gray-700 py-3 px-4 rounded-xl font-medium transition-all duration-300;
}

.details-btn:hover {
  @apply hover-lift bg-accent-50 border-accent-200 text-accent-700;
}

.hover-panel {
  @apply absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent opacity-0 transition-opacity duration-300 rounded-t-2xl flex items-end justify-start p-4;
  pointer-events: none;
}

.group:hover .hover-panel { @apply opacity-100; pointer-events: auto; }

.hover-title { @apply text-base md:text-lg font-bold text-white leading-snug line-clamp-3; }

.hover-text { @apply text-sm text-white/90 line-clamp-3; }

.hover-details { @apply inline-flex items-center bg-white/90 text-accent-700 hover:bg-white px-4 py-2 rounded-lg font-medium transition-colors duration-200; }

/* Compact floating cart button: hidden by default, appears on hover/focus */
.fly-cart {
  @apply absolute bottom-3 right-3 inline-flex items-center h-10 rounded-xl bg-accent-600 text-white shadow-lg overflow-hidden transition-all duration-200 ease-out z-10;
  width: 44px;
  opacity: 0;
  pointer-events: none;
  transform: translateY(4px);
}
.fly-cart:disabled, .fly-cart[aria-disabled="true"] { @apply opacity-50 cursor-not-allowed; }
.fly-icon { @apply w-5 h-5 mx-3; }
.fly-label { @apply text-sm font-semibold pr-4 opacity-0 transition-opacity duration-150 whitespace-nowrap; }
.group:hover .fly-cart, .group:focus-within .fly-cart { width: 140px; opacity: 1; pointer-events: auto; transform: translateY(0); }
.group:hover .fly-cart .fly-label, .group:focus-within .fly-cart .fly-label { @apply opacity-100; }

/* Tweaks for cleaner catalog cards */
.thumb-image { @apply h-56 md:h-60; }
.thumb-placeholder { @apply h-56 md:h-60; }
.info { @apply border-t border-gray-100; }
.price-row { @apply flex items-center justify-between mb-3; }
.details-link { @apply text-sm font-medium text-accent-600 hover:text-accent-700 transition-colors; }

/* duplicate fly-cart styles removed above */
</style>







