import request from '@/api/index'

export const contentApi = {
  // 获取内容列表
  getList(params) {
    return request({
      url: '/contents',
      method: 'get',
      params
    })
  },
  
  // 创建内容
  create(data) {
    return request({
      url: '/contents',
      method: 'post',
      data
    })
  },
  
  // 更新内容
  update(id, data) {
    return request({
      url: `/contents/${id}`,
      method: 'put',
      data
    })
  },
  
  // 删除内容
  delete(id) {
    return request({
      url: `/contents/${id}`,
      method: 'delete'
    })
  },
  
  // 获取内容详情
  getDetail(id) {
    return request({
      url: `/contents/${id}`,
      method: 'get'
    })
  },
  
  // 获取内容相关的问题
  getQuestions(contentId) {
    return request({
      url: `/contents/${contentId}/questions`,
      method: 'get'
    })
  },
  
  // 添加问题
  addQuestion(contentId, data) {
    return request({
      url: `/contents/${contentId}/questions`,
      method: 'post',
      data
    })
  }
}
