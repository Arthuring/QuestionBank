import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'
import * as icons from '@element-plus/icons-vue'

import '@/assets/css/global.css'

const app = createApp(App).use(store).use(router).use(ElementPlus,{size:'small'})
Object.keys(icons).forEach(key => {
    app.component(key, icons[key])
})
app.mount('#app')