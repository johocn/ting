<template>
  <view class="container">
    <view class="header">
      <text class="title">用户注册</text>
      <text class="subtitle">加入Ting学习平台，开启学习之旅</text>
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
          type="text" 
          placeholder="请输入手机号" 
          v-model="formData.phone"
          @input="onPhoneInput"
        />
        <text class="input-icon">📱</text>
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

      <view class="input-group">
        <input 
          class="input-field" 
          type="password" 
          placeholder="请确认密码" 
          v-model="formData.confirmPassword"
          @input="onConfirmPasswordInput"
        />
        <text class="input-icon">🔒</text>
      </view>

      <button 
        class="register-btn" 
        :disabled="!isValid || isSubmitting"
        @click="handleRegister"
      >
        {{ isSubmitting ? '注册中...' : '立即注册' }}
      </button>

      <view class="login-link">
        <text>已有账号？</text>
        <text class="link-text" @click="goToLogin">立即登录</text>
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
  name: 'RegisterPage',
  setup() {
    // 表单数据
    const formData = reactive({
      username: '',
      phone: '',
      password: '',
      confirmPassword: ''
    });

    // 状态管理
    const isSubmitting = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');

    // 验证函数
    const isValid = computed(() => {
      return (
        formData.username.trim() !== '' &&
        formData.phone.trim() !== '' &&
        formData.password.trim() !== '' &&
        formData.password === formData.confirmPassword &&
        validatePhone(formData.phone)
      );
    });

    // 手机号验证
    const validatePhone = (phone) => {
      const phoneRegex = /^1[3-9]\d{9}$/;
      return phoneRegex.test(phone);
    };

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

    const onPasswordInput = (e) => {
      formData.password = e.detail.value;
      if (errorMessage.value.includes('密码')) {
        errorMessage.value = '';
      }
    };

    const onConfirmPasswordInput = (e) => {
      formData.confirmPassword = e.detail.value;
      if (errorMessage.value.includes('密码')) {
        errorMessage.value = '';
      }
    };

    // 注册处理函数
    const handleRegister = async () => {
      if (!isValid.value) {
        errorMessage.value = '请填写完整且有效的注册信息';
        return;
      }

      isSubmitting.value = true;
      errorMessage.value = '';
      successMessage.value = '';

      try {
        const registerData = {
          username: formData.username,
          password: formData.password,
          phone: formData.phone
        };

        const response = await API.user.register(registerData);
        
        successMessage.value = '注册成功！正在跳转登录页面...';
        
        // 存储token
        if (response.token) {
          uni.setStorageSync('access_token', response.token);
          uni.setStorageSync('user_info', {
            id: response.user_id,
            username: response.username
          });
        }

        // 延迟跳转到登录页面
        setTimeout(() => {
          uni.redirectTo({
            url: '/pages/login/login'
          });
        }, 1500);

      } catch (error) {
        console.error('注册失败:', error);
        let errorMsg = '注册失败';
        
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

    // 跳转到登录页
    const goToLogin = () => {
      uni.redirectTo({
        url: '/pages/login/login'
      });
    };

    return {
      formData,
      isSubmitting,
      errorMessage,
      successMessage,
      isValid,
      onUsernameInput,
      onPhoneInput,
      onPasswordInput,
      onConfirmPasswordInput,
      handleRegister,
      goToLogin
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

.register-btn {
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

.register-btn:disabled {
  background: #cccccc;
  opacity: 0.6;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.link-text {
  color: #667eea;
  margin-left: 5px;
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