import Vue from 'vue'
import Vuex from 'vuex'
// import api from './api.js'

Vue.use(Vuex)

// const apiRoot = process.env.API_HOST + '/v1'

const store = new Vuex.Store({
  state: {
    flavor: ''
  },
  mutations: {
    change (state, flavor) {
      state.flavor = flavor
    }
  },
  getters: {
    flavor: state => state.flavor
  },
  actions: {
    // getLots (store, projectId) {
    //   return api.get(apiRoot + '/lots/?project=' + projectId, { headers: auth.getAuthHeader() })
    //     .then((response) => {
    //       store.commit('GET_LOTS', response)
    //     })
    //     .catch((error) => store.commit('API_FAIL', error))
    // }
  }
})

export default store
