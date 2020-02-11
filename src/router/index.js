import Vue from 'vue'
import Router from 'vue-router'

// import HomePage from 'pages/Home'
import ViewerPage from 'pages/Viewer'
import NotFoundPage from 'pages/404Page'

Vue.use(Router)

const routes = [
  {
    path: '/',
    component: ViewerPage
  },
  // {
  //   path: '/thing',
  //   component: HomePage
  // },
  // {
  //   path: '/other/thing',
  //   component: HomePage
  // },
  {
    path: '/confirmation/:key',
    name: 'verifyemail',
    component: ViewerPage
  },

  { path: '/#/404', component: NotFoundPage },
  { path: '*', redirect: '/#/404' }

  // { path: '*', component: NotFoundPage }, // to use with mode:'history'
]

var router = new Router({
    // mode:'history',
    routes: routes
})

export default router
