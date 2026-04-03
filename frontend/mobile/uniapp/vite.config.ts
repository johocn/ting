import { defineConfig } from "vite";
import uni from "@dcloudio/vite-plugin-uni";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    uni(),
  ],
  server: {
    host: '0.0.0.0',
    port: 8082,  // 更改端口以避免冲突
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 直接使用localhost:8000
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: 'dist/build/h5'
  }
});