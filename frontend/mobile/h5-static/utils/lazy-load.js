/**
 * 图片懒加载工具
 * 用于优化前端页面性能
 */

// 检测Intersection Observer API支持
const supportsIntersectionObserver = 'IntersectionObserver' in window;

// 懒加载配置
const LAZY_LOAD_CONFIG = {
    rootMargin: '50px 0px',  // 提前50px开始加载
    threshold: 0.01          // 1%可见时触发
};

// 懒加载类
class LazyLoader {
    constructor() {
        this.observer = null;
        this.init();
    }

    init() {
        if (supportsIntersectionObserver) {
            this.observer = new IntersectionObserver(this.handleIntersection.bind(this), LAZY_LOAD_CONFIG);
        }
        
        // 初始化所有懒加载元素
        this.setupLazyElements();
    }

    setupLazyElements() {
        // 处理图片懒加载
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => this.observeElement(img));
        
        // 处理背景图片懒加载
        const lazyBgElements = document.querySelectorAll('[data-bg]');
        lazyBgElements.forEach(el => this.observeElement(el));
    }

    observeElement(element) {
        if (this.observer) {
            this.observer.observe(element);
        } else {
            // 降级处理：直接加载
            this.loadElement(element);
        }
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.loadElement(entry.target);
                this.observer.unobserve(entry.target);
            }
        });
    }

    loadElement(element) {
        if (element.tagName === 'IMG') {
            // 加载图片
            const src = element.dataset.src;
            if (src) {
                element.src = src;
                element.onload = () => {
                    element.classList.add('loaded');
                    element.classList.remove('lazy');
                };
                element.onerror = () => {
                    element.classList.add('error');
                    element.classList.remove('lazy');
                };
            }
        } else if (element.dataset.bg) {
            // 加载背景图片
            const bgSrc = element.dataset.bg;
            element.style.backgroundImage = `url(${bgSrc})`;
            element.classList.add('loaded');
            element.classList.remove('lazy-bg');
        }
    }
}

// 代码分割和动态加载工具
class CodeSplitter {
    static async loadModule(url) {
        try {
            const module = await import(url);
            return module;
        } catch (error) {
            console.error('模块加载失败:', error);
            return null;
        }
    }

    static async loadComponent(componentName) {
        // 根据组件名称动态加载对应的模块
        const componentMap = {
            'calendar': './components/calendar.js',
            'chart': './components/chart.js',
            'player': './components/player.js',
            'notification-center': './components/notification-center.js'
        };

        const url = componentMap[componentName];
        if (url) {
            return await this.loadModule(url);
        }
        return null;
    }

    static lazyLoadScript(src, callback) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.async = true;
            
            script.onload = () => {
                if (callback) callback();
                resolve(script);
            };
            
            script.onerror = () => {
                reject(new Error(`Script load error for ${src}`));
            };
            
            document.head.appendChild(script);
        });
    }
}

// 工具函数：防抖
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 工具函数：节流
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 初始化懒加载
document.addEventListener('DOMContentLoaded', () => {
    new LazyLoader();
});

// 导出到全局 window（兼容普通脚本加载）
window.LazyLoader = LazyLoader;
window.CodeSplitter = CodeSplitter;
window.debounce = debounce;
window.throttle = throttle;

window.TingUtils = {
    LazyLoader,
    CodeSplitter,
    debounce,
    throttle
};