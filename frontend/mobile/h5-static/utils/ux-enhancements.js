/**
 * 用户体验优化工具
 * 包括加载动画、错误处理、离线支持
 */

// 加载动画管理器
class LoadingManager {
    constructor() {
        this.overlay = null;
        this.spinner = null;
        this.createOverlay();
    }

    createOverlay() {
        // 创建加载遮罩
        this.overlay = document.createElement('div');
        this.overlay.id = 'ting-loading-overlay';
        this.overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s, visibility 0.3s;
        `;

        // 创建加载动画
        this.spinner = document.createElement('div');
        this.spinner.id = 'ting-spinner';
        this.spinner.style.cssText = `
            display: flex;
            flex-direction: column;
            align-items: center;
        `;

        // 旋转圆圈动画
        const spinnerCircle = document.createElement('div');
        spinnerCircle.style.cssText = `
            width: 50px;
            height: 50px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #409eff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        `;

        // 添加CSS动画
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .loading-text {
                margin-top: 15px;
                color: #666;
                font-size: 14px;
            }
        `;
        document.head.appendChild(style);

        const loadingText = document.createElement('div');
        loadingText.className = 'loading-text';
        loadingText.textContent = '加载中...';

        this.spinner.appendChild(spinnerCircle);
        this.spinner.appendChild(loadingText);
        this.overlay.appendChild(this.spinner);
        document.body.appendChild(this.overlay);
    }

    show(message = '加载中...') {
        const loadingText = this.overlay.querySelector('.loading-text');
        if (loadingText) {
            loadingText.textContent = message;
        }
        this.overlay.style.opacity = '1';
        this.overlay.style.visibility = 'visible';
    }

    hide() {
        this.overlay.style.opacity = '0';
        this.overlay.style.visibility = 'hidden';
    }
}

// 错误处理管理器
class ErrorHandler {
    static showError(message, type = 'error') {
        // 创建错误提示
        const errorDiv = document.createElement('div');
        errorDiv.className = `ting-error-${type}`;
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? '#67c23a' : type === 'warning' ? '#e6a23c' : '#f56c6c'};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-width: 80%;
            text-align: center;
        `;
        errorDiv.textContent = message;

        document.body.appendChild(errorDiv);

        // 3秒后自动消失
        setTimeout(() => {
            errorDiv.style.transition = 'opacity 0.3s';
            errorDiv.style.opacity = '0';
            setTimeout(() => {
                if (errorDiv.parentNode) {
                    document.body.removeChild(errorDiv);
                }
            }, 300);
        }, 3000);

        return errorDiv;
    }

    static handleNetworkError(error) {
        console.error('网络错误:', error);
        this.showError('网络连接失败，请检查网络设置', 'error');
    }

    static handleAPIError(response) {
        if (response.status === 401) {
            this.showError('登录已过期，请重新登录', 'error');
            // 重定向到登录页面
            setTimeout(() => {
                window.location.href = '/ting';
            }, 1500);
        } else if (response.status === 403) {
            this.showError('权限不足', 'error');
        } else if (response.status === 500) {
            this.showError('服务器错误，请稍后重试', 'error');
        } else {
            this.showError(`请求失败: ${response.status}`, 'error');
        }
    }
}

// 离线支持管理器
class OfflineManager {
    constructor() {
        this.isOnline = navigator.onLine;
        this.cache = new Map();
        this.init();
    }

