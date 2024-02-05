import vue from '@vitejs/plugin-vue';

export default {
  plugins: [vue()],
  server: {
    port: 5173, // Порт, на котором будет запущен сервер разработки
  },
};
