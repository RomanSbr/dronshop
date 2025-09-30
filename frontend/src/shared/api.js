import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

// A bare client without interceptors to avoid loops when refreshing
const refreshClient = axios.create({ baseURL: '/api' })

// Attach access token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    // Ensure headers exists
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auto-refresh on 401 once, with queuing
let isRefreshing = false
let pending = []
let pendingRejects = []

function onRefreshed(newToken) {
  pending.forEach((cb) => {
    try { cb(newToken) } catch (_) {}
  })
  pending = []
  pendingRejects = []
}

function rejectAllPending(err) {
  pendingRejects.forEach((rej) => {
    try { rej(err) } catch (_) {}
  })
  pending = []
  pendingRejects = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { response, config } = error || {}
    // If no response or not 401, or already retried, just propagate
    if (!response || response.status !== 401 || config._retry) {
      return Promise.reject(error)
    }

    // Do not try to refresh for auth endpoints themselves
    const url = (config && config.url) || ''
    if (typeof url === 'string' && url.startsWith('/auth/')) {
      return Promise.reject(error)
    }

    // No refresh token -> logout
    const refreshToken = localStorage.getItem('refreshToken')
    if (!refreshToken) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      if (typeof window !== 'undefined') window.location.href = '/auth'
      return Promise.reject(error)
    }

    // Mark this request as a one-time retry
    config._retry = true

    if (isRefreshing) {
      // queue until refresh is done
      return new Promise((resolve, reject) => {
        pending.push((newToken) => {
          const headers = config.headers || {}
          headers.Authorization = `Bearer ${newToken}`
          config.headers = headers
          resolve(api(config))
        })
        pendingRejects.push(() => reject(error))
      })
    }

    try {
      isRefreshing = true
      // Use bare client to avoid interceptors on the refresh request
      const { data } = await refreshClient.post('/auth/refresh', null, {
        params: { refreshToken }
      })
      localStorage.setItem('accessToken', data.accessToken)
      localStorage.setItem('refreshToken', data.refreshToken)
      isRefreshing = false
      onRefreshed(data.accessToken)

      const headers = config.headers || {}
      headers.Authorization = `Bearer ${data.accessToken}`
      config.headers = headers
      return api(config)
    } catch (e) {
      isRefreshing = false
      rejectAllPending(e)
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      if (typeof window !== 'undefined') window.location.href = '/auth'
      return Promise.reject(error)
    }
  }
)

export default api
