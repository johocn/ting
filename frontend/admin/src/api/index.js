import axios from 'axios'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response?.status === 401) {
      // 未授权，跳转到登录页
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else {
      console.error('Response error:', error.response?.data?.message || 'Request failed')
    }
    return Promise.reject(error)
  }
)

export default service
