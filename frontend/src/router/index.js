import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'
import { getAuthToken } from '../services/auth'
import TemplatesView from '../views/TemplatesView.vue'
import TemplateView from '../views/TemplateView.vue'
import MainLayout from '../components/layouts/MainLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: AuthView
    },
    {
      path: '/auth/callback',
      name: 'auth-callback',
      component: () => import('../views/AuthCallbackView.vue')
    },
    // Routes that use MainLayout
    {
      path: '/app',
      component: MainLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '/templates',
          name: 'templates',
          component: TemplatesView,
          meta: { requiresAuth: true }
        },
        {
          path: '/templates/:id',
          name: 'template',
          component: TemplateView,
          meta: { requiresAuth: true }
        },
        {
          path: '/api-keys',
          name: 'api-keys',
          component: () => import('../views/APIKeysView.vue'),
          meta: { requiresAuth: true }
        }
      ]
    }
  ],
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = getAuthToken()

  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/templates')
  } else {
    next()
  }
})


export default router
