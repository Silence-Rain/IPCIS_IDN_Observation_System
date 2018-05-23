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
Vue.prototype.bus = new Vue()
Vue.prototype.testUrl = "http://211.65.193.23:8888"
// Vue.prototype.prodUrl = "http://211.65.193.23:8888"
axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})