// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Vuetify from "vuetify"
import "vuetify/dist/vuetify.min.css"

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import 'material-design-icons-iconfont/dist/material-design-icons.css'
import 'vue-select/dist/vue-select.css'

import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'

import locale from 'element-ui/lib/locale/lang/zh-TW'

Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(Vuetify)
Vue.use(ElementUI, { locale })
Vue.use(Antd)


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
