// 引入组件
import type { App } from 'vue'
import SvgIconVue from './SvgIcon.vue'

// 所有全局组件集合
const allGlobalComponent: Record<string, any> = { SvgIconVue }

// 对外暴露插件对象
export default {
  // 务必叫 install 方法
  install(app: App) {
    // 注册项目全部的全局组件
    Object.keys(allGlobalComponent).forEach((key) => {
      // 注册全局组件
      app.component(key, allGlobalComponent[key])
    })
  }
}
