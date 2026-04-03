<template>
  <view class="container">
    <view class="header">
      <text class="title">用户登录</text>
      <text class="subtitle">欢迎回到Ting学习平台</text>
    </view>

    <view class="form-container">
      <view class="input-group">
        <input 
          class="input-field" 
          type="text" 
          placeholder="请输入用户名" 
          v-model="formData.username"
          @input="onUsernameInput"
        />
        <text class="input-icon">👤</text>
      </view>

      <view class="input-group">
        <input 
          class="input-field" 
          type="password" 
          placeholder="请输入密码" 
          v-model="formData.password"
          @input="onPasswordInput"
        />
        <text class="input-icon">🔒</text>
      </view>

      <button 
        class="login-btn" 
        :disabled="!isValid || isSubmitting"
        @click="handleLogin"
      >
        {{ isSubmitting ? '登录中...' : '立即登录' }}
      </button>

      <view class="register-link">
        <text>还没有账号？</text>
        <text class="link-text" @click="goToRegister">立即注册</text>
      </view>

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
import { ref, reactive, computed } from 'vue';
import { API } from '../../utils/request';

export default {
  name: 'LoginPage',
  setup() {
    // 表单数据
    const formData = reactive({
      username: '',
      password: ''
    });

    // 状态管理
    const isSubmitting = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');

    // 验证函数
    const isValid = computed(() => {
      return (
        formData.username.trim() !== '' &&
        formData.password.trim() !== ''
      );
    });

    // 输入处理函数
    const onUsernameInput = (e) => {
      formData.username = e.detail.value;
      if (errorMessage.value.includes('用户名')) {
        errorMessage.value = '';
      }
    };

    const onPasswordInput = (e) => {
      formData.password = e.detail.value;
      if (errorMessage.value.includes('密码')) {
        errorMessage.value = '';
      }
    };

    // 登录处理函数
    const handleLogin = async () => {
      if (!isValid.value) {
        errorMessage.value = '请填写完整的登录信息';
        return;
      }

      isSubmitting.value = true;
      errorMessage.value = '';
      successMessage.value = '';

      try {
        const loginData = {
          username: formData.username,
          password: formData.password
        };

        const response = await API.user.login(loginData);
        
        successMessage.value = '登录成功！正在跳转...';
        
        // 存储token
        if (response.token) {
          uni.setStorageSync('access_token', response.token);
          uni.setStorageSync('user_info', {
            id: response.user_id,
            username: response.username
          });
        }

        // 延迟跳转到首页
        setTimeout(() => {
          uni.switchTab({
            url: '/pages/index/index'
          });
        }, 1000);

      } catch (error) {
        console.error('登录失败:', error);
        let errorMsg = '登录失败';
        
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

    // 跳转到注册页
    const goToRegister = () => {
      uni.redirectTo({
        url: '/pages/register/register'
      });
    };

    return {
      formData,
      isSubmitting,
      errorMessage,
      successMessage,
      isValid,
      onUsernameInput,
      onPasswordInput,
      handleLogin,
      goToRegister
    };
  }
};
</script>

<style>
.container {
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 28px;
  font-weight: bold;
  color: white;
  display: block;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  display: block;
}

.form-container {
  background: white;
  border-radius: 15px;
  padding: 30px 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.input-group {
  position: relative;
  margin-bottom: 20px;
}

.input-field {
  width: 100%;
  padding: 15px 45px 15px 15px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  font-size: 16px;
  background: #fafafa;
}

.input-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: #999;
}

.login-btn {
  width: 100%;
  height: 50px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-top: 10px;
}

.login-btn:disabled {
  background: #cccccc;
  opacity: 0.6;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.link-text {
  color: #667eea;
  margin-left: 5px;
  text-decoration: underline;
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