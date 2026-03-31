import request from '@/api/index'

export const pointsApi = {
  // 获取积分账户信息
  getAccount() {
    return request({
      url: '/points/account',
      method: 'get'
    })
  },
  
  // 获取积分流水
  getTransactions(params) {
    return request({
      url: '/points/transactions',
      method: 'get',
      params
    })
  },
  
  // 获取即将过期积分
  getExpiring() {
    return request({
      url: '/points/expiring',
      method: 'get'
    })
  },
  
  // 获取积分过期规则
  getExpirationRules() {
    return request({
      url: '/points/expiration-rules',
      method: 'get'
    })
  },
  
  // 创建积分流水
  createTransaction(data) {
    return request({
      url: '/points/transaction',
      method: 'post',
      data
    })
  }
}
