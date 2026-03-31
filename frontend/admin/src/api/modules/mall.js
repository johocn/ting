import request from '@/api/index'

export const mallApi = {
  // 获取商品分类
  getCategories() {
    return request({
      url: '/products/categories',
      method: 'get'
    })
  },
  
  // 获取商品列表
  getList(params) {
    return request({
      url: '/products',
      method: 'get',
      params
    })
  },
  
  // 获取商品详情
  getDetail(productId) {
    return request({
      url: `/products/${productId}`,
      method: 'get'
    })
  },
  
  // 创建商品
  create(data) {
    return request({
      url: '/products',
      method: 'post',
      data
    })
  },
  
  // 更新商品
  update(productId, data) {
    return request({
      url: `/products/${productId}`,
      method: 'put',
      data
    })
  },
  
  // 删除商品
  delete(productId) {
    return request({
      url: `/products/${productId}`,
      method: 'delete'
    })
  },
  
  // 获取兑换记录
  getExchangeRecords(params) {
    return request({
      url: '/products/exchange/records',
      method: 'get',
      params
    })
  },
  
  // 获取兑换记录详情
  getExchangeRecord(recordId) {
    return request({
      url: `/products/exchange/record/${recordId}`,
      method: 'get'
    })
  },
  
  // 兑换商品
  exchange(productId, quantity = 1) {
    return request({
      url: `/products/${productId}/exchange`,
      method: 'post',
      params: { quantity }
    })
  }
}
