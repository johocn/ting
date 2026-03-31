import request from '@/api/index'

export const userApi = {
  // 获取用户列表
  getList(params) {
    return request({
      url: '/users',
      method: 'get',
      params
    })
  },
  
  // 获取用户资料
  getProfile() {
    return request({
      url: '/users/profile',
      method: 'get'
    })
  },
  
  // 更新用户资料
  updateProfile(data) {
    return request({
      url: '/users/profile',
      method: 'put',
      data
    })
  },
  
  // 获取用户详情
  getDetail(userId) {
    return request({
      url: `/users/${userId}`,
      method: 'get'
    })
  },
  
  // 更新用户
  update(userId, data) {
    return request({
      url: `/users/${userId}`,
      method: 'put',
      data
    })
  },
  
  // 删除用户
  delete(userId) {
    return request({
      url: `/users/${userId}`,
      method: 'delete'
    })
  }
}
