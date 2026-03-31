<template>
  <div class="login-container">
    <div class="login-form">
      <div class="logo">
        <h1>Ting Admin</h1>
        <p>视频音频学习赚积分平台</p>
      </div>
      
      <el-form 
        :model="loginForm" 
        :rules="loginRules" 
        ref="loginFormRef"
        class="login-form-content"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="loginForm.remember">记住密码</el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            @click="handleLogin" 
            :loading="loading"
            size="large"
            style="width: 100%;"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="other-options">
        <el-link type="primary">忘记密码？</el-link>
        <el-link type="primary">注册账号</el-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const loading = ref(false)
    const loginFormRef = ref(null)
    
    const loginForm = reactive({
      username: '',
      password: '',
      remember: false
    })
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
      ]
    }
    
    const handleLogin = async () => {
      if (!loginFormRef.value) return
      
      await loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 这里应该是真实的登录API调用
            // 为了演示，我们模拟登录成功
            const mockUser = {
              id: 1,
              username: loginForm.username,
              phone: '138****8888',
              integral: 1250,
              level: 3,
              is_member: true
            }
            const mockToken = 'mock-token-' + Date.now()
            
            // 模拟API延迟
            await new Promise(resolve => setTimeout(resolve, 1000))
            
            // 登录成功，保存用户信息和token
            store.dispatch('login', {
              user: mockUser,
              token: mockToken
            })
            
            ElMessage.success('登录成功')
            
            // 跳转到首页
            router.push('/dashboard')
          } catch (error) {
            ElMessage.error('登录失败: ' + (error.message || '网络错误'))
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    return {
      loading,
      loginFormRef,
      loginForm,
      loginRules,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-form {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 15px 35px rgba(50, 50, 93, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07);
}

.logo {
  text-align: center;
  margin-bottom: 30px;
}

.logo h1 {
  color: #303133;
  font-size: 24px;
  margin-bottom: 10px;
}

.logo p {
  color: #909399;
  font-size: 14px;
}

.login-form-content {
  margin-bottom: 20px;
}

.other-options {
  display: flex;
  justify-content: space-between;
}
</style>
