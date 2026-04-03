<!-- @ts-nocheck -->
<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";

onLaunch(() => {
  console.log("App Launch - Ting 学习平台");
  // 检查登录状态
  const token = uni.getStorageSync('access_token');
  if (!token) {
    // 未登录，跳转到登录页
    // uni.reLaunch({
    //   url: '/pages/login/login'
    // });
  }
});

onShow(() => {
  console.log("App Show");
  // 页面显示时刷新用户信息
});

onHide(() => {
  console.log("App Hide");
});
</script>

<template>
  <view class="uni-body">
    <slot />
  </view>
</template>

<style>
/* 全局样式 */
page {
  background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.uni-body {
  min-height: 100vh;
}

/* 通用按钮样式 */
.btn-primary {
  background: linear-gradient(45deg, #409eff, #66b1ff);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 16px;
}

.btn-success {
  background: linear-gradient(45deg, #67c23a, #85ce61);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 16px;
}

/* 通用卡片样式 */
.card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 15px;
}
</style>
