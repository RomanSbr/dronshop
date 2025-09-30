<template>
  <section
    ref="heroRef"
    class="hero-slider"
    role="region"
    aria-roledescription="carousel"
    :aria-label="t('home.heroCta')"
  >
    <AsyncState :loading="isLoading" :error="heroError" :retry="reload">
      <div
        v-if="slides.length"
        class="hero-shell"
        @mouseenter="handleHover(true)"
        @mouseleave="handleHover(false)"
      >
        <div class="slides-container">
          <article
            v-for="(slide, i) in slides"
            :key="slide.id || i"
            class="slide"
            :class="slideClasses(i)"
            :aria-hidden="index !== i"
          >
            <div class="media">
              <img
                class="media-img"
                :src="slide.image"
                :alt="resolveText(slide, 'title')"
                loading="lazy"
              />
              <div class="media-gradient" aria-hidden="true"></div>
            </div>
            <div class="content">
              <h2 class="headline">{{ resolveText(slide, "title") }}</h2>
              <p class="subtitle">{{ resolveText(slide, "subtitle") }}</p>
              <router-link class="cta" :to="slide.link || '/'">
                {{ resolveText(slide, "cta") || t("home.heroCta") }}
                <svg
                  class="cta-icon"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17 8l4 4m0 0l-4 4m4-4H3"
                  />
                </svg>
              </router-link>
            </div>
          </article>
        </div>

        <div class="controls">
          <button
            class="control"
            type="button"
            @click="prevSlide"
            :aria-label="t('hero.ariaPrev')"
          >
            <svg
              class="control-icon"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </button>

          <button
            class="control"
            type="button"
            @click="toggleAutoplay"
            :aria-label="autoplayLabel"
            :aria-pressed="isAutoplaying"
          >
            <svg
              v-if="isAutoplaying"
              class="control-icon"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 9v6m4-6v6"
              />
            </svg>
            <svg
              v-else
              class="control-icon"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M14.752 11.168l-5.197-3.03A1 1 0 008 9.03v5.94a1 1 0 001.555.832l5.197-3.03a1 1 0 000-1.664z"
              />
            </svg>
          </button>

          <button
            class="control"
            type="button"
            @click="nextSlide"
            :aria-label="t('hero.ariaNext')"
          >
            <svg
              class="control-icon"
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
          </button>
        </div>

        <div class="dots" role="tablist">
          <button
            v-for="(slide, i) in slides"
            :key="slide.id || `dot-${i}`"
            class="dot"
            :class="{ active: index === i }"
            type="button"
            role="tab"
            :aria-selected="index === i"
            :aria-label="`${resolveText(slide, 'title')} — ${i + 1}`"
            @click="goTo(i)"
          >
            <span class="dot-tooltip">{{ resolveText(slide, "title") }}</span>
          </button>
        </div>

        <div class="progress" aria-hidden="true">
          <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
        </div>
      </div>
    </AsyncState>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import AsyncState from "./AsyncState.vue";
import { useContentStore } from "../stores/content";
import { useI18n } from "../shared/i18n";

const contentStore = useContentStore();
const { t } = useI18n();

const heroRef = ref(null);
const index = ref(0);
const progress = ref(0);
const isAutoplaying = ref(true);

let rafId = null;
let mediaQuery = null;
let observer = null;

const SLIDE_DURATION = 7000;

const slides = computed(() => contentStore.heroSlides);
const isLoading = computed(
  () =>
    contentStore.heroState.status === "loading" &&
    !contentStore.heroState.loaded,
);
const heroError = computed(() => contentStore.heroState.error);

const autoplayLabel = computed(() =>
  isAutoplaying.value ? t("hero.pause") : t("hero.play"),
);

function resolveText(slide, field) {
  if (!slide) return "";
  const key = slide[`${field}Key`];
  if (key) return t(key);
  return slide[field] ?? "";
}

function slideClasses(i) {
  return {
    active: index.value === i,
    previous: index.value > i,
    next: index.value < i,
  };
}

function goTo(i) {
  index.value = i;
  restartAutoplay();
}

function nextSlide() {
  if (!slides.value.length) return;
  index.value = (index.value + 1) % slides.value.length;
  restartAutoplay();
}

function prevSlide() {
  if (!slides.value.length) return;
  index.value = (index.value - 1 + slides.value.length) % slides.value.length;
  restartAutoplay();
}

function handleHover(value) {
  if (value) {
    pauseAutoplay();
  } else if (isAutoplaying.value) {
    restartAutoplay();
  }
}

function toggleAutoplay() {
  if (isAutoplaying.value) {
    isAutoplaying.value = false;
    pauseAutoplay();
  } else {
    isAutoplaying.value = true;
    restartAutoplay();
  }
}

function pauseAutoplay() {
  cancelAnimation();
  progress.value = 0;
}

function restartAutoplay() {
  cancelAnimation();
  if (
    !isAutoplaying.value ||
    prefersReducedMotion.value ||
    slides.value.length <= 1
  ) {
    progress.value = 0;
    return;
  }
  const start = performance.now();
  const step = (timestamp) => {
    const elapsed = timestamp - start;
    progress.value = Math.min((elapsed / SLIDE_DURATION) * 100, 100);
    if (elapsed >= SLIDE_DURATION) {
      nextSlide();
      return;
    }
    rafId = requestAnimationFrame(step);
  };
  rafId = requestAnimationFrame(step);
}

