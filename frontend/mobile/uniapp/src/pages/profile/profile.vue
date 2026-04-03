<template>
  <view class="container">
    <view class="header">
      <text class="title">个人中心</text>
    </view>

    <!-- 用户信息卡片 -->
    <view class="user-card">
      <view class="avatar-section">
        <view class="avatar">
          <text class="avatar-text">{{ userInfo.username ? userInfo.username.charAt(0).toUpperCase() : 'U' }}</text>
        </view>
        <text class="username">{{ userInfo.username || '未登录用户' }}</text>
      </view>
      
      <view class="user-stats">
        <view class="stat-item">
          <text class="stat-value">{{ userInfo.integral || 0 }}</text>
          <text class="stat-label">积分</text>
        </view>
        <view class="stat-item">
          <text class="stat-value">Lv.{{ userInfo.level || 1 }}</text>
          <text class="stat-label">等级</text>
        </view>
        <view class="stat-item" :class="{ member: userInfo.is_member }">
          <text class="stat-value">{{ userInfo.is_member ? '会员' : '普通' }}</text>
          <text class="stat-label">身份</text>
        </view>
      </view>
    </view>

    <!-- 功能菜单 -->
    <view class="menu-section">
      <view class="menu-item" @click="goToProfileEdit">
        <text class="menu-icon">👤</text>
        <text class="menu-text">个人资料</text>
        <text class="arrow">›</text>
      </view>
      
      <view class="menu-item" @click="goToHistory">
        <text class="menu-icon">📜</text>
        <text class="menu-text">学习历史</text>
        <text class="arrow">›</text>
      </view>
      
      <view class="menu-item" @click="goToAbout">
        <text class="menu-icon">ℹ️</text>
        <text class="menu-text">关于我们</text>
        <text class="arrow">›</text>
      </view>
    </view>

    <!-- 退出登录按钮 -->
    <view class="logout-section">
      <button class="logout-btn" @click="logout">退出登录</button>
    </view>
  </view>
</template>

<script>
import { ref, onMounted } from 'vue';
import { API } from '../../utils/request';

export default {
  setup() {
    const userInfo = ref({});

    // 加载用户信息
    const loadUserInfo = async () => {
      try {
        const storedUser = uni.getStorageSync('user_info');
        if (storedUser) {
          userInfo.value = storedUser;
        } else {
          // 尝试从API获取用户信息
          const response = await API.user.getUserProfile();
          userInfo.value = response;
          // 保存到本地存储
          uni.setStorageSync('user_info', response);
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        // 检查是否有本地存储的用户信息
        try {
          const storedUser = uni.getStorageSync('user_info');
          if (storedUser) {
            userInfo.value = storedUser;
          }
        } catch (storageError) {
          console.error('获取本地用户信息失败:', storageError);
        }
      }
    };

    // 页面跳转方法
    const goToProfileEdit = () => {
      uni.navigateTo({
        url: '/pages/profile-edit/profile-edit'
      });
    };

    const goToHistory = () => {
      uni.navigateTo({
        url: '/pages/history/history'
      });
    };

    const goToAbout = () => {
      uni.showModal({
        title: '关于 Ting',
        content: 'Ting 学习平台 v1.0.0\n\n通过观看视频和音频学习内容，赚取积分，兑换奖励！',
        showCancel: false
      });
    };

    // 退出登录
    const logout = () => {
      uni.showModal({
        title: '确认退出',
        content: '确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            // 清除本地存储的用户信息和token
            uni.removeStorageSync('user_info');
            uni.removeStorageSync('access_token');
            
            // 跳转到登录页
            uni.reLaunch({
              url: '/pages/login/login'
            });
          }
        }
      });
    };

    onMounted(() => {
      loadUserInfo();
    });

    return {
      userInfo,
      loadUserInfo,
      goToProfileEdit,
      goToSecurity,
      goToHistory,
      goToSettings,
      logout
    };
  }
};
</script>

<style>
.container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.user-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.avatar-section {
  text-align: center;
  margin-bottom: 20px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
}

.avatar-text {
  font-size: 32px;
  color: white;
  font-weight: bold;
}

.username {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.stat-item {
  text-align: center;
}

.stat-item.member {
  color: #e6a23c;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #999;
}

.menu-section {
  background: white;
  border-radius: 15px;
  padding: 10px 0;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #f5f5f5;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-icon {
  font-size: 20px;
  margin-right: 15px;
  width: 24px;
}

.menu-text {
  flex: 1;
  font-size: 16px;
  color: #333;
}

.arrow {
  font-size: 18px;
  color: #ccc;
}

.logout-section {
  text-align: center;
}

.logout-btn {
  background: #f56c6c;
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 25px;
  font-size: 16px;
}
</style>