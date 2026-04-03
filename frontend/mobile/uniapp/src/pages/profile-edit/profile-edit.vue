<template>
  <view class="container">
    <view class="header">
      <text class="title">编辑个人资料</text>
    </view>

    <view class="form-container">
      <view class="input-group">
        <text class="input-label">用户名</text>
        <input 
          class="input-field" 
          type="text" 
          placeholder="请输入用户名" 
          v-model="formData.username"
          @input="onUsernameInput"
        />
      </view>

      <view class="input-group">
        <text class="input-label">手机号</text>
        <input 
          class="input-field" 
          type="text" 
          placeholder="请输入手机号" 
          v-model="formData.phone"
          @input="onPhoneInput"
        />
      </view>

      <view class="input-group">
        <text class="input-label">邮箱</text>
        <input 
          class="input-field" 
          type="text" 
          placeholder="请输入邮箱" 
          v-model="formData.email"
          @input="onEmailInput"
        />
      </view>

      <button 
        class="save-btn" 
        :disabled="!isValid || isSubmitting"
        @click="handleSave"
      >
        {{ isSubmitting ? '保存中...' : '保存' }}
      </button>

      <view v-if="errorMessage" class="error-message">
        <text>{{ errorMessage }}</text>
      </view>

      <view v-if="successMessage" class="success-message">
        <text>{{ successMessage }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { API } from '../../utils/request';

export default {
  name: 'ProfileEditPage',
  setup() {
    // 表单数据
    const formData = reactive({
      username: '',
      phone: '',
      email: ''
    });

    // 状态管理
    const isSubmitting = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');

    // 从用户信息加载数据
    const loadUserProfile = async () => {
      try {
        const response = await API.user.getUserProfile();
        formData.username = response.username || '';
        formData.phone = response.phone || '';
        formData.email = response.email || '';
      } catch (error) {
        console.error('获取用户资料失败:', error);
        errorMessage.value = '获取用户资料失败';
      }
    };

    // 验证函数
    const isValid = computed(() => {
      return (
        formData.username.trim() !== ''
      );
    });

    // 输入处理函数
    const onUsernameInput = (e) => {
      formData.username = e.detail.value;
      if (errorMessage.value.includes('用户名')) {
        errorMessage.value = '';
      }
    };

    const onPhoneInput = (e) => {
      formData.phone = e.detail.value;
      if (errorMessage.value.includes('手机号')) {
        errorMessage.value = '';
      }
    };

    const onEmailInput = (e) => {
      formData.email = e.detail.value;
      if (errorMessage.value.includes('邮箱')) {
        errorMessage.value = '';
      }
    };

    // 保存处理函数
    const handleSave = async () => {
      if (!isValid.value) {
        errorMessage.value = '请填写完整的资料信息';
        return;
      }

      isSubmitting.value = true;
      errorMessage.value = '';
      successMessage.value = '';

      try {
        const updateData = {
          username: formData.username,
          phone: formData.phone,
          email: formData.email
        };

        const response = await API.user.updateUserProfile(updateData);
        
        successMessage.value = '资料更新成功！';
        
        // 更新本地存储的用户信息
        try {
          const storedUser = uni.getStorageSync('user_info');
          if (storedUser) {
            Object.assign(storedUser, {
              username: formData.username,
              phone: formData.phone,
              email: formData.email
            });
            uni.setStorageSync('user_info', storedUser);
          }
        } catch (storageError) {
          console.error('更新本地存储失败:', storageError);
        }

        // 延迟返回上一页
        setTimeout(() => {
          uni.navigateBack();
        }, 1500);

      } catch (error) {
        console.error('更新资料失败:', error);
        let errorMsg = '更新资料失败';
        
        if (error.errMsg) {
          errorMsg = '网络连接失败，请检查网络';
        } else if (error.data && error.data.detail) {
          errorMsg = error.data.detail;
        } else if (error.message) {
          errorMsg = error.message;
        }
        
        errorMessage.value = errorMsg;
      } finally {
        isSubmitting.value = false;
      }
    };

    onMounted(() => {
      loadUserProfile();
    });

    return {
      formData,
      isSubmitting,
      errorMessage,
      successMessage,
      isValid,
      onUsernameInput,
      onPhoneInput,
      onEmailInput,
      handleSave
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
  margin-bottom: 30px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.form-container {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.input-group {
  margin-bottom: 20px;
}

.input-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.input-field {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  font-size: 16px;
  background: #fafafa;
}

.save-btn {
  width: 100%;
  height: 50px;
  background: linear-gradient(45deg, #409eff, #66b1ff);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-top: 10px;
}

.save-btn:disabled {
  background: #cccccc;
  opacity: 0.6;
}

.error-message {
  background: #fef0f0;
  color: #f56c6c;
  padding: 12px;
  border-radius: 6px;
  margin-top: 15px;
  font-size: 14px;
  border-left: 4px solid #f56c6c;
}

.success-message {
  background: #f0f9ff;
  color: #67c23a;
  padding: 12px;
  border-radius: 6px;
  margin-top: 15px;
  font-size: 14px;
  border-left: 4px solid #67c23a;
}
</style>