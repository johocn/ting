<template>
  <view class="container">
    <view class="header">
      <text class="title">Ting Learning Platform</text>
      <text class="subtitle">学习成长平台 - 移动端</text>
    </view>

    <view class="status-card">
      <text class="status-text">平台状态: 服务正常运行</text>
      <text class="status-text">API连接: 已连接</text>
    </view>

    <view class="features-grid">
      <view class="feature-card" @click="goToLearning">
        <text class="feature-icon">📚</text>
        <text class="feature-title">学习中心</text>
        <text class="feature-desc">观看学习内容，参与答题</text>
      </view>
      
      <view class="feature-card" @click="goToPoints">
        <text class="feature-icon">💎</text>
        <text class="feature-title">积分中心</text>
        <text class="feature-desc">查看和管理积分</text>
      </view>
      
      <view class="feature-card" @click="goToChannels">
        <text class="feature-icon">🔗</text>
        <text class="feature-title">渠道管理</text>
        <text class="feature-desc">管理推广渠道</text>
      </view>
      
      <view class="feature-card" @click="goToProfile">
        <text class="feature-icon">👤</text>
        <text class="feature-title">个人中心</text>
        <text class="feature-desc">个人信息管理</text>
      </view>
    </view>

    <view class="api-demo">
      <text class="demo-title">API连接测试</text>
      <button @click="testApiConnection" class="api-btn">测试API连接</button>
      <text v-if="apiResult" class="api-result">{{ apiResult }}</text>
    </view>
  </view>
</template>

<script>
import { ref } from 'vue';
import { API } from '../../utils/request';

export default {
  setup() {
    const apiResult = ref('');

    // 测试API连接
    const testApiConnection = async () => {
      try {
        apiResult.value = '正在连接API...';
        const response = await API.health();
        apiResult.value = 'API连接成功';
        console.log('Health check response:', response);
      } catch (error) {
        console.error('API连接失败:', error);
        apiResult.value = 'API连接失败: ' + (error.errMsg || error.message || '未知错误');
      }
    };

    return {
      apiResult,
      testApiConnection
    };
  },
  methods: {
    // 页面导航方法
    goToLearning() {
      uni.navigateTo({
        url: '/pages/learning/learning'
      });
    },
    goToPoints() {
      uni.navigateTo({
        url: '/pages/points/points'
      });
    },
    goToChannels() {
      uni.navigateTo({
        url: '/pages/channels/channels'
      });
    },
    goToProfile() {
      uni.navigateTo({
        url: '/pages/profile/profile'
      });
    }
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
  margin-bottom: 30px;
  padding: 20px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.subtitle {
  font-size: 16px;
  color: #666;
}

.status-card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.status-text {
  display: block;
  font-size: 14px;
  color: #409eff;
  margin-bottom: 5px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.feature-card {
  background: white;
  padding: 20px 15px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s ease;
}

.feature-card:active {
  transform: scale(0.95);
}

.feature-icon {
  font-size: 28px;
  display: block;
  margin-bottom: 10px;
}

.feature-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 5px;
}

.feature-desc {
  font-size: 12px;
  color: #999;
  display: block;
}

.api-demo {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.demo-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 15px;
}

.api-btn {
  background: #409eff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  font-size: 16px;
  margin-bottom: 15px;
  width: 100%;
}

.api-result {
  font-size: 14px;
  color: #666;
  word-break: break-all;
  line-height: 1.4;
}
</style>