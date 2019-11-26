import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'
import { EventBus } from './event-bus'
import { each, some } from 'underscore'
import { info as notifyInfo, close as notifyClose } from 'utils/notify'

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
    storyContent: {
      title : '',
      summary : '',
      status: 'DRAFT',
      storyBodyElements: []
    },
    drawMode: false,
    storyViewMode: true,
    geomMediaMode: false,
    reuseMode: false,
    featuresForReuse: [],
    websiteTranslObj: null,
    lang: 'eng',
    allUsedStoriesGeometries: null,
    allUsedStoriesGeometriesObj: null
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
      // Sort the storyBodyElements array by attribute order_position
      response.storyBodyElements.sort((a, b) => parseFloat(a.order_position) - parseFloat(b.order_position))
      state.storyContent = response
    },
    SET_STORY_VIEW_MODE (state, mode){
      state.storyViewMode = mode
    },
    SET_DRAW_MODE (state, mode){
      state.drawMode = mode
    },
    SET_REUSE_MODE (state, mode){
      state.featuresForReuse = []
      state.reuseMode = mode
      if (mode) {
        notifyInfo("<div class='text-center'><i class='fa fa-info-circle' /><strong>&nbsp;&nbsp;Click in any geometry on the map to reuse it in the narrative.</strong></div>")
      } else {
        notifyClose()
      }
    },
    SET_GEOM_MEDIA_MODE (state, mode) {
      state.geomMediaMode = mode
    },
    RESET_STORY_FORM (state) {
      state.storyContent = {
        title : '',
        summary : '',
        status: 'DRAFT',
        storyBodyElements: []
      }
    },
    ADD_FEATURES_FOR_REUSE (state, f) {
      if (Array.isArray(f)) {
        state.featuresForReuse = state.featuresForReuse.concat(f)
      } else {
        state.featuresForReuse.push(f)
      }
    },
    DELETE_ELEMENT (state, element) {
      const elements = state.storyContent.storyBodyElements
      some(state.storyContent.storyBodyElements, function (el, i) {
        if (el.id === element.id) {
          elements.splice(i, 1)
          return true
        }
      })
    },
    SET_TRANSLATION (state, translObj) {
      state.websiteTranslObj = translObj
    },
    SET_LANG (state, value) {
      state.lang = value
    },
    SET_ALL_USEDSTORIESGEOMETRIES (state, payload) {
      state.allUsedStoriesGeometriesObj = payload.allusedgeomsObj
      state.allUsedStoriesGeometries = payload.allusedgeoms
      EventBus.$emit('createLayer', state.allUsedStoriesGeometries, 'allstoriesgeoms')
    },
    RESTORE_ALL_USEDSTORIESGEOMETRIES (state) {
      EventBus.$emit('createLayer', state.allUsedStoriesGeometries, 'allstoriesgeoms')
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
      .then((response) => {
        store.commit('SET_STORIES', response)
        store.dispatch('getAllUsedStoriesGeometries')
      })
        // .catch((error) => store.commit('API_FAIL', error))
    },
    getStoryContent (store, storyid) {
      // Add auth headers to the request in the future
      return api.get(apiRoot + '/stories/' + storyid + '/')
        .then((response) => {
          store.commit('SET_STORY_CONTENT', response.body)
          return response.body
          })
        // .catch((error) => store.commit('API_FAIL', error))
    },
    saveStoryContent (store, story) {
      story.storyBodyElements_temp = story.storyBodyElements
      delete story['storyBodyElements']
      return api.patch(apiRoot + '/stories/' + story.id + '/', story)
        .then((response) => {
          store.dispatch('getStories')
          store.commit('SET_STORY_CONTENT', response.body)
        })
    },
    addStory (store, story) {
      story.storyBodyElements_temp = story.storyBodyElements
      delete story['storyBodyElements']
      return api.post(apiRoot + '/stories/', story)
        .then((response) => {
          store.dispatch('getStories')
          store.commit('SET_STORY_CONTENT', response.body)
        })
    },
    addMedia (store, media) {
      return api.post(apiRoot + '/upload_media_file/', media, {
        progress(e) {
          if (e.lengthComputable) {
            console.log(e.loaded / e.total * 100);
          }
        }
      })
        .then((response) => {
          return response
        })
        .catch((error) => {
          return error
        })
    },
    deleteStoryBodyElement (store, element) {
      return api.delete(apiRoot + '/storybodyelements/' + element.id + '/')
        .then(() => store.commit('DELETE_ELEMENT', element))
        // .catch((error) => store.commit('API_FAIL', error))
    },
    deleteUnusedMediaFiles () {
      return api.post(apiRoot + '/delete_unused_media/')
        .then((response) => {
          return response
        })
    },
    deleteUnusedGeomAttrs () {
      return api.post(apiRoot + '/delete_unused_geoms/')
        .then((response) => {
          return response
        })
    },
    deleteStory (store, storyid) {
      return api.delete(apiRoot + '/stories/' + storyid + '/')
      .then(() => {
        store.dispatch('getStories')
        store.dispatch('deleteUnusedMediaFiles')
      })
    },
    addGeometryAttrb (store, drawnfeature) {
      drawnfeature.geom_temp = drawnfeature.geometry
      delete drawnfeature['geometry']
      return api.post(apiRoot + '/storygeomsattrib/', drawnfeature)
        .then((response) => {
          return response
        })
    },
    updateGeometryAttrb (store, drawnfeature) {
      drawnfeature.geom_temp = drawnfeature.geometry
      delete drawnfeature['geometry']
      return api.patch(apiRoot + '/storygeomsattrib/' + drawnfeature.id + '/', drawnfeature)
        .then((response) => {
          return response
        })
    },
    addGeometryAttrbMedia (store, geomAttrMedia) {
      geomAttrMedia.mediafile_temp = geomAttrMedia.mediafile
      geomAttrMedia.geomattr_temp = geomAttrMedia.geom_attr
      delete geomAttrMedia['mediafile']
      delete geomAttrMedia['geom_attr']
      return api.post(apiRoot + '/storygeomsattribmedia/', geomAttrMedia)
        .then((response) => {
          return response
        })
    },
    updateGeometryAttrbMediaCaptions (store, geomAttrMediaFiles) {
      each(geomAttrMediaFiles, geomAttrMedia => {
        return api.patch(apiRoot + '/storygeomsattribmedia/' + geomAttrMedia.id + '/', geomAttrMedia)
      })
    },
    deleteGeometryAttrbMedia (store, geomAttrMedia) {
      return api.delete(apiRoot + '/storygeomsattribmedia/' + geomAttrMedia.id + '/')
    },
    getWebsiteTranslation () {
      return api.get(apiRoot + '/websitetranslation/')
        .then((response) => {
          var result = {}
          response.body.forEach(function(item) {
            result[item.field_name]=item
          })
          store.commit('SET_TRANSLATION', result)
        })
        // .catch((error) => store.commit('API_FAIL', error))
    },
    getAllUsedStoriesGeometries (store) {
      api.get(apiRoot + '/storygeometries')
        .then((response) => {
          var allUsedGeoms = []
          var allUsedGeomsObj = {}
          var count = 0
          var totalGeoms = response.body.features
          totalGeoms.forEach((geom) => {
            store.dispatch('getGeometryUsage', geom.id)
            .then((response) => {
              count++
              if (response) {
                geom['usage'] = response
                allUsedGeoms.push(geom)
                allUsedGeomsObj[geom.id] = response // geomAttr and story
              }
              if (count === totalGeoms.length) {
                store.commit('SET_ALL_USEDSTORIESGEOMETRIES', {'allusedgeoms': allUsedGeoms, 'allusedgeomsObj': allUsedGeomsObj})
                return
              }
            })
          })
        })
        // .catch((error) => store.commit('API_FAIL', error))
    },
    getGeometryUsage (store, geomId) {
      var geomUsage = {
        'geomAttr': null,
        'story': null
      }
      return api.get(apiRoot + '/storygeomsattrib/?geom=' + geomId)
      .then((response) => {
        // forEach storygeomattr
        geomUsage['geomAttr'] = response.body[0]
        return api.get(apiRoot + '/storybodyelements/?geomattr=' + response.body[0].id)
        .then((response) => {
          if (response.body[0]) {
            geomUsage['story'] = {
              'id': response.body[0].story.id,
              'title': response.body[0].story.title,
              'summary': response.body[0].story.summary
            }
            return geomUsage
          } else {
            return null
          }

        })
      })
    }
  }
})

export default store
