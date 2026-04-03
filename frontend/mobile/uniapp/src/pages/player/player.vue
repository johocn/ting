<template>
  <view class="player-container">
    <view class="video-wrapper">
      <!-- 视频播放器 -->
      <video 
        id="learningVideo"
        :src="content.url"
        :controls="true"
        :enable-play-gesture="true"
        :show-center-play-btn="true"
        @play="onPlay"
        @pause="onPause"
        @ended="onEnded"
        @timeupdate="onTimeUpdate"
        @loadedmetadata="onLoadedMetadata"
        class="video-player"
      ></video>
    </view>

    <view class="content-info">
      <text class="content-title">{{ content.title }}</text>
      <view class="content-meta">
        <text class="content-category">{{ content.category }}</text>
        <text class="content-points">积分: {{ content.reward_points_per_minute }}/分钟</text>
      </view>
    </view>

    <view class="progress-info">
      <view class="progress-row">
        <text class="progress-label">已学习:</text>
        <text class="progress-value">{{ formatDuration(watchedDuration) }}</text>
      </view>
      <view class="progress-row">
        <text class="progress-label">总时长:</text>
        <text class="progress-value">{{ formatDuration(totalDuration) }}</text>
      </view>
      <view class="progress-row">
        <text class="progress-label">进度:</text>
        <text class="progress-value">{{ progressPercentage }}%</text>
      </view>
    </view>

    <view class="progress-bar-container">
      <view 
        class="progress-bar-fill" 
        :style="{ width: progressPercentage + '%' }"
      ></view>
    </view>

    <view class="controls">
      <button 
        class="complete-btn" 
        @click="completeLearning"
        :disabled="progressPercentage < 100"
      >
        {{ progressPercentage < 100 ? '完成学习 (' + (100 - progressPercentage) + '% remaining)' : '完成学习' }}
      </button>
    </view>

    <view class="tips">
      <text class="tip-text">💡 提示: 完成学习后将获得 {{ calculatedPoints }} 积分</text>
    </view>
  </view>
</template>

<script>
import { ref, onLoad, onUnload, onShow, onHide } from 'vue';
import { API } from '../../utils/request';

