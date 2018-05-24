// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import iView from 'iview';
import 'iview/dist/styles/iview.css';

Vue.config.productionTip = false
Vue.use(iView)
Vue.prototype.axios = axios
Vue.prototype.bus = new Vue()								// 兄弟组件间通信数据总线
Vue.prototype.baseUrl = "http://118.89.140.118:8888"		// 服务端基础url
axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})