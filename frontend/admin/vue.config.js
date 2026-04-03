const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // 开发服务器配置
  devServer: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api/v1'
        }
      }
    }
  },
  
  // CSS配置
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  },
  
  // 构建配置
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          elementPlus: {
            name: 'chunk-element-plus',
            test: /[\\/]node_modules[\\/]_?element-plus(.*)/,
            priority: 10
          },
          echarts: {
            name: 'chunk-echarts',
            test: /[\\/]node_modules[\\/](vue-)?echarts[\\/]/,
            priority: 10
          }
        }
      }
    }
  },
  
  // 链式配置
  chainWebpack: config => {
    // 配置别名
    config.resolve.alias
      .set('@', path.join(__dirname, 'src'))
      .set('@assets', path.join(__dirname, 'src/assets'))
      .set('@components', path.join(__dirname, 'src/components'))
      .set('@views', path.join(__dirname, 'src/views'))
      .set('@utils', path.join(__dirname, 'src/utils'))
      .set('@api', path.join(__dirname, 'src/api'))
    
    // 优化图片处理
    config.module
      .rule('images')
      .use('url-loader')
      .tap(options => {
        if (options) {
          options.limit = 4096
        }
        return options
      })
  }
})
