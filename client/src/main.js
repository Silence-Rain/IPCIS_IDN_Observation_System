/* eslint-disable */

import Vue from 'vue'
import router from './router'
import App from './App.vue'
import axios from 'axios'
import iView from 'iview'
import 'iview/dist/styles/iview.css'

Vue.config.productionTip = false
Vue.use(iView)
Vue.prototype.axios = axios
Vue.prototype.bus = new Vue()								// 兄弟组件间通信数据总线
Vue.prototype.baseUrl = "http://211.65.193.23:8888"			// 服务端基础url
axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded'

new Vue({
	router,
	components: { App },
	template: '<App/>',
	render: h => h(App)
}).$mount('#app')
