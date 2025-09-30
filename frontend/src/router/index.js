import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Catalog from '../pages/Catalog.vue'
import Product from '../pages/Product.vue'
import Auth from '../pages/Auth.vue'
import Register from '../pages/Register.vue'
import Profile from '../pages/Profile.vue'
import Cart from '../pages/Cart.vue'
import Checkout from '../pages/Checkout.vue'
import Favorites from '../pages/Favorites.vue'
import AdminIndex from '../pages/admin/AdminIndex.vue'
import AdminProducts from '../pages/admin/AdminProducts.vue'
import AdminCategories from '../pages/admin/AdminCategories.vue'
import StaticNew from '../pages/static/New.vue'
import StaticDelivery from '../pages/static/Delivery.vue'
import StaticPayment from '../pages/static/Payment.vue'
import StaticAbout from '../pages/static/About.vue'
import StaticContacts from '../pages/static/Contacts.vue'
import StaticPrivacy from '../pages/static/Privacy.vue'
import StaticTerms from '../pages/static/Terms.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/catalog', component: Catalog },
  { path: '/product/:id', component: Product },
  { path: '/auth', component: Auth },
  { path: '/register', component: Register },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/cart', component: Cart },
  { path: '/checkout', component: Checkout },
  { path: '/favorites', component: Favorites },
  { path: '/new', component: StaticNew },
  { path: '/delivery', component: StaticDelivery },
  { path: '/payment', component: StaticPayment },
  { path: '/about', component: StaticAbout },
  { path: '/contacts', component: StaticContacts },
  { path: '/privacy', component: StaticPrivacy },
  { path: '/terms', component: StaticTerms },
  { path: '/admin', component: AdminIndex, meta: { requiresAdmin: true } },
  { path: '/admin/products', component: AdminProducts, meta: { requiresAdmin: true } },
  { path: '/admin/categories', component: AdminCategories, meta: { requiresAdmin: true } },
  { path: '/admin/products/:id', component: () => import('../pages/admin/AdminProductDetail.vue'), meta: { requiresAdmin: true } },
  { path: '/admin/inventory', component: () => import('../pages/admin/AdminInventory.vue'), meta: { requiresAdmin: true } },
  { path: '/admin/orders', component: () => import('../pages/admin/AdminOrders.vue'), meta: { requiresAdmin: true } },
  { path: '/admin/orders/:id', component: () => import('../pages/admin/AdminOrderDetail.vue'), meta: { requiresAdmin: true } },
  { path: '/admin/reviews', component: () => import('../pages/admin/AdminReviews.vue'), meta: { requiresAdmin: true } },
  { path: '/admin/settings', component: () => import('../pages/admin/AdminSettings.vue'), meta: { requiresAdmin: true } }
  ,{ path: '/admin/users', component: () => import('../pages/admin/AdminUsers.vue'), meta: { requiresAdmin: true } }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

function isAccessTokenValid() {
  const t = localStorage.getItem('accessToken')
  if (!t) return false
  try {
    const base64Url = t.split('.')[1]
    if (!base64Url) return false
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const padding = (4 - (base64.length % 4)) % 4
    if (padding) base64 += '='.repeat(padding)
    const json = decodeURIComponent(atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''))
    const payload = JSON.parse(json)
    const now = Math.floor(Date.now() / 1000)
    return payload.exp && payload.exp > now
  } catch (e) {
    return false
  }
}

function parseRolesFromAccess() {
  const t = localStorage.getItem('accessToken')
  if (!t) return []
  try {
    const base64Url = t.split('.')[1]
    if (!base64Url) return []
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const padding = (4 - (base64.length % 4)) % 4
    if (padding) base64 += '='.repeat(padding)
    const json = decodeURIComponent(atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''))
    const payload = JSON.parse(json)
    const now = Math.floor(Date.now() / 1000)
    if (!payload.exp || payload.exp <= now) return []
    return Array.isArray(payload.roles) ? payload.roles : []
  } catch (e) {
    return []
  }
}

router.beforeEach((to, from, next) => {
  if (to.matched.some(r => r.meta && r.meta.requiresAuth)) {
    if (!isAccessTokenValid()) {
      return next('/auth')
    }
  }
  if (to.matched.some(r => r.meta && r.meta.requiresAdmin)) {
    const roles = parseRolesFromAccess()
    if (!roles.includes('admin')) {
      return next('/auth')
    }
  }
  next()
})
export default router