    init() {
        // 监听网络状态变化
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.handleConnectivityChange(true);
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.handleConnectivityChange(false);
        });

        // 初始化缓存
        this.loadCacheFromStorage();
    }

    handleConnectivityChange(isOnline) {
        if (isOnline) {
            ErrorHandler.showError('网络连接已恢复', 'success');
            // 尝试同步离线操作
            this.syncOfflineOperations();
        } else {
            ErrorHandler.showError('网络连接已断开，部分功能受限', 'warning');
        }
    }

    // 检查是否在线
    isCurrentlyOnline() {
        return this.isOnline && navigator.onLine;
    }

    // 缓存数据
    cacheData(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
        this.saveCacheToStorage();
    }

    // 获取缓存数据
    getCachedData(key, maxAge = 5 * 60 * 1000) { // 默认5分钟
        const cached = this.cache.get(key);
        if (cached && (Date.now() - cached.timestamp) < maxAge) {
            return cached.data;
        }
        return null;
    }

    // 保存缓存到本地存储
    saveCacheToStorage() {
        try {
            const serialized = new Map();
            for (let [key, value] of this.cache) {
                serialized.set(key, value);
            }
            localStorage.setItem('ting_cache', JSON.stringify(Array.from(serialized)));
        } catch (e) {
            console.warn('无法保存缓存到本地存储:', e);
        }
    }

    // 从本地存储加载缓存
    loadCacheFromStorage() {
        try {
            const serialized = localStorage.getItem('ting_cache');
            if (serialized) {
                const parsed = JSON.parse(serialized);
                this.cache = new Map(parsed);
            }
        } catch (e) {
            console.warn('无法从本地存储加载缓存:', e);
            this.cache = new Map();
        }
    }

    // 添加离线操作
    addOfflineOperation(operation) {
        try {
            let offlineOps = JSON.parse(localStorage.getItem('ting_offline_ops') || '[]');
            offlineOps.push({
                ...operation,
                timestamp: Date.now()
            });
            localStorage.setItem('ting_offline_ops', JSON.stringify(offlineOps));
        } catch (e) {
            console.error('无法保存离线操作:', e);
        }
    }

    // 同步离线操作
    async syncOfflineOperations() {
        try {
            let offlineOps = JSON.parse(localStorage.getItem('ting_offline_ops') || '[]');
            if (offlineOps.length > 0) {
                ErrorHandler.showError(`正在同步 ${offlineOps.length} 个离线操作...`, 'info');
                
                // 批量处理离线操作
                for (const op of offlineOps) {
                    try {
                        await this.processOfflineOperation(op);
                    } catch (error) {
                        console.error('同步操作失败:', op, error);
                    }
                }
                
                // 清除已同步的操作
                localStorage.setItem('ting_offline_ops', '[]');
                ErrorHandler.showError('离线操作同步完成', 'success');
            }
        } catch (e) {
            console.error('同步离线操作失败:', e);
        }
    }

    // 处理单个离线操作
    async processOfflineOperation(operation) {
        // 根据操作类型进行处理
        const { type, url, options } = operation;
        
        if (type === 'POST' || type === 'PUT' || type === 'DELETE') {
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...options.headers,
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            
            if (!response.ok) {
                throw new Error(`API调用失败: ${response.status}`);
            }
            
            return response.json();
        }
    }
}

// 请求包装器，集成加载动画和错误处理
class RequestWrapper {
    constructor() {
        this.loadingManager = new LoadingManager();
        this.errorHandler = ErrorHandler;
        this.offlineManager = new OfflineManager();
    }

    async request(url, options = {}) {
        const showLoading = options.showLoading !== false; // 默认显示
        const errorMessage = options.errorMessage || '请求失败';
        
        if (showLoading) {
            this.loadingManager.show(options.loadingMessage || '加载中...');
        }

        try {
            // 检查网络连接
            if (!this.offlineManager.isCurrentlyOnline()) {
                // 尝试使用缓存数据
                const cached = this.offlineManager.getCachedData(url);
                if (cached && options.allowCache !== false) {
                    console.log('使用缓存数据:', url);
                    return cached;
                }
                
                // 如果没有缓存且不允许离线操作，抛出错误
                if (options.method && ['POST', 'PUT', 'DELETE'].includes(options.method.toUpperCase())) {
                    // 将操作添加到离线队列
                    this.offlineManager.addOfflineOperation({
                        type: options.method,
                        url: url,
                        options: options
                    });
                    this.errorHandler.showError('操作已保存，网络恢复后将自动同步', 'warning');
                    return { success: true, offline: true };
                } else {
                    this.errorHandler.showError('当前处于离线状态，部分内容可能无法加载', 'warning');
                    throw new Error('Offline');
                }
            }

            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (showLoading) {
                this.loadingManager.hide();
            }

            if (!response.ok) {
                this.errorHandler.handleAPIError(response);
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            // 缓存GET请求的结果
            if (options.method === 'GET' || !options.method) {
                this.offlineManager.cacheData(url, data);
            }

            return data;
        } catch (error) {
            if (showLoading) {
                this.loadingManager.hide();
            }
            
            if (error.message === 'Offline') {
                // 离线状态下，对于GET请求尝试返回缓存
                if (!options.method || options.method.toUpperCase() === 'GET') {
                    const cached = this.offlineManager.getCachedData(url);
                    if (cached) {
                        return cached;
                    }
                }
            } else {
                this.errorHandler.handleNetworkError(error);
            }
            
            throw error;
        }
    }
}

// 初始化全局实例
const tingUX = {
    loading: new LoadingManager(),
    error: ErrorHandler,
    offline: new OfflineManager(),
    request: new RequestWrapper()
};

// 导出到全局
window.TingUX = tingUX;

export { LoadingManager, ErrorHandler, OfflineManager, RequestWrapper, tingUX };