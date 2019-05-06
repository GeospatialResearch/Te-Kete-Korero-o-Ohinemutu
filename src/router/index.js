import Vue from 'vue'
import Router from 'vue-router'

// import Home from 'pages/Home'
import Viewer from 'pages/Viewer'

Vue.use(Router)

const routes = [
  {
    path: '*',
    component: Viewer
  }
]

export default new Router({
  routes
})
