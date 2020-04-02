import Vue from 'vue'
import router from './router'
import App from './App'
import store from './store'

// import 'assets/css/app.styl'

// import javascript
import 'malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.concat.min.js'
import 'malihu-custom-scrollbar-plugin'
import 'jquery/dist/jquery.min.js'
import 'popper.js'
import 'bootstrap'
import 'bootstrap-select'

// import vue-moment
import vueMoment from 'vue-moment'
Vue.use(vueMoment)

// import fontawesome icons
import { FontAwesomeIcon } from './utils/icons.js'
Vue.component('font-awesome-icon', FontAwesomeIcon)

// import VueDraggable
import vuedraggable from 'vuedraggable'
Vue.use(vuedraggable)

// import css

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-select/dist/css/bootstrap-select.min.css'
import './css/custom.css'
import './css/sidebar.css'
import './css/sidebar-themes.css'
import 'ol/ol.css'
import 'malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.css'
import 'animate.css'
import 'ol-geocoder/dist/ol-geocoder.css'
import 'ol-ext/dist/ol-ext.css'

// initialising all popovers
$(function () {
  $('[data-toggle="popover"]').popover({
    boundary:'window',
    html: true
  })
})

// import notifications
import Notifications from 'bootstrap-notify'
Vue.use(Notifications)

/* eslint-disable-next-line no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
