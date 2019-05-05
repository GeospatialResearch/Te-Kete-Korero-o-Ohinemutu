import Vue from 'vue'
import router from './router'
import App from './App'
import store from './store'

// import 'assets/css/app.styl'

// import bootstrap javascript
import 'bootstrap'

// import fontawesome icons
import { FontAwesomeIcon } from './utils/icons.js'
Vue.component('font-awesome-icon', FontAwesomeIcon)

// import css
import 'bootstrap/dist/css/bootstrap.min.css'
import './css/custom.css'
import 'ol/ol.css'


/* eslint-disable-next-line no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
