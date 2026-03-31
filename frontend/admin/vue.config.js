const { defineConfig } = require('@vue/cli-service')

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
      .set('@', resolve('src'))
      .set('@assets', resolve('src/assets'))
      .set('@components', resolve('src/components'))
      .set('@views', resolve('src/views'))
      .set('@utils', resolve('src/utils'))
      .set('@api', resolve('src/api'))
    
    // 优化图片处理
    config.module
      .rule('images')
      .use('url-loader')
      .tap(options => {
        options.limit = 4096
        return options
      })
  }
})

function resolve(dir) {
  return require('path').join(__dirname, dir)
}
