<template>
  <view class="container">
    <view class="header">
      <text class="title">学习历史</text>
      <text class="subtitle">查看您的学习记录</text>
    </view>

    <!-- 学习统计 -->
    <view class="stats-card">
      <view class="stat-item">
        <text class="stat-value">{{ totalSessions }}</text>
        <text class="stat-label">学习会话</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ totalDuration }}</text>
        <text class="stat-label">总时长(分钟)</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ completedCount }}</text>
        <text class="stat-label">已完成</text>
      </view>
    </view>

    <!-- 学习记录列表 -->
    <view class="history-section">
      <view class="section-header">
        <text class="section-title">学习记录</text>
        <text class="refresh-icon" @click="refreshHistory">🔄</text>
      </view>
      
      <scroll-view class="history-list" scroll-y="true">
        <view 
          v-for="session in learningSessions" 
          :key="session.session_id" 
          class="session-item"
        >
          <view class="session-info">
            <text class="content-title">{{ session.content.title }}</text>
            <view class="session-meta">
              <text class="session-status" :class="session.status">{{ session.status }}</text>
              <text class="session-date">{{ formatDate(session.start_time) }}</text>
            </view>
          </view>
          
          <view class="session-progress">
            <text class="duration">{{ formatDuration(session.watched_duration) }} / {{ formatDuration(session.total_duration) }}</text>
            <view class="progress-bar-container">
              <view 
                class="progress-bar-fill" 
                :style="{ width: session.progress_percentage + '%' }"
              ></view>
            </view>
            <text class="progress-text">{{ session.progress_percentage }}%</text>
          </view>
        </view>
        
        <view v-if="learningSessions.length === 0" class="empty-state">
          <text class="empty-text">暂无学习记录</text>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script>
import { ref, onMounted } from 'vue';
import { API } from '../../utils/request';

export default {
  setup() {
    const learningSessions = ref([]);
    const totalSessions = ref(0);
    const totalDuration = ref(0);
    const completedCount = ref(0);

    // 加载学习历史
    const loadLearningHistory = async () => {
      try {
        const response = await API.learning.getUserProgress();
        learningSessions.value = Array.isArray(response) ? response : [];
        
        // 计算统计数据
        totalSessions.value = learningSessions.value.length;
        totalDuration.value = Math.floor(learningSessions.value.reduce((sum, session) => 
          sum + (session.watched_duration || 0), 0) / 60); // 转换为分钟
        completedCount.value = learningSessions.value.filter(session => 
          session.status === 'completed').length;
      } catch (error) {
        console.error('获取学习历史失败:', error);
        uni.showToast({
          title: '获取学习历史失败',
          icon: 'error'
        });
      }
    };

    // 刷新历史记录
    const refreshHistory = async () => {
      await loadLearningHistory();
      uni.showToast({
        title: '刷新成功',
        icon: 'success'
      });
    };

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return `${date.getMonth()+1}-${date.getDate()}`;
    };

    // 格式化时长
    const formatDuration = (seconds) => {
      if (!seconds) return '00:00';
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    // 加载数据
    onMounted(() => {
      loadLearningHistory();
    });

    return {
      learningSessions,
      totalSessions,
      totalDuration,
      completedCount,
      loadLearningHistory,
      refreshHistory,
      formatDate,
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

.stats-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #999;
}

.history-section {
  background: white;
  border-radius: 15px;
  padding: 20px;
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

.history-list {
  max-height: 400px;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.session-item:last-child {
  border-bottom: none;
}

.session-info {
  flex: 1;
}

.content-title {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.session-meta {
  display: flex;
  justify-content: space-between;
}

.session-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
}

.session-status.completed {
  color: #67c23a;
  background: #f0f9eb;
}

.session-status.in_progress {
  color: #e6a23c;
  background: #fdf6ec;
}

.session-date {
  font-size: 12px;
  color: #999;
}

.session-progress {
  width: 120px;
  text-align: right;
}

.duration {
  display: block;
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

.progress-bar-container {
  width: 100%;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #66b1ff);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.progress-text {
  display: block;
  font-size: 10px;
  color: #999;
  text-align: right;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.empty-text {
  color: #999;
  font-size: 16px;
}
</style>