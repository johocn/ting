<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="sidebarWidth" class="sidebar">
      <div class="logo">
        <h2>Ting Admin</h2>
      </div>
      <el-menu
        :default-active="$route.path"
        :collapse="sidebarCollapsed"
        :unique-opened="true"
        :router="true"
        class="menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><House /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/contents">
          <el-icon><VideoPlay /></el-icon>
          <span>内容管理</span>
        </el-menu-item>
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/points">
          <el-icon><Coin /></el-icon>
          <span>积分管理</span>
        </el-menu-item>
        <el-menu-item index="/channels">
          <el-icon><Connection /></el-icon>
          <span>渠道管理</span>
        </el-menu-item>
        <el-menu-item index="/mall">
          <el-icon><ShoppingCart /></el-icon>
          <span>商城管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区域 -->
    <el-container>
      <!-- 顶部导航 -->
      <el-header class="header">
        <div class="header-left">
          <el-icon class="collapse-icon" @click="toggleSidebar">
            <component :is="sidebarCollapsed ? 'Expand' : 'Fold'" />
          </el-icon>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="el-dropdown-link">
              {{ userInfo.username || 'Admin' }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="goToProfile">个人资料</el-dropdown-item>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 页面内容 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { 
  House, VideoPlay, User, Coin, 
  Connection, ShoppingCart, ArrowDown, 
  Fold, Expand 
} from '@element-plus/icons-vue'

export default {
  name: 'Layout',
  components: {
    House, VideoPlay, User, Coin,
    Connection, ShoppingCart, ArrowDown,
    Fold, Expand
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const sidebarCollapsed = computed(() => store.state.sidebarCollapsed)
    const sidebarWidth = computed(() => sidebarCollapsed.value ? '64px' : '200px')
    const userInfo = computed(() => store.state.user || {})
    
    const toggleSidebar = () => {
      store.dispatch('toggleSidebar')
    }
    
    const logout = () => {
      store.dispatch('logout')
      router.push('/login')
    }
    
    const goToProfile = () => {
      // 跳转到个人资料页
      router.push('/profile')
    }
    
    onMounted(() => {
      // 检查登录状态
      if (!store.state.token) {
        router.push('/login')
      }
    })
    
    return {
      sidebarCollapsed,
      sidebarWidth,
      userInfo,
      toggleSidebar,
      logout,
      goToProfile
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  color: #bfcbd9;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b3a4d;
}

.logo h2 {
  color: white;
  margin: 0;
  font-size: 18px;
}

.menu:not(.el-menu--collapse) {
  width: 200px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.collapse-icon {
  cursor: pointer;
  font-size: 18px;
  margin-right: 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
