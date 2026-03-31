import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/Layout.vue'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import ContentManagement from '@/views/ContentManagement.vue'
import UserManagement from '@/views/UserManagement.vue'
import PointsManagement from '@/views/PointsManagement.vue'
import ChannelManagement from '@/views/ChannelManagement.vue'
import MallManagement from '@/views/MallManagement.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '仪表盘' }
      },
      {
        path: 'contents',
        name: 'ContentManagement',
        component: ContentManagement,
        meta: { title: '内容管理' }
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement,
        meta: { title: '用户管理' }
      },
      {
        path: 'points',
        name: 'PointsManagement',
        component: PointsManagement,
        meta: { title: '积分管理' }
      },
      {
        path: 'channels',
        name: 'ChannelManagement',
        component: ChannelManagement,
        meta: { title: '渠道管理' }
      },
      {
        path: 'mall',
        name: 'MallManagement',
        component: MallManagement,
        meta: { title: '商城管理' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
