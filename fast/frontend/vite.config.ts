import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // 다른 장치에서 접근할 수 있도록 설정
    port: 5173 // 원하는 포트를 설정 (기본값은 5173)
  }
})