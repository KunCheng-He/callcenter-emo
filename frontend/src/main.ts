import './assets/styles/index.scss'  // 引入全局样式

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
// import '@/assets/styles/element-variables.scss'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'virtual:svg-icons-register'
import globalComponent from '@/components'  // 全局组件

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus, {  // 引入element-plus
    locale: zhCn,       // 设置语言
  })
app.use(globalComponent)  // 注册全局组件

app.mount('#app')
