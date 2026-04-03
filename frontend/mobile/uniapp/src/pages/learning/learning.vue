<template>
  <view class="container">
    <view class="header">
      <text class="title">学习中心</text>
      <text class="subtitle">观看视频/音频内容，赚取积分</text>
    </view>

    <!-- 积分信息卡片 -->
    <view class="points-card">
      <view class="points-info">
        <text class="points-label">当前积分</text>
        <text class="points-value">{{ userInfo.integral || 0 }}</text>
      </view>
      <view class="points-info">
        <text class="points-label">等级</text>
        <text class="points-value">Lv.{{ userInfo.level || 1 }}</text>
      </view>
    </view>

    <!-- 学习内容列表 -->
    <view class="content-section">
      <view class="section-header">
        <text class="section-title">学习内容</text>
        <text class="refresh-icon" @click="refreshContents">🔄</text>
      </view>
      
      <scroll-view class="content-list" scroll-y="true">
        <view 
          v-for="content in contents" 
          :key="content.id" 
          class="content-item"
          @click="startLearning(content)"
        >
          <view class="content-info">
            <text class="content-title">{{ content.title }}</text>
            <text class="content-duration">{{ formatDuration(content.duration) }}</text>
            <text class="content-category">{{ content.category }}</text>
            <text class="content-points">积分: {{ content.reward_points_per_minute }}/分钟</text>
          </view>
          <text class="arrow">›</text>
        </view>
      </scroll-view>
    </view>

    <!-- 当前学习进度 -->
    <view v-if="currentSession" class="progress-section">
      <view class="section-header">
        <text class="section-title">当前学习进度</text>
      </view>
      
      <view class="session-card">
        <text class="session-title">{{ currentSession.content.title }}</text>
        <text class="session-duration">{{ formatDuration(currentSession.watched_duration) }} / {{ formatDuration(currentSession.total_duration) }}</text>
        
        <view class="progress-bar-container">
          <view 
            class="progress-bar-fill" 
            :style="{ width: currentSession.progress_percentage + '%' }"
          ></view>
        </view>
        <text class="progress-text">{{ currentSession.progress_percentage }}%</text>
        
        <button 
          class="continue-btn" 
          @click="continueLearning"
          :disabled="currentSession.status === 'completed'"
        >
          {{ currentSession.status === 'completed' ? '已完成' : '继续学习' }}
        </button>
      </view>
    </view>
  </view>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { API } from '../../utils/request';

export default {
  setup() {
    // 用户信息
    const userInfo = ref({});
    
    // 内容列表
    const contents = ref([]);
    
    // 当前学习会话
    const currentSession = ref(null);
    
    // 从本地存储获取用户信息
    const loadUserInfo = async () => {
      try {
        const storedUser = uni.getStorageSync('user_info');
        if (storedUser) {
          userInfo.value = storedUser;
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    };
    
    // 获取内容列表
    const loadContents = async () => {
      try {
        const response = await API.content.list();
        contents.value = response.data || [];
      } catch (error) {
        console.error('获取内容列表失败:', error);
        uni.showToast({
          title: '获取内容失败',
          icon: 'error'
        });
      }
    };
    
    // 刷新内容列表
    const refreshContents = async () => {
      await loadContents();
      uni.showToast({
        title: '刷新成功',
        icon: 'success'
      });
    };
    
    // 开始学习
    const startLearning = async (content) => {
      try {
        uni.showLoading({
          title: '开始学习...'
        });
        
        const response = await API.learning.startLearning(content.id);
        currentSession.value = {
          session_id: response.session_id,
          content: content,
          watched_duration: 0,
          total_duration: content.duration,
          progress_percentage: 0,
          status: 'in_progress'
        };
        
        // 保存当前会话到本地存储
        uni.setStorageSync('current_learning_session', currentSession.value);
        
        uni.hideLoading();
        uni.showToast({
          title: '学习已开始',
          icon: 'success'
        });
        
        // 跳转到学习播放页面
        uni.navigateTo({
          url: `/pages/player/player?sessionId=${response.session_id}&contentId=${content.id}`
        });
      } catch (error) {
        console.error('开始学习失败:', error);
        uni.hideLoading();
        uni.showToast({
          title: '开始学习失败',
          icon: 'error'
        });
      }
    };
    
    // 继续学习
    const continueLearning = async () => {
      if (currentSession.value && currentSession.value.session_id) {
        uni.navigateTo({
          url: `/pages/player/player?sessionId=${currentSession.value.session_id}&contentId=${currentSession.value.content.id}`
        });
      }
    };
    
    // 格式化时长
    const formatDuration = (seconds) => {
      if (!seconds) return '00:00';
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };
    
    // 加载数据
    const loadData = async () => {
      await Promise.all([
        loadUserInfo(),
        loadContents()
      ]);
      
      // 检查是否有当前学习会话
      try {
        const session = uni.getStorageSync('current_learning_session');
        if (session && session.status !== 'completed') {
          currentSession.value = session;
        }
      } catch (error) {
        console.log('没有当前学习会话');
      }
    };
    
    onMounted(() => {
      loadData();
    });
    
    return {
      userInfo,
      contents,
      currentSession,
      loadContents,
      refreshContents,
      startLearning,
      continueLearning,
      formatDuration
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
  display: block;
  margin-bottom: 5px;
}

.subtitle {
  font-size: 14px;
  color: #666;
  display: block;
}

.points-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-around;
}

.points-info {
  text-align: center;
}

.points-label {
  display: block;
  font-size: 14px;
  color: #999;
  margin-bottom: 5px;
}

.points-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.content-section {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.refresh-icon {
  font-size: 18px;
  color: #409eff;
  padding: 5px;
}

.content-list {
  max-height: 300px;
}

.content-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.content-item:last-child {
  border-bottom: none;
}

.content-info {
  flex: 1;
}

.content-title {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.content-duration {
  display: block;
  font-size: 12px;
  color: #999;
  margin-bottom: 3px;
}

.content-category {
  display: inline-block;
  font-size: 12px;
  color: #409eff;
  background: #ecf5ff;
  padding: 2px 8px;
  border-radius: 10px;
  margin-right: 10px;
}

.content-points {
  display: inline-block;
  font-size: 12px;
  color: #67c23a;
  background: #f0f9eb;
  padding: 2px 8px;
  border-radius: 10px;
}

.arrow {
  font-size: 18px;
  color: #ccc;
}

.progress-section {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.session-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 15px;
}

.session-title {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.session-duration {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
}

.progress-bar-container {
  width: 100%;
  height: 10px;
  background: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #66b1ff);
  border-radius: 5px;
  transition: width 0.3s ease;
}

.progress-text {
  display: block;
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-bottom: 15px;
}

.continue-btn {
  width: 100%;
  background: #409eff;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 5px;
  font-size: 16px;
}

.continue-btn:disabled {
  background: #c0c4cc;
}
</style>