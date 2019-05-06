import Vue from 'vue'
import Vuex from 'vuex'
import { EventBus } from './event-bus.js'
// import api from './api.js'

Vue.use(Vuex)

// const apiRoot = process.env.API_HOST + '/v1'

const store = new Vuex.Store({
  state: {
    flavor: '',
    showLeftPanel: true,
    map: null
  },
  mutations: {
    CHANGE (state, flavor) {
      state.flavor = flavor
    },
    // UI Actions
    TOGGLE_LEFT_PANEL (state) {
      state.showLeftPanel = !state.showLeftPanel
      store.commit('UPDATESIZE_MAP')
    },
    // Map related functions
    SET_MAP (state, map) {
      state.map = map
    },
    UPDATESIZE_MAP () {
      EventBus.$emit('updatesize-map', 5)
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