function cancelAnimation() {
  if (rafId) {
    cancelAnimationFrame(rafId);
    rafId = null;
  }
}

const prefersReducedMotion = ref(false);

function setupReducedMotionListener() {
  if (typeof window === "undefined" || !window.matchMedia) return;
  mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  const update = () => {
    prefersReducedMotion.value = mediaQuery.matches;
    if (prefersReducedMotion.value) {
      pauseAutoplay();
    } else if (isAutoplaying.value) {
      restartAutoplay();
    }
  };
  mediaQuery.addEventListener("change", update);
  prefersReducedMotion.value = mediaQuery.matches;
  update();

  onBeforeUnmount(() => {
    mediaQuery.removeEventListener("change", update);
  });
}

function setupVisibilityObserver() {
  if (typeof IntersectionObserver === "undefined") return;
  observer = new IntersectionObserver(
    (entries) => {
      const [entry] = entries;
      if (!entry) return;
      if (
        entry.isIntersecting &&
        isAutoplaying.value &&
        !prefersReducedMotion.value
      ) {
        restartAutoplay();
      } else {
        pauseAutoplay();
      }
    },
    { threshold: 0.4 },
  );

  if (heroRef.value) {
    observer.observe(heroRef.value);
  }
}

function cleanup() {
  cancelAnimation();
  if (observer) {
    if (heroRef.value) {
      observer.unobserve(heroRef.value);
    }
    if (typeof observer.disconnect === "function") {
      observer.disconnect();
    }
    observer = null;
  }
}

async function reload() {
  await contentStore.fetchHeroSlides({ force: true });
  index.value = 0;
  restartAutoplay();
}

onMounted(async () => {
  await contentStore.fetchHeroSlides();
  setupReducedMotionListener();
  setupVisibilityObserver();
  if (!prefersReducedMotion.value) {
    restartAutoplay();
  }
});

onBeforeUnmount(() => {
  cleanup();
});

watch(slides, (newSlides) => {
  if (!newSlides.length) {
    pauseAutoplay();
    return;
  }
  if (index.value >= newSlides.length) {
    index.value = 0;
  }
  restartAutoplay();
});
</script>

<style scoped>
.hero-slider {
  @apply relative overflow-hidden rounded-2xl shadow-2xl bg-gray-900 text-white;
}

.hero-shell {
  @apply relative;
}

.slides-container {
  @apply relative h-96 md:h-[500px] flex items-center;
}

.slide {
  @apply absolute inset-0 flex flex-col md:flex-row items-center justify-center gap-6 md:gap-12 px-6 md:px-12 transition-opacity duration-700 ease-out;
  opacity: 0;
  pointer-events: none;
}

.slide.active {
  opacity: 1;
  pointer-events: auto;
}

.media {
  @apply absolute inset-0 overflow-hidden;
}

.media-img {
  @apply w-full h-full object-cover scale-105 transition-transform duration-[3000ms] ease-[cubic-bezier(0.25,0.1,0.25,1)];
}

.slide.active .media-img {
  transform: scale(1.05);
}

.media-gradient {
  @apply absolute inset-0 bg-gradient-to-r from-black/60 via-black/30 to-black/0;
}

.content {
  @apply relative z-10 max-w-2xl text-center md:text-left space-y-6;
}

.headline {
  @apply text-3xl md:text-5xl font-bold drop-shadow-[0_2px_8px_rgba(0,0,0,0.6)];
}

.subtitle {
  @apply text-lg md:text-xl text-white/90 drop-shadow-[0_1px_6px_rgba(0,0,0,0.5)];
}

.cta {
  @apply inline-flex items-center bg-accent-600 hover:bg-accent-700 text-white px-6 md:px-8 py-3 md:py-4 rounded-xl font-semibold text-lg transition-transform duration-300;
}

.cta:hover {
  @apply translate-y-[-3px];
}

.cta-icon {
  @apply w-5 h-5 ml-2 transition-transform duration-300;
}

.cta:hover .cta-icon {
  @apply translate-x-1;
}

.controls {
  @apply absolute inset-x-0 bottom-6 flex justify-center gap-3 z-20;
}

.control {
  @apply w-11 h-11 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full flex items-center justify-center text-white transition-colors duration-300;
}

.control:hover {
  @apply bg-white/20;
}

.control-icon {
  @apply w-5 h-5;
}

.dots {
  @apply absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-3 z-20;
}

.dot {
  @apply w-3 h-3 rounded-full bg-white/40 transition-all duration-300 relative;
}

.dot.active {
  @apply bg-white scale-125;
}

.dot-tooltip {
  @apply absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 text-xs bg-black/80 text-white rounded opacity-0 transition-opacity duration-300 whitespace-nowrap;
}

.dot:hover .dot-tooltip,
.dot:focus-visible .dot-tooltip {
  @apply opacity-100;
}

.progress {
  @apply absolute bottom-0 left-0 right-0 h-1 bg-white/20;
}

.progress-fill {
  @apply h-full bg-accent-400 transition-[width] duration-200 ease-linear;
}

@media (max-width: 768px) {
  .slides-container {
    @apply h-80;
  }

  .controls {
    @apply bottom-4;
  }

  .dots {
    @apply bottom-16;
  }
}

@media (max-width: 640px) {
  .slides-container {
    @apply h-72;
  }

  .headline {
    @apply text-2xl;
  }

  .subtitle {
    @apply text-base;
  }

  .cta {
    @apply text-base px-5 py-3;
  }
}
</style>
