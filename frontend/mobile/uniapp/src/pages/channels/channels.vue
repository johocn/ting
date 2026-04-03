<template>
  <view class="container">
    <view class="header">
      <text class="title">渠道管理</text>
      <text class="subtitle">管理和查看您的推广渠道</text>
    </view>

    <!-- 渠道概览 -->
    <view class="channel-overview">
      <view class="overview-card">
        <view class="overview-item">
          <text class="item-label">我的渠道</text>
          <text class="item-value">{{ myChannels.length }}</text>
        </view>
        <view class="overview-item">
          <text class="item-label">注册用户</text>
          <text class="item-value">{{ totalRegistered }}</text>
        </view>
        <view class="overview-item">
          <text class="item-label">活跃用户</text>
          <text class="item-value">{{ totalActive }}</text>
        </view>
      </view>
    </view>

    <!-- 我的渠道列表 -->
    <view class="channels-section">
      <view class="section-header">
        <text class="section-title">我的渠道</text>
        <button class="add-btn" @click="createChannel">+ 新建</button>
      </view>
      
      <scroll-view class="channels-list" scroll-y="true">
        <view 
          v-for="channel in myChannels" 
          :key="channel.id" 
          class="channel-item"
          @click="viewChannelDetails(channel)"
        >
          <view class="channel-info">
            <text class="channel-name">{{ channel.name }}</text>
            <text class="channel-code">邀请码: {{ channel.code }}</text>
          </view>
          <view class="channel-stats">
            <text class="stat-item">注册: {{ channel.stats?.registered_users || 0 }}</text>
            <text class="stat-item">活跃: {{ channel.stats?.active_users || 0 }}</text>
          </view>
          <text class="arrow">›</text>
        </view>
        
        <view v-if="myChannels.length === 0" class="empty-state">
          <text class="empty-text">暂无渠道，点击右上角创建新渠道</text>
        </view>
      </scroll-view>
    </view>

    <!-- 邀请链接 -->
    <view class="invite-section" v-if="selectedChannel">
      <view class="section-header">
        <text class="section-title">邀请链接</text>
      </view>
      <view class="invite-content">
        <text class="invite-url">{{ selectedChannel.invite_link }}</text>
        <button class="copy-btn" @click="copyInviteLink">复制链接</button>
      </view>
    </view>
  </view>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { API } from '../../utils/request';

export default {
  setup() {
    const myChannels = ref([]);
    const selectedChannel = ref(null);
    const totalRegistered = ref(0);
    const totalActive = ref(0);

    // 加载我的渠道
    const loadMyChannels = async () => {
      try {
        const response = await API.channel.getMyChannels();
        myChannels.value = Array.isArray(response) ? response : [];
        
        // 计算总计
        totalRegistered.value = myChannels.value.reduce((sum, channel) => 
          sum + (channel.stats?.registered_users || 0), 0);
        totalActive.value = myChannels.value.reduce((sum, channel) => 
          sum + (channel.stats?.active_users || 0), 0);
      } catch (error) {
        console.error('获取渠道列表失败:', error);
        uni.showToast({
          title: '获取渠道列表失败',
          icon: 'error'
        });
      }
    };

    // 创建新渠道
    const createChannel = () => {
      uni.navigateTo({
        url: '/pages/channel-create/channel-create'
      });
    };

    // 查看渠道详情
    const viewChannelDetails = (channel) => {
      selectedChannel.value = channel;
      uni.setClipboardData({
        data: channel.invite_link,
        success: () => {
          uni.showToast({
            title: '链接已复制',
            icon: 'success'
          });
        }
      });
    };

    // 复制邀请链接
    const copyInviteLink = () => {
      if (selectedChannel.value) {
        uni.setClipboardData({
          data: selectedChannel.value.invite_link,
          success: () => {
            uni.showToast({
              title: '链接已复制',
              icon: 'success'
            });
          }
        });
      }
    };

    // 加载数据
    const loadData = async () => {
      await loadMyChannels();
    };

    onMounted(() => {
      loadData();
    });

    return {
      myChannels,
      selectedChannel,
      totalRegistered,
      totalActive,
      loadMyChannels,
      createChannel,
      viewChannelDetails,
      copyInviteLink
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

.channel-overview {
  margin-bottom: 20px;
}

.overview-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-around;
}

.overview-item {
  text-align: center;
}

.item-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.item-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.channels-section {
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

.add-btn {
  background: #409eff;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  font-size: 14px;
}

.channels-list {
  max-height: 300px;
}

.channel-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.channel-item:last-child {
  border-bottom: none;
}

.channel-info {
  flex: 1;
}

.channel-name {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.channel-code {
  display: block;
  font-size: 12px;
  color: #999;
}

.channel-stats {
  width: 100px;
  text-align: right;
}

.stat-item {
  display: block;
  font-size: 12px;
  color: #666;
  margin-bottom: 3px;
}

.arrow {
  font-size: 18px;
  color: #ccc;
  margin-left: 10px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.empty-text {
  color: #999;
  font-size: 14px;
}

.invite-section {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.invite-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.invite-url {
  flex: 1;
  font-size: 12px;
  color: #409eff;
  word-break: break-all;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
  max-height: 60px;
  overflow-y: auto;
}

.copy-btn {
  background: #67c23a;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  font-size: 14px;
  white-space: nowrap;
}
</style>