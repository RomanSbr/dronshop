<template>
  <footer class="site-footer bg-gradient-to-b from-gray-900 to-gray-950 text-white pt-16 pb-8">
    <div class="container mx-auto px-4">
      <div class="footer-content grid grid-cols-1 md:grid-cols-12 gap-8 mb-12">
        <!-- Бренд и краткое описание -->
        <div class="footer-brand md:col-span-4">
          <router-link to="/" class="brand-logo inline-block mb-6 hover-lift">
            <img src="/brand.svg" alt="GLORYAIR" height="40" class="transition-transform duration-300 hover:scale-105" />
          </router-link>
          <p class="brand-description text-gray-300 text-lg leading-relaxed mb-6 max-w-md">
            Современный магазин дронов. Подберём технику для спорта и съёмок,
            настроим под ваши задачи и поможем с обслуживанием.
          </p>
          <div class="social-links flex gap-4">
            <a href="#" class="social-link w-12 h-12 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center transition-all duration-300 hover-lift hover:bg-accent-600 hover:scale-110 group" aria-label="Telegram">
              <svg class="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm.14 19.018c-.237 0-.47-.033-.696-.08l-3.26.93 1.376-3.242a5.077 5.077 0 01-.754-2.685c0-2.834 2.326-5.133 5.196-5.133 2.87 0 5.196 2.3 5.196 5.133 0 2.833-2.325 5.132-5.195 5.132h-.002c-.423 0-.833-.05-1.228-.145l-1.757.945.922-1.854z"/></svg>
            </a>
            <a href="#" class="social-link w-12 h-12 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center transition-all duration-300 hover-lift hover:bg-blue-600 hover:scale-110 group" aria-label="VK">
              <svg class="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24"><path d="M21.547 7h-3.29a.743.743 0 0 0-.655.392s-1.312 2.416-1.734 3.23c-1.232 2.203-2.356 3.101-2.797 3.101-.145 0-.287-.07-.487-.405V7.392A.64.64 0 0 0 12 6.752h-2c-.55 0-.854.267-.854.64 0 .635.790.785.874 2.518v3.329c-.18.163-.23.217-.414.217-.62 0-2.055-.834-3.109-2.745-.45-.818-.87-1.749-.87-1.749a.697.697 0 0 0-.564-.313H2.453a.73.73 0 0 0-.729.681c0 .635.535 2.948 2.585 6.082C5.418 17.749 7.94  19,10.212 19c1.371 0 1.54-.3 1.54-.819v-1.891c0-.603.129-.723.562-.723.319 0 .889.158 2.11 1.392 1.446 1.446 1.666 2.041 2.5 2.041h3.294c.358 0 .538-.173.538-.49 0-.59-.732-1.684-1.897-2.808-.526-.558-1.309-1.16-1.546-1.437-.319-.329-.319-.46 0-.818 0 0 2.72-3.765 3.005-5.040.232-.868 0-1.213-.48-1.213z"/></svg>
            </a>
            <a href="#" class="social-link w-12 h-12 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center transition-all duration-300 hover-lift hover:bg-red-600 hover:scale-110 group" aria-label="YouTube">
              <svg class="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
          </div>
        </div>

        <!-- Навигация -->
        <div class="footer-nav md:col-span-8 grid grid-cols-1 sm:grid-cols-3 gap-8">
          <div class="nav-column">
            <h3 class="nav-title text-xl font-bold mb-6 gradient-text">Каталог</h3>
            <ul class="nav-list space-y-3">
              <li><router-link to="/catalog" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift">Все товары</router-link></li>
              <li><router-link to="/catalog?tag=new" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift">Новинки</router-link></li>
              <li><router-link to="/catalog?tag=best" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift">Лучшие предложения</router-link></li>
            </ul>
          </div>

          <div class="nav-column">
            <h3 class="nav-title text-xl font-bold mb-6 gradient-text">Информация</h3>
            <ul class="nav-list space-y-3">
              <li><router-link to="/delivery" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift">Доставка</router-link></li>
              <li><router-link to="/payment" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift">Оплата</router-link></li>
              <li><router-link to="/about" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift">О компании</router-link></li>
            </ul>
          </div>

          <div class="nav-column">
            <h3 class="nav-title text-xl font-bold mb-6 gradient-text">Контакты</h3>
            <ul class="nav-list space-y-3">
              <li>
                <a href="tel:+79990000000" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift flex items-center group">
                  <svg class="w-5 h-5 mr-3 text-accent-400 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                  +7 (999) 000-00-00
                </a>
              </li>
              <li>
                <a href="mailto:info@example.com" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift flex items-center group">
                  <svg class="w-5 h-5 mr-3 text-accent-400 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12H8m8 0l-8 5m8-5l-8-5"/></svg>
                  info@example.com
                </a>
              </li>
              <li>
                <a href="#" class="nav-link text-gray-300 hover:text-white transition-colors duration-300 hover-lift flex items-center group">
                  <svg class="w-5 h-5 mr-3 text-accent-400 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  г. Москва, ул. Электрозаводская, д. 123
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Нижняя полоса и ссылки -->
      <div class="footer-bottom pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="copyright text-gray-400 text-sm">© {{ currentYear }} GLORYAIR. Все права защищены.</div>
        <div class="footer-links flex gap-6">
          <router-link to="/privacy" class="footer-link text-gray-400 hover:text-white transition-colors duration-300 text-sm">Политика конфиденциальности</router-link>
          <router-link to="/terms" class="footer-link text-gray-400 hover:text-white transition-colors duration-300 text-sm">Пользовательское соглашение</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from "vue";
const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-link::before {
  content: "";
  @apply w-2 h-2 bg-accent-400 rounded-full mr-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300;
}

.nav-link { @apply transition-all duration-300 ease-out; }
.nav-link:hover { transform: translateX(4px); }

.social-link { @apply transition-all duration-500 ease-out; }
.social-link:hover { transform: translateY(-2px) rotate(5deg); }

@media (max-width: 768px) {
  .footer-content { @apply gap-12; }
  .footer-nav { @apply gap-8; }
  .footer-bottom { @apply flex-col items-center text-center; }
}

:deep(.dark-theme) .site-footer { @apply bg-gradient-to-b from-gray-950 to-black; }
:deep(.dark-theme) .nav-link { @apply text-gray-400; }
:deep(.dark-theme) .nav-link:hover { @apply text-white; }
</style>
