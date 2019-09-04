import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'
import { EventBus } from './event-bus'
import { each } from 'underscore'

Vue.use(Vuex)

const apiRoot = process.env.API_HOST + '/v1'

const store = new Vuex.Store({
  state: {
    flavor: '',
    map: null,
    isLoading: false,
    isUploadingData: false,
    isPanelOpen: false,
    contentToShow: 'map',
    externalLayers: null,
    internalLayers: {},
    map_resolution: 0,
    map_zoom: 0,
    stories: [],
    storyContent: {}
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
    SET_INTERNAL_LAYERS (state, layersArray) {
      each(layersArray, (obj) => {
        obj.visible = false
        obj.legendURL = process.env.WEB_HOST + ":8080/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=storyapp:" + obj.name + "&myData:" + Math.random()
        Vue.set(state.internalLayers, obj.name, obj)
      })
    },
    ADD_INTERNAL_LAYER (state, payload) {
      var obj = {
        name: payload.filename,
        visible: true,
        legendURL: process.env.WEB_HOST + ":8080/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=storyapp:" + payload.filename + "&myData:" + Math.random(),
        geomtype: ['POINT', 'MULTIPOINT'].includes(payload.geomtype) ? 0 : ['LINESTRING', 'MULTILINESTRING'].includes(payload.geomtype) ? 1 : ['POLYGON', 'MULTIPOLYGON'].includes(payload.geomtype) ? 2 : 3,
        assigned_name: null
      }
      Vue.set(state.internalLayers, payload.filename, obj) // so the new property is also reactive
    },
    DELETE_INTERNAL_LAYER (state, layername) {
      Vue.delete(state.internalLayers, layername)
    },
    RENAME_INTERNAL_LAYER (state, payload) {
      state.internalLayers[payload.layername].assigned_name = payload.assignedName
    },
    SET_MAP_RESOLUTION (state, resolution) {
      state.map_resolution = resolution
    },
    SET_MAP_ZOOM (state, zoom) {
      state.map_zoom = zoom
    },
    SET_PANEL_OPEN (state, open) {
      state.isPanelOpen = open
      EventBus.$emit('adjustMap', 10)
    },
    SET_STORIES (state, response) {
      state.stories = response.body
    },
    SET_STORY_CONTENT (state, response) {
      state.storyContent = response
    },
    // Generic fail handling
    API_FAIL (state, error) {
      if (error.status === 401 || error.status === 403) {
        console.error("Authentication error found. Logging user out.")
        // store.commit("DEAUTHENTICATE")
      } else {
        console.error(error)
      }
    }
  },
  getters: {
    flavor: state => state.flavor
  },
  actions: {
    uploadFile (store, datafile) {
      return api.post(apiRoot + '/upload_file/', datafile)
        .then((response) => {
          return response
        })
        .catch((error) => {
          store.commit('API_FAIL', error)
          return error
        })
    },
    getDatasets (store) {
      return api.get(apiRoot + '/datasets/')
      .then((response) => {
        store.commit('SET_INTERNAL_LAYERS', response.body)
      })
    },
    getInternalLayerStyle (store, layername) {
      return api.get(apiRoot + '/get_layer_style/?layername=' + layername)
      .then((response) => {
        return response
      })
    },
    setInternalLayerStyle (store, payload) {
      return api.post(apiRoot + '/set_layer_style/', payload)
      .then((response) => {
        return response
      })
    },
    deleteLayer (store, layername) {
      return api.post(apiRoot + '/delete_layer/', {'layername': layername})
      .then(() => {
        store.commit('DELETE_INTERNAL_LAYER', layername)
      })
    },
    renameLayer (store, payload) {
      return api.post(apiRoot + '/rename_layer/', payload)
      .then(() => {
        store.commit('RENAME_INTERNAL_LAYER', payload)
      })
    },
    getInternalRasterLayerBbox (store, layername) {
      return api.get(apiRoot + '/get_layer_bbox/?layername=' + layername)
      .then((response) => {
        return response
      })
    },
    getStories () {
      // To be filtered in the future based on the stories that the public/user has access
      return api.get(apiRoot + '/stories')
        .then((response) => store.commit('SET_STORIES', response))
        // .catch((error) => store.commit('API_FAIL', error))
    },
    getStoryContent (store, storyid) {
      // Add auth headers to the request in the future
      var story_content = {}
      return api.get(apiRoot + '/stories/' + storyid + '/')
        .then((response) => {
          story_content.content = response.body
          return api.get(apiRoot + '/story_geoms_attrb/?story_id=' + storyid)
            .then((response) => {
              story_content.geoms = response.body
              console.log(story_content)
              store.commit('SET_STORY_CONTENT', story_content)
            })
        })
        // .catch((error) => store.commit('API_FAIL', error))
    },
    saveStoryContent (store, storyContent) {
      return api.patch(apiRoot + '/stories/' + storyContent.content.id + '/', storyContent.content)
        .then((response) => {
          console.log(response)
        })
    }
  }
})

export default store
