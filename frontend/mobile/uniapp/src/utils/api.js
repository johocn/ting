// API客户端配置
import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://www.joyogo.com/tingapi',  // 使用nginx代理路径
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么，比如添加认证token
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    return response.data;
  },
  error => {
    // 对响应错误做点什么
    if (error.response?.status === 401) {
      // 未授权，可能需要重新登录
      localStorage.removeItem('access_token');
      // 可以重定向到登录页面
    }
    return Promise.reject(error);
  }
);

// API接口定义
export const API = {
  // 认证相关
  auth: {
    register: (userData) => apiClient.post('/auth/auth/register', userData),
    login: (credentials) => apiClient.post('/auth/auth/login', credentials),
  },

  // 用户相关
  users: {
    getUsers: (params = {}) => apiClient.get('/users/users/', params),
    getUserProfile: () => apiClient.get('/users/users/profile'),
    updateUserProfile: (userData) => apiClient.put('/users/users/profile', userData),
    getUserById: (userId) => apiClient.get(`/users/users/${userId}`),
    updateUser: (userId, userData) => apiClient.put(`/users/users/${userId}`, userData),
    deleteUser: (userId) => apiClient.delete(`/users/users/${userId}`),
  },

  // 内容相关
  contents: {
    getContents: (params = {}) => apiClient.get('/contents/contents/', params),
    createContent: (contentData) => apiClient.post('/contents/contents/', contentData),
    getContentById: (contentId) => apiClient.get(`/contents/contents/${contentId}`),
    updateContent: (contentId, contentData) => apiClient.put(`/contents/contents/${contentId}`, contentData),
    deleteContent: (contentId) => apiClient.delete(`/contents/contents/${contentId}`),
    getContentQuestions: (contentId) => apiClient.get(`/contents/contents/${contentId}/questions`),
    createQuestion: (contentId, questionData) => apiClient.post(`/contents/contents/${contentId}/questions`, questionData),
    getQuizConfig: (contentId) => apiClient.get(`/contents/contents/${contentId}/quiz-config`),
    updateQuizConfig: (contentId, configData) => apiClient.put(`/contents/contents/${contentId}/quiz-config`, configData),
  },

  // 答题相关
  quizzes: {
    getContentQuestions: (contentId) => apiClient.get(`/quizzes/quizzes/${contentId}/questions`),
    getQuizConfig: (contentId) => apiClient.get(`/quizzes/quizzes/${contentId}/config`),
    submitQuiz: (submissionData) => apiClient.post('/quizzes/quizzes/submit', submissionData),
    getUserProgress: (contentId) => apiClient.get(`/quizzes/quizzes/${contentId}/user-progress`),
  },

  // 积分相关
  points: {
    getUserAccount: () => apiClient.get('/points/points/account'),
    getTransactions: (params = {}) => apiClient.get('/points/points/transactions', params),
    getExpiringPoints: () => apiClient.get('/points/points/expiring'),
    createTransaction: (transactionData) => apiClient.post('/points/points/transaction', transactionData),
    getExpirationRules: () => apiClient.get('/points/points/expiration-rules'),
  },

  // 渠道相关
  channels: {
    getChannelTypes: () => apiClient.get('/channels/channels/types'),
    getMyChannels: () => apiClient.get('/channels/channels/my'),
    getChannels: (params = {}) => apiClient.get('/channels/channels/', params),
    createChannel: (channelData) => apiClient.post('/channels/channels/', channelData),
    getChannelById: (channelId) => apiClient.get(`/channels/channels/${channelId}`),
    updateChannel: (channelId, channelData) => apiClient.put(`/channels/channels/${channelId}`, channelData),
    deleteChannel: (channelId) => apiClient.delete(`/channels/channels/${channelId}`),
    getChannelStats: (channelId, params = {}) => apiClient.get(`/channels/channels/${channelId}/statistics`, params),
    getChannelUsers: (channelId, params = {}) => apiClient.get(`/channels/channels/${channelId}/users`, params),
  },

  // 层级相关
  hierarchy: {
    getLevel: (levelId) => apiClient.get(`/hierarchy/hierarchy/${levelId}`),
    getLevelStats: (levelId) => apiClient.get(`/hierarchy/hierarchy/${levelId}/statistics`),
    getSubordinates: (levelId) => apiClient.get(`/hierarchy/hierarchy/${levelId}/subordinates`),
    getDirectUsers: (levelId, params = {}) => apiClient.get(`/hierarchy/hierarchy/${levelId}/users`, params),
  },

  // 核销相关
  verification: {
    getStoreInfo: () => apiClient.get('/verification/verification/store-info'),
    getDashboardStats: () => apiClient.get('/verification/verification/dashboard-stats'),
    getRecentVerifications: (params = {}) => apiClient.get('/verification/verification/recent', params),
    getVerificationDetail: (code) => apiClient.get('/verification/verification/detail', { params: { code } }),
    confirmVerification: (verificationData) => apiClient.post('/verification/verification/confirm', verificationData),
    generateQRCode: (data) => apiClient.get('/verification/verification/generate-qrcode', { params: { data } }),
  },

  // 健康检查
  health: () => apiClient.get('/health'),
};

export default apiClient;