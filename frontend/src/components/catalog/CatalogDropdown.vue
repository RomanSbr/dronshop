<template>
  <div class="catalog" ref="root" @keydown.escape="close">
    <button class="cd-btn" @click.stop="toggle" :aria-expanded="open" aria-haspopup="true">
      <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">
        <rect width="16" height="2"/><rect y="7" width="16" height="2"/><rect y="14" width="16" height="2"/>
      </svg>
      <span>Каталог товаров</span>
      <svg class="chev" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6" fill="currentColor"/></svg>
    </button>

    <transition name="fade-scale">
      <div v-if="open" class="cd-panel" ref="panel" @mouseenter="hovering=true" @mouseleave="close">
        <div class="cd-arrow"/>
        <div class="cd-grid">
          <router-link
            v-for="c in cats"
            :key="c.id"
            class="cd-item"
            :to="{ path: '/catalog', query: { category: c.id, sort: 'created_at:desc' } }"
            @click="close"
            >
            <span class="cd-name">{{ c.name }}</span>
          </router-link>
        </div>
      </div>
    </transition>
  </div>
  </template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import api from '../../shared/api'

const open = ref(false)
const hovering = ref(false)
const cats = ref([])
const panel = ref(null)
const root = ref(null)

function toggle(){ open.value = !open.value }
function close(){ open.value = false }

function onClickOutside(e){
  // Close only if click is outside the whole component (button + panel)
  if (!root.value) return
  if (!root.value.contains(e.target)) close()
}

onMounted(async () => {
  try {
    const { data } = await api.get('/categories')
    cats.value = Array.isArray(data) ? data : []
  } catch {
    cats.value = []
  }
  document.addEventListener('click', onClickOutside)
})

onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<style scoped>
.catalog { position: relative; }
.cd-btn { display: inline-flex; align-items: center; gap: 10px; background: var(--accent, #2563eb); color: #fff; border: none; border-radius: 12px; padding: 10px 14px; cursor: pointer; box-shadow: 0 4px 16px rgba(37,99,235,.25); transition: transform .15s ease, box-shadow .2s ease; }
.cd-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(37,99,235,.3); }
.cd-btn svg { fill: currentColor; }
.cd-btn .chev { opacity:.9; }

.cd-panel { position: absolute; top: calc(100% + 10px); left: 0; background: #fff; border: 1px solid #e5e7eb; border-radius: 14px; box-shadow: 0 20px 40px rgba(0,0,0,0.12); padding: 14px; z-index: 50; min-width: 520px; }
.cd-arrow { position: absolute; top: -8px; left: 24px; width: 16px; height: 16px; background: #fff; border-left: 1px solid #e5e7eb; border-top: 1px solid #e5e7eb; transform: rotate(45deg); }
.cd-grid { display: grid; grid-template-columns: repeat(3, minmax(140px,1fr)); gap: 10px; }
.cd-item { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 10px; border: 1px solid #eff3f7; color: #111827; text-decoration: none; background: #fff; transition: background .15s ease, transform .15s ease, border-color .2s ease; }
.cd-item:hover { background: #f8fafc; border-color: #e5e7eb; transform: translateY(-1px); }
.cd-name { font-weight: 500; }

.fade-scale-enter-active, .fade-scale-leave-active { transition: opacity .15s ease, transform .15s ease; transform-origin: 24px 0; }
.fade-scale-enter-from, .fade-scale-leave-to { opacity:0; transform: scale(.98); }
</style>
