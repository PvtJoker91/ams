import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    target: 'modules',
    outDir: 'dist',
    assetsDir: 'assets',
    minify: 'terser', // Минификация кода
    terserOptions: {
      compress: {
        drop_console: true, // Удалить console.log из продакшен-кода
      },
    },
  },
})