export default {
  setup() {
    // 页面参数
    const sessionId = ref('');
    const contentId = ref('');
    
    // 内容信息
    const content = ref({});
    
    // 播放状态
    const watchedDuration = ref(0);
    const totalDuration = ref(0);
    const progressPercentage = ref(0);
    const calculatedPoints = ref(0);
    const isPlaying = ref(false);
    
    // 定时器ID
    const updateTimer = ref(null);
    
    // 页面加载
    const onLoadHandler = (options) => {
      sessionId.value = options.sessionId;
      contentId.value = options.contentId;
      
      loadContentDetails();
      startTrackingProgress();
    };
    
    // 页面卸载
    const onUnloadHandler = () => {
      if (updateTimer.value) {
        clearInterval(updateTimer.value);
      }
      // 如果用户离开页面但未完成学习，尝试保存进度
      if (watchedDuration.value > 0 && progressPercentage.value < 100) {
        updateLearningProgress();
      }
    };
    
    // 加载内容详情
    const loadContentDetails = async () => {
      try {
        uni.showLoading({
          title: '加载中...'
        });
        
        const response = await API.content.get(contentId.value);
        content.value = response;
        totalDuration.value = response.duration || 0;
        
        uni.hideLoading();
      } catch (error) {
        console.error('加载内容详情失败:', error);
        uni.hideLoading();
        uni.showToast({
          title: '加载失败',
          icon: 'error'
        });
      }
    };
    
    // 开始跟踪进度
    const startTrackingProgress = () => {
      // 每10秒更新一次进度
      updateTimer.value = setInterval(async () => {
        if (isPlaying.value && watchedDuration.value > 0) {
          await updateLearningProgress();
        }
      }, 10000); // 10秒更新一次
    };
    
    // 更新学习进度
    const updateLearningProgress = async () => {
      if (!sessionId.value || watchedDuration.value <= 0) return;
      
      try {
        await API.learning.updateProgress(sessionId.value, watchedDuration.value);
        
        // 计算积分
        calculatePoints();
      } catch (error) {
        console.error('更新学习进度失败:', error);
      }
    };
    
    // 完成学习
    const completeLearning = async () => {
      if (!sessionId.value) {
        uni.showToast({
          title: '无效的学习会话',
          icon: 'error'
        });
        return;
      }
      
      try {
        uni.showLoading({
          title: '完成学习...'
        });
        
        const response = await API.learning.completeLearning(sessionId.value);
        
        uni.hideLoading();
        
        // 更新本地存储中的会话状态
        try {
          const session = uni.getStorageSync('current_learning_session');
          if (session && session.session_id === sessionId.value) {
            session.status = 'completed';
            uni.setStorageSync('current_learning_session', session);
          }
        } catch (storageError) {
          console.error('更新本地存储失败:', storageError);
        }
        
        // 更新用户积分
        try {
          const userInfo = uni.getStorageSync('user_info');
          if (userInfo) {
            userInfo.integral = userInfo.integral || 0;
            userInfo.integral += response.points_earned;
            uni.setStorageSync('user_info', userInfo);
          }
        } catch (userStorageError) {
          console.error('更新用户积分失败:', userStorageError);
        }
        
        uni.showToast({
          title: `学习完成！获得${response.points_earned}积分`,
          icon: 'success',
          duration: 2000
        });
        
        // 延迟返回，让用户看到成功提示
        setTimeout(() => {
          uni.navigateBack();
        }, 2000);
      } catch (error) {
        console.error('完成学习失败:', error);
        uni.hideLoading();
        uni.showToast({
          title: '完成学习失败',
          icon: 'error'
        });
      }
    };
    
    // 计算预计积分
    const calculatePoints = () => {
      if (totalDuration.value > 0 && content.value.reward_points_per_minute) {
        const minutesWatched = watchedDuration.value / 60;
        const estimatedPoints = Math.floor(minutesWatched * content.value.reward_points_per_minute);
        calculatedPoints.value = estimatedPoints;
      }
    };
    
    // 事件处理器
    const onPlay = () => {
      isPlaying.value = true;
    };
    
    const onPause = () => {
      isPlaying.value = false;
      // 暂停时也更新进度
      updateLearningProgress();
    };
    
    const onEnded = async () => {
      // 视频播放完毕，更新进度到总时长
      watchedDuration.value = totalDuration.value;
      progressPercentage.value = 100;
      calculatePoints();
      
      // 更新进度
      await updateLearningProgress();
    };
    
    const onTimeUpdate = (e) => {
      // 更新已观看时长
      watchedDuration.value = Math.floor(e.detail.currentTime);
      
      // 更新进度百分比
      if (totalDuration.value > 0) {
        progressPercentage.value = Math.floor((watchedDuration.value / totalDuration.value) * 100);
      }
      
      // 计算积分
      calculatePoints();
    };
    
    const onLoadedMetadata = (e) => {
      totalDuration.value = Math.floor(e.detail.duration);
    };
    
    // 格式化时长
    const formatDuration = (seconds) => {
      if (!seconds) return '00:00';
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };
    
    // 在setup中注册生命周期钩子
    onLoad(onLoadHandler);
    onUnload(onUnloadHandler);
    
    return {
      sessionId,
      contentId,
      content,
      watchedDuration,
      totalDuration,
      progressPercentage,
      calculatedPoints,
      onLoadHandler,
      onUnloadHandler,
      loadContentDetails,
      updateLearningProgress,
      completeLearning,
      calculatePoints,
      onPlay,
      onPause,
      onEnded,
      onTimeUpdate,
      onLoadedMetadata,
      formatDuration
    };
  }
};
</script>

<style>
.player-container {
  background: #000;
  min-height: 100vh;
  padding-bottom: 20px;
}

.video-wrapper {
  width: 100%;
  height: 40vh;
  position: relative;
}

.video-player {
  width: 100%;
  height: 100%;
}

.content-info {
  padding: 20px;
  background: white;
  margin-top: 10px;
}

.content-title {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.content-meta {
  display: flex;
  justify-content: space-between;
}

.content-category {
  font-size: 12px;
  color: #409eff;
  background: #ecf5ff;
  padding: 2px 8px;
  border-radius: 10px;
}

.content-points {
  font-size: 12px;
  color: #67c23a;
  background: #f0f9eb;
  padding: 2px 8px;
  border-radius: 10px;
}

.progress-info {
  background: white;
  padding: 20px;
  margin: 10px 0;
}

.progress-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.progress-row:last-child {
  margin-bottom: 0;
}

.progress-label {
  font-size: 14px;
  color: #666;
}

.progress-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.progress-bar-container {
  width: 90%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  margin: 15px auto;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #66b1ff);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.controls {
  padding: 0 20px;
}

.complete-btn {
  width: 100%;
  background: #409eff;
  color: white;
  border: none;
  padding: 15px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
}

.complete-btn:disabled {
  background: #c0c4cc;
}

.tips {
  padding: 0 20px;
  margin-top: 15px;
}

.tip-text {
  font-size: 12px;
  color: #999;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
  display: block;
}
</style>