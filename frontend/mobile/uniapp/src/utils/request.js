// uni-app 请求封装
// 生产环境使用 nginx 代理地址，开发环境可使用本地地址
const BASE_URL = 'http://www.joyogo.com/tingapi';
// 开发环境可切换为：const BASE_URL = 'http://localhost:8000';

class Request {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
  }

  // 通用请求方法
  request(options = {}) {
    return new Promise((resolve, reject) => {
      // 获取token
      const token = uni.getStorageSync('access_token') || '';
      
      uni.request({
        url: this.baseURL + options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` }),
          ...options.header
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            // 错误处理
            reject(res);
          }
        },
        fail: (err) => {
          reject(err);
        }
      });
    });
  }

  // GET请求
  get(url, params = {}, header = {}) {
    return this.request({
      url,
      method: 'GET',
      data: params,
      header
    });
  }

  // POST请求
  post(url, data = {}, header = {}) {
    return this.request({
      url,
      method: 'POST',
      data,
      header
    });
  }

  // PUT请求
  put(url, data = {}, header = {}) {
    return this.request({
      url,
      method: 'PUT',
      data,
      header
    });
  }

  // DELETE请求
  delete(url, data = {}, header = {}) {
    return this.request({
      url,
      method: 'DELETE',
      data,
      header
    });
  }
}

// 创建API实例
const api = new Request(BASE_URL);

// API接口定义
export const API = {
  // 健康检查
  health: () => api.get('/health'),

  // 用户相关API
  user: {
    // 获取用户列表
    getUsers: (params = {}) => api.get('/api/v1/users/users/', params),
    
    // 获取用户信息
    getUserProfile: () => api.get('/api/v1/users/users/profile'),
    
    // 更新用户信息
    updateUserProfile: (data) => api.put('/api/v1/users/users/profile', data),
    
    // 用户注册
    register: (data) => api.post('/api/v1/auth/auth/register', data),
    
    // 用户登录
    login: (data) => api.post('/api/v1/auth/auth/login', data),
  },

  // 内容相关API
  content: {
    // 获取内容列表
    getContents: (params = {}) => api.get('/api/v1/contents/contents/', params),
    
    // 获取单个内容
    getContent: (id) => api.get(`/api/v1/contents/contents/${id}`),
    
    // 创建内容
    createContent: (data) => api.post('/api/v1/contents/contents/', data),
    
    // 更新内容
    updateContent: (id, data) => api.put(`/api/v1/contents/contents/${id}`, data),
    
    // 删除内容
    deleteContent: (id) => api.delete(`/api/v1/contents/contents/${id}`),
    
    // 获取内容相关问题
    getContentQuestions: (contentId) => api.get(`/api/v1/contents/contents/${contentId}/questions`),
    
    // 获取答题配置
    getQuizConfig: (contentId) => api.get(`/api/v1/contents/contents/${contentId}/quiz-config`),
  },

  // 答题相关API
  quiz: {
    // 提交答题
    submitQuiz: (data) => api.post('/api/v1/quizzes/quizzes/submit', data),
    
    // 获取内容的问题
    getContentQuestions: (contentId) => api.get(`/api/v1/quizzes/quizzes/${contentId}/questions`),
    
    // 获取用户答题进度
    getUserProgress: (contentId) => api.get(`/api/v1/quizzes/quizzes/${contentId}/user-progress`),
    
    // 获取答题配置
    getQuizConfig: (contentId) => api.get(`/api/v1/quizzes/quizzes/${contentId}/config`),
  },

  // 积分相关API
  points: {
    // 获取用户积分账户
    getUserAccount: () => api.get('/api/v1/points/points/account'),
    
    // 获取积分交易记录
    getTransactions: (params = {}) => api.get('/api/v1/points/points/transactions', params),
    
    // 获取即将过期的积分
    getExpiringPoints: () => api.get('/api/v1/points/points/expiring'),
    
    // 创建积分交易
    createTransaction: (data) => api.post('/api/v1/points/points/transaction', data),
    
    // 获取过期规则
    getExpirationRules: () => api.get('/api/v1/points/points/expiration-rules'),
  },

  // 渠道相关API
  channel: {
    // 获取渠道类型
    getChannelTypes: () => api.get('/api/v1/channels/channels/types'),
    
    // 获取我的渠道
    getMyChannels: () => api.get('/api/v1/channels/channels/my'),
    
    // 获取渠道列表
    getChannels: (params = {}) => api.get('/api/v1/channels/channels/', params),
    
    // 创建渠道
    createChannel: (data) => api.post('/api/v1/channels/channels/', data),
    
    // 获取单个渠道
    getChannel: (id) => api.get(`/api/v1/channels/channels/${id}`),
    
    // 更新渠道
    updateChannel: (id, data) => api.put(`/api/v1/channels/channels/${id}`, data),
    
    // 删除渠道
    deleteChannel: (id) => api.delete(`/api/v1/channels/channels/${id}`),
    
    // 获取渠道统计
    getChannelStats: (id, params = {}) => api.get(`/api/v1/channels/channels/${id}/statistics`, params),
    
    // 获取渠道用户
    getChannelUsers: (id, params = {}) => api.get(`/api/v1/channels/channels/${id}/users`, params),
  },

  // 层级相关API
  hierarchy: {
    // 获取层级信息
    getLevel: (id) => api.get(`/api/v1/hierarchy/hierarchy/${id}`),
    
    // 获取层级统计
    getLevelStats: (id) => api.get(`/api/v1/hierarchy/hierarchy/${id}/statistics`),
    
    // 获取下级信息
    getSubordinates: (id) => api.get(`/api/v1/hierarchy/hierarchy/${id}/subordinates`),
    
    // 获取直属用户
    getDirectUsers: (id, params = {}) => api.get(`/api/v1/hierarchy/hierarchy/${id}/users`, params),
  },

  // 核销相关API
  verification: {
    // 获取店铺信息
    getStoreInfo: () => api.get('/api/v1/verification/verification/store-info'),
    
    // 获取核销统计
    getDashboardStats: () => api.get('/api/v1/verification/verification/dashboard-stats'),
    
    // 获取近期核销记录
    getRecentVerifications: (params = {}) => api.get('/api/v1/verification/verification/recent', params),
    
    // 确认核销
    confirmVerification: (data) => api.post('/api/v1/verification/verification/confirm', data),
    
    // 生成二维码
    generateQRCode: (data) => api.get('/api/v1/verification/verification/generate-qrcode', data),
  },

  // 学习进度相关API
  learning: {
    // 开始学习
    startLearning: (contentId) => api.post('/api/v1/learning/learning/start-learning', { content_id: contentId }),
    
    // 更新学习进度
    updateProgress: (sessionId, watchedDuration) => api.post('/api/v1/learning/learning/update-progress', {
      session_id: sessionId,
      watched_duration: watchedDuration
    }),
    
    // 完成学习
    completeLearning: (sessionId) => api.post('/api/v1/learning/learning/complete-learning', { session_id: sessionId }),
    
    // 获取用户学习进度
    getUserProgress: () => api.get('/api/v1/learning/learning/user-progress'),
    
    // 获取内容学习统计
    getContentStats: (contentId) => api.get(`/api/v1/learning/learning/content-progress/${contentId}`),
  }
};

export default api;