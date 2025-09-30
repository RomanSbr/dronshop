const fs = require('fs');
const path = 'frontend/src/components/Header.vue';
let raw = fs.readFileSync(path, 'utf8');
if (!raw.includes("const isAuthenticated")) {
  raw = raw.replace(
    'const isAdmin = ref(false)',
    "const isAdmin = ref(false)const isAuthenticated = computed(() => !!localStorage.getItem('accessToken'))"
  );
}
const marker = ":to=\"isAuthenticated ? '/profile' : '/auth'\"";
const idx = raw.indexOf(marker);
if (idx >= 0) {
  const closeIdx = raw.indexOf('</router-link>', idx);
  if (closeIdx >= 0) {
    const insertion = " <button v-if=\"isAuthenticated\" @click=\"localStorage.removeItem('accessToken'); localStorage.removeItem('refreshToken'); window.dispatchEvent(new Event('auth-changed')); window.location.href='/auth'\" class=\"icon-action p-3 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 hover:border-accent-400/30 transition-all duration-300\" aria-label=\"Выйти\"><svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2h4a2 2 0 012 2v1\"/></svg><span class=\"hidden md:inline ml-2 text-sm font-medium\">Выйти</span></button>";
    raw = raw.slice(0, closeIdx + 14) + insertion + raw.slice(closeIdx + 14);
  }
}
fs.writeFileSync(path, raw, 'utf8');
console.log('Patched');
