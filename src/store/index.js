import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'

Vue.use(Vuex)

const apiRoot = process.env.API_HOST + '/v1'

const store = new Vuex.Store({
  state: {
    flavor: '',
    map: null,
    isUploadingData: false,
    contentToShow: 'map',
    externalLayers: null
  },
  mutations: {
    CHANGE (state, flavor) {
      state.flavor = flavor
    },
    // Map related functions
    SET_MAP (state, map) {
      state.map = map
    },
    TOGGLE_CONTENT (state, content) {
      state.contentToShow = content
    },
    SET_EXTERNAL_LAYERS (state, layersObj) {
      state.externalLayers = layersObj
    },
    // Generic fail handling
    // API_FAIL (state, error) {
    //   if (error.status === 401 || error.status === 403) {
    //     console.error("Authentication error found. Logging user out.")
    //     store.commit("DEAUTHENTICATE")
    //     if (router.currentRoute.path === '/projects') {
    //       // Getting projects to refresh the list because we're looking at it.
    //       store.dispatch('getProjectsSummary')
    //     } else {
    //       router.push('/')
    //     }
    //   } else {
    //     console.error(error)
    //   }
    // }
  },
  getters: {
    flavor: state => state.flavor
  },
  actions: {
    uploadFile (store, datafile) {
      return api.post(apiRoot + '/upload_file/', datafile)
        .then((response) => {
          // store.commit('GET_LOTS', response)
          console.log(response)
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    }
  }
})

export default store
