const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false, //关闭代码检查
  //配置反向代理，解决跨域问题,需重启,必须要保存在重启
  devServer: {
    
    hot: true,//自动保存
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: false
      }
    }
  },
  
})

