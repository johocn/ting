import request from '@/api/index'

export const channelApi = {
  // 获取渠道类型
  getTypes() {
    return request({
      url: '/channels/types',
      method: 'get'
    })
  },
  
  // 获取我的渠道
  getMyChannels() {
    return request({
      url: '/channels/my',
      method: 'get'
    })
  },
  
  // 获取渠道列表
  getList(params) {
    return request({
      url: '/channels',
      method: 'get',
      params
    })
  },
  
  // 获取渠道详情
  getDetail(channelId) {
    return request({
      url: `/channels/${channelId}`,
      method: 'get'
    })
  },
  
  // 创建渠道
  create(data) {
    return request({
      url: '/channels',
      method: 'post',
      data
    })
  },
  
  // 更新渠道
  update(channelId, data) {
    return request({
      url: `/channels/${channelId}`,
      method: 'put',
      data
    })
  },
  
  // 删除渠道
  delete(channelId) {
    return request({
      url: `/channels/${channelId}`,
      method: 'delete'
    })
  },
  
  // 获取渠道统计
  getStatistics(channelId, params) {
    return request({
      url: `/channels/${channelId}/statistics`,
      method: 'get',
      params
    })
  },
  
  // 获取渠道用户
  getUsers(channelId, params) {
    return request({
      url: `/channels/${channelId}/users`,
      method: 'get',
      params
    })
  }
}
