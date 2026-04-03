<template>
  <view class="container">
    <view class="header">
      <text class="title">积分中心</text>
      <text class="subtitle">查看和管理您的积分</text>
    </view>

    <!-- 积分概览 -->
    <view class="points-overview">
      <view class="points-card">
        <text class="card-title">当前积分</text>
        <text class="points-total">{{ userPoints.total_points || 0 }}</text>
        <view class="points-breakdown">
          <view class="breakdown-item">
            <text class="item-label">可用积分</text>
            <text class="item-value">{{ userPoints.available_points || 0 }}</text>
          </view>
          <view class="breakdown-item">
            <text class="item-label">冻结积分</text>
            <text class="item-value">{{ userPoints.frozen_points || 0 }}</text>
          </view>
          <view class="breakdown-item">
            <text class="item-label">已过期积分</text>
            <text class="item-value">{{ userPoints.expired_points || 0 }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 积分流水 -->
    <view class="transactions-section">
      <view class="section-header">
        <text class="section-title">积分流水</text>
        <text class="refresh-icon" @click="refreshTransactions">🔄</text>
      </view>
      
      <scroll-view class="transactions-list" scroll-y="true" :style="{ height: windowHeight - 400 + 'px' }">
        <view 
          v-for="(transaction, index) in transactions" 
          :key="index" 
          class="transaction-item"
        >
          <view class="transaction-info">
            <text class="transaction-type" :class="transaction.transaction_type === 'earn' ? 'earn' : 'spend'">
              {{ transaction.transaction_type === 'earn' ? '+' : '-' }}{{ Math.abs(transaction.points_change) }}
            </text>
            <text class="transaction-description">{{ transaction.description }}</text>
          </view>
          <view class="transaction-meta">
            <text class="transaction-time">{{ formatDate(transaction.created_at) }}</text>
            <text class="transaction-operation">{{ getOperationText(transaction.operation_type) }}</text>
          </view>
        </view>
        
        <view v-if="transactions.length === 0" class="empty-state">
          <text class="empty-text">暂无积分记录</text>
        </view>
      </scroll-view>
    </view>

    <!-- 快捷操作 -->
    <view class="quick-actions">
      <button class="action-btn" @click="goToMall">积分商城</button>
      <button class="action-btn secondary" @click="goToCheckin">每日签到</button>
    </view>
  </view>
</template>

<script>
import { ref, onMounted } from 'vue';
import { API } from '../../utils/request';

export default {
  setup() {
    const userPoints = ref({});
    const transactions = ref([]);
    const windowHeight = ref(uni.getSystemInfoSync().windowHeight);

    // 加载用户积分信息
    const loadUserPoints = async () => {
      try {
        const response = await API.points.getUserAccount();
        userPoints.value = response;
      } catch (error) {
        console.error('获取积分信息失败:', error);
        uni.showToast({
          title: '获取积分信息失败',
          icon: 'error'
        });
      }
    };

    // 加载积分流水
    const loadTransactions = async () => {
      try {
        const response = await API.points.getTransactions({ skip: 0, limit: 50 });
        transactions.value = Array.isArray(response) ? response : [];
      } catch (error) {
        console.error('获取积分流水失败:', error);
        uni.showToast({
          title: '获取积分流水失败',
          icon: 'error'
        });
      }
    };

    // 刷新积分流水
    const refreshTransactions = async () => {
      await loadTransactions();
      uni.showToast({
        title: '刷新成功',
        icon: 'success'
      });
    };

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return `${date.getMonth()+1}-${date.getDate()} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    };

    // 获取操作类型文本
    const getOperationText = (operationType) => {
      const map = {
        'watch_content': '观看内容',
        'answer_quiz': '答题奖励',
        'daily_checkin': '每日签到',
        'exchange_item': '兑换商品',
        'purchase': '购买',
        'refund': '退款',
        'referral': '推荐奖励'
      };
      return map[operationType] || operationType;
    };

    // 快捷操作
    const goToMall = () => {
      uni.showToast({
        title: '积分商城功能开发中',
        icon: 'none'
      });
    };

    const goToCheckin = () => {
      uni.showToast({
        title: '每日签到功能开发中',
        icon: 'none'
      });
    };

    // 加载数据
    const loadData = async () => {
      await Promise.all([
        loadUserPoints(),
        loadTransactions()
      ]);
    };

    onMounted(() => {
      loadData();
    });

    return {
      userPoints,
      transactions,
      windowHeight,
      loadUserPoints,
      loadTransactions,
      refreshTransactions,
      formatDate,
      getOperationText,
      goToMall,
      goToCheckin
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

.points-overview {
  margin-bottom: 20px;
}

.points-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  text-align: center;
}

.card-title {
  display: block;
  font-size: 16px;
  color: #666;
  margin-bottom: 10px;
}

.points-total {
  display: block;
  font-size: 48px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 20px;
}

.points-breakdown {
  display: flex;
  justify-content: space-around;
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.breakdown-item {
  text-align: center;
}

.item-label {
  display: block;
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

.item-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.transactions-section {
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

.transactions-list {
  max-height: 300px;
}

.transaction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.transaction-item:last-child {
  border-bottom: none;
}

.transaction-info {
  flex: 1;
}

.transaction-type {
  display: block;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.transaction-type.earn {
  color: #67c23a;
}

.transaction-type.spend {
  color: #f56c6c;
}

.transaction-description {
  display: block;
  font-size: 14px;
  color: #666;
}

.transaction-meta {
  text-align: right;
  width: 120px;
}

.transaction-time {
  display: block;
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

.transaction-operation {
  display: block;
  font-size: 12px;
  color: #409eff;
  background: #ecf5ff;
  padding: 2px 6px;
  border-radius: 10px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.empty-text {
  color: #999;
  font-size: 16px;
}

.quick-actions {
  display: flex;
  gap: 15px;
}

.action-btn {
  flex: 1;
  background: #409eff;
  color: white;
  border: none;
  padding: 15px;
  border-radius: 8px;
  font-size: 16px;
}

.action-btn.secondary {
  background: #909399;
}
</style>