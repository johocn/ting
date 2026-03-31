/**
 * 通用工具函数
 */

/**
 * 深拷贝对象
 * @param {Object} obj - 要深拷贝的对象
 * @returns {Object} 拷贝后的对象
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime())
  }
  
  if (obj instanceof Array) {
    return obj.reduce((arr, item) => {
      arr.push(deepClone(item))
      return arr
    }, [])
  }
  
  if (typeof obj === 'object') {
    return Object.keys(obj).reduce((newObj, key) => {
      newObj[key] = deepClone(obj[key])
      return newObj
    }, {})
  }
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {number} delay - 延迟时间
 * @returns {Function} 防抖后的函数
 */
export function debounce(func, delay) {
  let timeoutId
  return function (...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func.apply(this, args), delay)
  }
}

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {number} delay - 延迟时间
 * @returns {Function} 节流后的函数
 */
export function throttle(func, delay) {
  let lastCall = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastCall >= delay) {
      lastCall = now
      func.apply(this, args)
    }
  }
}

/**
 * 生成唯一ID
 * @param {string} prefix - 前缀
 * @returns {string} 唯一ID
 */
export function generateId(prefix = '') {
  return prefix + (+new Date()).toString(36) + Math.random().toString(36).substr(2)
}

/**
 * 格式化数字（千分位分隔符）
 * @param {number} num - 要格式化的数字
 * @returns {string} 格式化后的数字字符串
 */
export function formatNumber(num) {
  if (num === null || num === undefined) return ''
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 格式化大数字（如：1.2k, 1.2m）
 * @param {number} num - 要格式化的数字
 * @returns {string} 格式化后的数字字符串
 */
export function formatLargeNumber(num) {
  if (num === null || num === undefined) return ''
  
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'm'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

/**
 * 验证手机号
 * @param {string} phone - 手机号
 * @returns {boolean} 是否为有效手机号
 */
export function validatePhone(phone) {
  const regex = /^1[3-9]\d{9}$/
  return regex.test(phone)
}

/**
 * 驗证邮箱
 * @param {string} email - 邮箱
 * @returns {boolean} 是否为有效邮箱
 */
export function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

/**
 * 驗证URL
 * @param {string} url - URL
 * @returns {boolean} 是否为有效URL
 */
export function validateUrl(url) {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * URL参数解析
 * @param {string} url - URL
 * @returns {Object} 参数对象
 */
export function getUrlParams(url) {
  const params = {}
  const parser = document.createElement('a')
  parser.href = url
  
  const query = parser.search.substring(1)
  if (query) {
    query.split('&').forEach(param => {
      const [key, value] = param.split('=')
      params[decodeURIComponent(key)] = decodeURIComponent(value || '')
    })
  }
  
  return params
}

/**
 * 将对象转换为URL参数字符串
 * @param {Object} obj - 参数对象
 * @returns {string} URL参数字符串
 */
export function objToUrlParams(obj) {
  return Object.keys(obj).map(key => 
    encodeURIComponent(key) + '=' + encodeURIComponent(obj[key])
  ).join('&')
}

/**
 * 获取文件扩展名
 * @param {string} filename - 文件名
 * @returns {string} 扩展名
 */
export function getFileExtension(filename) {
  return filename.split('.').pop().toLowerCase()
}

/**
 * 格化文件大小
 * @param {number} bytes - 字节数
 * @returns {string} 格式化后的文件大小
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 生成随机字符串
 * @param {number} length - 长度
 * @returns {string} 随机字符串
 */
export function randomString(length = 8) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * 检查是否为移动端
 * @returns {boolean} 是否为移动端
 */
export function isMobile() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
}

/**
 * 复制文本到剪贴板
 * @param {string} text - 要复制的文本
 * @returns {Promise<boolean>} 是否复制成功
 */
export async function copyToClipboard(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
      return true
    } else {
      // 降级方案
      const textArea = document.createElement('textarea')
      textArea.value = text
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      textArea.style.top = '-999999px'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      
      const result = document.execCommand('copy')
      textArea.remove()
      return result
    }
  } catch (err) {
    console.error('Failed to copy: ', err)
    return false
  }
}
