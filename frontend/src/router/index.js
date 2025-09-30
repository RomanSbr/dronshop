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
  {
    path: '/admin/products/:id',
    component: () => import('../pages/admin/AdminProductDetail.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/inventory',
    component: () => import('../pages/admin/AdminInventory.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/orders',
    component: () => import('../pages/admin/AdminOrders.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/orders/:id',
    component: () => import('../pages/admin/AdminOrderDetail.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/reviews',
    component: () => import('../pages/admin/AdminReviews.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/settings',
    component: () => import('../pages/admin/AdminSettings.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/users',
    component: () => import('../pages/admin/AdminUsers.vue'),
    meta: { requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

function readToken(key) {
  if (typeof window === 'undefined') {
    return null
  }
  try {
    return window.localStorage.getItem(key)
  } catch (error) {
    console.warn('Unable to read token from storage', error)
    return null
  }
}

function decodeJwtPayload(token) {
  if (!token) return null
  const [, payload = ''] = token.split('.')
  if (!payload) return null
  try {
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/')
    const padded = normalized.padEnd(normalized.length + ((4 - (normalized.length % 4)) % 4), '=')
    const binary = atob(padded)
    const uriEncoded = binary
      .split('')
      .map((char) => `%${char.charCodeAt(0).toString(16).padStart(2, '0')}`)
      .join('')
    return JSON.parse(decodeURIComponent(uriEncoded))
  } catch (error) {
    console.warn('Unable to decode JWT payload', error)
    return null
  }
}

function isAccessTokenValid() {
  const payload = decodeJwtPayload(readToken('accessToken'))
  if (!payload?.exp) {
    return false
  }
  const now = Math.floor(Date.now() / 1000)
  return payload.exp > now
}

function parseRolesFromAccess() {
  const payload = decodeJwtPayload(readToken('accessToken'))
  if (!payload?.exp || payload.exp <= Math.floor(Date.now() / 1000)) {
    return []
  }
  return Array.isArray(payload.roles) ? payload.roles : []
}

router.beforeEach((to, from, next) => {
  if (typeof window === 'undefined') {
    next()
    return
  }

  const requiresAuth = to.matched.some((record) => record.meta?.requiresAuth)
  if (requiresAuth && !isAccessTokenValid()) {
    next({ path: '/auth', query: { redirect: to.fullPath } })
    return
  }

  const requiresAdmin = to.matched.some((record) => record.meta?.requiresAdmin)
  if (requiresAdmin) {
    const roles = parseRolesFromAccess()
    if (!roles.includes('admin')) {
      next('/auth')
      return
    }
  }

  next()
})

export default router

