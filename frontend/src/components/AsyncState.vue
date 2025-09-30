<template>
  <div>
    <template v-if="loading">
      <slot name="loading">
        <div class="async-state async-state--loading">
          <span class="spinner" aria-hidden="true"></span>
          <span class="sr-only">{{ t('common.loading') }}</span>
        </div>
      </slot>
    </template>
    <template v-else-if="error">
      <slot name="error" :retry="retry">
        <div class="async-state async-state--error">
          <p>{{ t('common.error') }}</p>
          <button class="retry" type="button" @click="retry" v-if="retry">
            {{ t('common.retry') }}
          </button>
        </div>
      </slot>
    </template>
    <slot v-else></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from '../shared/i18n'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: [Boolean, Object, String],
    default: false
  },
  retry: {
    type: Function,
    default: null
  }
})

const { t } = useI18n()

const hasError = computed(() => Boolean(props.error))
</script>

<style scoped>
.async-state {
  @apply flex flex-col items-center justify-center gap-3 text-center py-6 text-sm text-muted-dark;
}

.async-state--loading {
  @apply text-muted-dark;
}

.spinner {
  width: 1.75rem;
  height: 1.75rem;
  border: 2px solid rgba(148, 163, 184, 0.3);
  border-top-color: rgba(37, 99, 235, 0.8);
  border-radius: 999px;
  animation: spin 0.8s linear infinite;
}

.retry {
  @apply inline-flex items-center gap-2 px-3 py-2 rounded-lg border border-accent-200 text-accent-700 hover:bg-accent-50 transition;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
</style>
