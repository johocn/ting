/**
 * 日期格式化工具
 */

/**
 * 格式化日期
 * @param {Date|string|number} date - 日期对象、字符串或时间戳
 * @param {string} fmt - 格式字符串，如 'yyyy-MM-dd hh:mm:ss'
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date, fmt = 'yyyy-MM-dd hh:mm:ss') {
  if (!date) return ''
  
  // 如果是时间戳，转换为Date对象
  if (typeof date === 'number' || typeof date === 'string') {
    date = new Date(date)
  }
  
  // 如果不是有效的日期对象，返回空字符串
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    return ''
  }
  
  const o = {
    'M+': date.getMonth() + 1, // 月份
    'd+': date.getDate(), // 日
    'h+': date.getHours(), // 小时
    'm+': date.getMinutes(), // 分
    's+': date.getSeconds(), // 秒
    'q+': Math.floor((date.getMonth() + 3) / 3), // 季度
    'S': date.getMilliseconds() // 毫秒
  }
  
  if (/(y+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
  }
  
  for (let k in o) {
    if (new RegExp('(' + k + ')').test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)))
    }
  }
  
  return fmt
}

/**
 * 计算时间差
 * @param {Date|string|number} startTime - 开始时间
 * @param {Date|string|number} endTime - 结束时间
 * @returns {Object} 包含天、小时、分钟、秒的对象
 */
export function timeDiff(startTime, endTime) {
  if (!startTime || !endTime) return null
  
  const start = new Date(startTime)
  const end = new Date(endTime)
  
  if (isNaN(start.getTime()) || isNaN(end.getTime())) {
    return null
  }
  
  let diff = Math.abs(end.getTime() - start.getTime())
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  diff -= days * (1000 * 60 * 60 * 24)
  
  const hours = Math.floor(diff / (1000 * 60 * 60))
  diff -= hours * (1000 * 60 * 60)
  
  const minutes = Math.floor(diff / (1000 * 60))
  diff -= minutes * (1000 * 60)
  
  const seconds = Math.floor(diff / 1000)
  
  return {
    days,
    hours,
    minutes,
    seconds
  }
}

/**
 * 相对时间格式化（如：几秒钟前、几分钟前）
 * @param {Date|string|number} date - 日期
 * @returns {string} 相对时间字符串
 */
export function relativeTime(date) {
  if (!date) return ''
  
  const now = new Date()
  const target = new Date(date)
  
  if (isNaN(target.getTime())) {
    return ''
  }
  
  const diff = now.getTime() - target.getTime()
  const minute = 1000 * 60
  const hour = minute * 60
  const day = hour * 24
  const week = day * 7
  const month = day * 30
  const year = day * 365
  
  if (diff < minute) {
    return '刚刚'
  } else if (diff < hour) {
    return Math.floor(diff / minute) + '分钟前'
  } else if (diff < day) {
    return Math.floor(diff / hour) + '小时前'
  } else if (diff < week) {
    return Math.floor(diff / day) + '天前'
  } else if (diff < month) {
    return Math.floor(diff / week) + '周前'
  } else if (diff < year) {
    return Math.floor(diff / month) + '个月前'
  } else {
    return Math.floor(diff / year) + '年前'
  }
}

/**
 * 格式化持续时间（秒数转为时分秒）
 * @param {number} seconds - 秒数
 * @returns {string} 格式化后的时分秒字符串
 */
export function formatDuration(seconds) {
  if (typeof seconds !== 'number' || seconds < 0) {
    return '0s'
  }
  
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  
  if (h > 0) {
    return `${h}h ${m}m ${s}s`
  } else if (m > 0) {
    return `${m}m ${s}s`
  } else {
    return `${s}s`
  }
}

/**
 * 获取今天开始和结束时间
 * @returns {Object} 包含今天开始和结束时间的对象
 */
export function getTodayRange() {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  return {
    start: today,
    end: tomorrow
  }
}

/**
 * 获取本周开始和结束时间
 * @returns {Object} 包含本周开始和结束时间的对象
 */
export function getWeekRange() {
  const now = new Date()
  const dayOfWeek = now.getDay() || 7 // 周日为0，转换为7
  const start = new Date(now)
  start.setDate(now.getDate() + (now.getDate() === 0 ? -6 : 1 - dayOfWeek))
  start.setHours(0, 0, 0, 0)
  
  const end = new Date(start)
  end.setDate(start.getDate() + 7)
  
  return {
    start,
    end
  }
}

/**
 * 获取本月开始和结束时间
 * @returns {Object} 包含本月开始和结束时间的对象
 */
export function getMonthRange() {
  const now = new Date()
  const start = new Date(now.getFullYear(), now.getMonth(), 1)
  const end = new Date(now.getFullYear(), now.getMonth() + 1, 1)
  
  return {
    start,
    end
  }
}
