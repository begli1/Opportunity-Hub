import { createRouter, createWebHistory } from 'vue-router'
import PreLogin from '@/components/Prelogin.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue' 
import Dashboard from '@/components/Dashboard.vue'
import MyPosts from '@/components/MyPosts.vue'
import Applications from '@/components/Applications.vue'
import Moderator from '@/components/Moderator.vue'
import AboutUs from '@/components/AboutUs.vue'
import References from '@/components/References.vue'
import { useAuth } from '@/lib/authStore'
import AxiosInstance from '@/apiClient'

const routes = [
  { path: '/', component: PreLogin },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { path: '/about', component: AboutUs },
  { path: '/references', component: References },
  { 
    path: '/dashboard', 
    component: Dashboard,
    meta: { requiresAuth: true } // Protected route
  },
  {
    path: '/my-posts',
    component: MyPosts,
    meta: { requiresAuth: true }
  },
  {
    path: '/applications',
    component: Applications,
    meta: { requiresAuth: true }
  },
  {
    path: '/moderation',
    component: Moderator,
    meta: { requiresAuth: true }
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard to protect routes

router.beforeEach(async (to) => {
  // protect moderation route
  if (to.path === '/moderation') {
    try {
      await AxiosInstance.get('/moderation/appeals')
      return true // ok, moderator
    } catch (e) {
      const status = e?.response?.status
      if (status === 401) return '/login'
      if (status === 403) return '/dashboard'
      return '/dashboard'
    }
  }

  return true
})

export default router