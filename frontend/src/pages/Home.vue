<template>
  <div class="home">
    <HeroSlider class="section" />

    <ProductSection
      class="section"
      :title="t('home.newArrivalsTitle')"
      :subtitle="t('home.newArrivalsSubtitle')"
      :params="{ sort: 'created_at:desc' }"
      :more-query="{ sort: 'created_at:desc' }"
    />

    <section class="section">
      <AsyncState
        :loading="isPromoLoading"
        :error="promoError"
        :retry="reloadPromo"
      >
        <div class="promo-grid">
          <article
            v-for="block in resolvedPromoBlocks"
            :key="block.id"
            class="promo-card"
          >
            <div class="promo-media" aria-hidden="true">
              <img :src="block.image" :alt="block.title" loading="lazy" />
              <div class="promo-overlay"></div>
            </div>
            <div class="promo-content">
              <h3 class="promo-title">{{ block.title }}</h3>
              <p class="promo-text">{{ block.description }}</p>
              <router-link :to="block.link" class="promo-cta">
                {{ block.cta }}
                <svg
                  class="promo-cta-icon"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </router-link>
            </div>
          </article>
        </div>
      </AsyncState>
    </section>

    <ProductSection
      class="section"
      :title="t('home.bestDealsTitle')"
      :subtitle="t('home.bestDealsSubtitle')"
      :params="{ sort: 'price:desc' }"
      :more-query="{ sort: 'price:desc' }"
    />

    <BrandStrip class="section" />

    <section class="section cta">
      <div class="cta-inner">
        <h2 class="cta-title">{{ t("home.ctaHeadline") }}</h2>
        <p class="cta-text">{{ t("home.ctaDescription") }}</p>
        <div class="cta-actions">
          <router-link to="/catalog" class="cta-primary">
            {{ t("home.ctaPrimary") }}
          </router-link>
          <router-link to="/about" class="cta-secondary">
            {{ t("home.ctaSecondary") }}
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import HeroSlider from "../components/HeroSlider.vue";
import ProductSection from "../components/ProductSection.vue";
import BrandStrip from "../components/BrandStrip.vue";
import AsyncState from "../components/AsyncState.vue";
import { useContentStore } from "../stores/content";
import { useI18n } from "../shared/i18n";

const contentStore = useContentStore();
const { t } = useI18n();

const isPromoLoading = computed(
  () =>
    contentStore.promoState.status === "loading" &&
    !contentStore.promoState.loaded,
);
const promoError = computed(() => contentStore.promoState.error);

const resolvedPromoBlocks = computed(() =>
  contentStore.promoBlocks.map((block) => ({
    ...block,
    title: resolveContentText(block, "title"),
    description: resolveContentText(block, "description"),
    cta: resolveContentText(block, "cta"),
  })),
);

function resolveContentText(block, field) {
  const key = block?.[`${field}Key`];
  if (key) {
    return t(key);
  }
  return block?.[field] ?? "";
}

async function reloadPromo() {
  await contentStore.fetchPromoBlocks({ force: true });
}

onMounted(() => {
  contentStore.fetchPromoBlocks();
});
</script>

<style scoped>
.home {
  @apply space-y-12 md:space-y-16 pb-12;
}

.section {
  @apply animate-fade-in;
}

.promo-grid {
  @apply grid grid-cols-1 md:grid-cols-2 gap-6;
}

.promo-card {
  @apply relative overflow-hidden rounded-2xl shadow-xl transition-transform duration-500 ease-out;
}

.promo-card:hover {
  @apply transform translate-y-[-6px] scale-[1.01];
}

.promo-media {
  @apply absolute inset-0;
}

.promo-media img {
  @apply w-full h-full object-cover transition-transform duration-[2000ms] ease-in-out;
}

.promo-card:hover .promo-media img {
  @apply scale-110;
}

.promo-overlay {
  @apply absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent;
}

.promo-content {
  @apply relative z-10 p-6 md:p-8 text-white flex flex-col gap-4 h-full justify-end;
}

.promo-title {
  @apply text-2xl md:text-3xl font-bold;
}

.promo-text {
  @apply text-white/80;
}

.promo-cta {
  @apply inline-flex items-center bg-white/20 backdrop-blur-sm text-white px-5 py-2 rounded-xl font-medium transition-colors duration-300;
}

.promo-cta:hover {
  @apply bg-white/30;
}

.promo-cta-icon {
  @apply w-4 h-4 ml-2 transition-transform duration-300;
}

.promo-cta:hover .promo-cta-icon {
  @apply translate-x-1;
}

.cta {
  @apply bg-gradient-to-r from-accent-600 to-accent-800 rounded-2xl text-white;
}

.cta-inner {
  @apply max-w-3xl mx-auto px-6 md:px-12 py-10 text-center space-y-6;
}

.cta-title {
  @apply text-3xl md:text-4xl font-bold;
}

.cta-text {
  @apply text-lg md:text-xl text-white/80;
}

.cta-actions {
  @apply flex flex-col sm:flex-row gap-4 justify-center;
}

.cta-primary {
  @apply bg-white text-accent-600 px-8 py-4 rounded-xl font-semibold text-lg transition-transform duration-300;
}

.cta-primary:hover {
  @apply transform -translate-y-1;
}

.cta-secondary {
  @apply border-2 border-white text-white px-8 py-4 rounded-xl font-semibold text-lg transition-transform duration-300;
}

.cta-secondary:hover {
  @apply transform -translate-y-1 bg-white/10;
}

@media (prefers-reduced-motion: reduce) {
  .section,
  .promo-card,
  .promo-media img,
  .cta-primary,
  .cta-secondary {
    transition-duration: 0.01ms !important;
    animation: none !important;
  }
}
</style>
