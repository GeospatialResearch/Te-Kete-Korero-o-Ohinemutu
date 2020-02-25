import Vue from 'vue'
import Vuex from 'vuex'
import api from './api.js'
import { EventBus } from './event-bus'
import { each, some, isEmpty } from 'underscore'
import { info as notifyInfo, close as notifyClose } from 'utils/notify'
import signup from './signup'
import router from '../router'

Vue.use(Vuex)

const apiRoot = process.env.API_HOST + '/v1'

var getAuthHeader = function () {
  var authToken = localStorage.getItem('token')
  var authHeader
  if (authToken !== undefined && authToken !== null) {
    authHeader = {
      'Authorization': 'JWT ' + authToken // rest-auth with jwt enabled (REST_USE_JWT = True in settings.py)
      // 'Authorization': 'Token ' + authToken // rest-auth token (REST_USE_JWT = False in settings.py)
    }
  }
  return authHeader
}

var getData = function () {
  store.dispatch('getDatasets')
  store.dispatch('getStories')
  store.dispatch('getAtuas'),
  store.dispatch('getStoryTypes'),
  store.dispatch('getElementContentTypes'),
  store.dispatch('getWebsiteTranslation')
}

const initialState = {
  flavor: '',
  map: null,
  isLoading: false,
  isUploadingData: false,
  isPanelOpen: false,
  contentToShow: 'welcome',
  externalLayers: null,
  internalLayers: {},
  allStoriesGeomsLayer: {
    visible: true,
    name: 'allStoriesGeomsLayer',
    layername: 'Geometries in Narratives',
    style: null,
    allUsedStoriesGeometries: null,
    allUsedStoriesGeometriesObj: null
  },
  map_resolution: 0,
  map_zoom: 0,
  stories: [],
  storyContent: {
    titleeng : '',
    titlemao : '',
    summaryeng : '',
    summarymao : '',
    status: 'DRAFT',
    storyBodyElements: [],
    atua: [],
    story_type_id: '',
    approx_time: {
      type: '',
      date: null,
      start_time: null,
      end_time: null,
      year: null
    }
  },
  uploadMediaProgress: 0,
  drawMode: false,
  storyViewMode: true,
  geomMediaMode: false,
  reuseMode: false,
  featuresForReuse: [],
  websiteTranslObj: null,
  lang: 'eng',
  storyViewLang: 'eng',
  allAtuas: [],
  allStoryTypes: [],
  allElementContentTypes: [],
  isMobile: false,
  hitTolerance: 0,
  // User related attributes
  token: null, // (used for jwt or rest-auth token),
  authenticated: false,
  user: null,
  orientation: null
}

const store = new Vuex.Store({
  modules: {
    signup
  },
  state: $.extend(true, {}, initialState),
  mutations: {
    CHANGE (state, flavor) {
      state.flavor = flavor
    },
    // Map related functions
    SET_MAP (state, map) {
      state.map = map
    },
    SET_LOADING (state, value) {
      state.isLoading = value
    },
    SET_ORIENTATION(state, content) {
      state.orientation = content
    },
    TOGGLE_CONTENT (state, content) {
      state.contentToShow = content
      if (state.contentToShow != 'map') {
        EventBus.$emit('closePanel')
      }
    },
    SET_EXTERNAL_LAYERS (state, layersObj) {
      state.externalLayers = layersObj
    },
    SET_INTERNAL_LAYERS (state, layersArray) {
      each(layersArray, (obj) => {
        obj.visible = false
        obj.legendURL = process.env.GEOSERVER_HOST + "/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=storyapp:" + obj.name + "&myData:" + Math.random()
        Vue.set(state.internalLayers, obj.name, obj)
      })
    },
    ADD_INTERNAL_LAYER (state, payload) {
      var obj = {
        name: payload.filename,
        visible: true,
        legendURL: process.env.GEOSERVER_HOST + "/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=storyapp:" + payload.filename + "&myData:" + Math.random(),
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
      EventBus.$emit('scrollStoryTop')
    },
    SET_STORIES (state, response) {
      state.stories = response.body
    },
    SET_ALLATUAS (state, response) {
      state.allAtuas = response.body
    },
    SET_ALLSTORYTYPES (state, response) {
      state.allStoryTypes = response.body
    },
    SET_ALL_ELEMENT_CONTENTTYPES (state, response) {
      state.allElementContentTypes = response.body
    },
    SET_STORY_CONTENT (state, response) {
      // Sort the storyBodyElements array by attribute order_position
      response.storyBodyElements.sort((a, b) => parseFloat(a.order_position) - parseFloat(b.order_position))
      each(response.storyBodyElements, el =>{
        if (el.element_type === 'TEXT')
        {
          el.texteng = el.text.eng
          el.textmao = el.text.mao
        }
        if (el.element_type !== 'TEXT' && el.element_type !== 'GEOM')
        {
          el.tempMediaDescriptionEng = el.media_description.eng
          el.tempMediaDescriptionMao = el.media_description.mao
        }
      })
      response['titleeng']= response.title.eng
      response['titlemao']= response.title.mao
      response['summaryeng']= response.summary.eng
      response['summarymao']= response.summary.mao
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
        storyBodyElements: [],
        atua: [],
        story_type_id: '',
        approx_time: {
          type: '',
          date: null,
          start_time: null,
          end_time: null
        }
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
    SET_STORY_VIEW_LANG(state, value) {
      state.storyViewLang = value
    },
    SET_ALL_USEDSTORIESGEOMETRIES (state, payload) {
      state.allStoriesGeomsLayer.allUsedStoriesGeometriesObj = payload.allusedgeomsObj
      state.allStoriesGeomsLayer.allUsedStoriesGeometries = payload.allusedgeoms
      EventBus.$emit('createLayer', state.allStoriesGeomsLayer.allUsedStoriesGeometries, 'allstoriesgeoms')
    },
    RESTORE_ALL_USEDSTORIESGEOMETRIES (state) {
      EventBus.$emit('createLayer', state.allStoriesGeomsLayer.allUsedStoriesGeometries, 'allstoriesgeoms')
    },
    SET_UPLOADMEDIA_PROGRESS (state, value) {
      if (value == 100) {
        state.uploadMediaProgress = 99.9
      } else {
        state.uploadMediaProgress = value
      }

    },
    // Account system
    SET_LOGIN (state, response) {
      if (!isEmpty(response.body)) {
        state.user = response.body.user
        if (response.body.hasOwnProperty('token')) {
          state.token = response.body.token // rest-auth jwt
          localStorage.setItem('token', response.body.token)
        } else if (response.body.hasOwnProperty('key')) {
          state.token = response.body.key // rest-auth token
          localStorage.setItem('token', response.body.key)
        }
        state.authenticated = true
        // store.dispatch('checkAdmin')
      }
    },
    DEAUTHENTICATE (state) {
      localStorage.removeItem('token')
      state.authenticated = false
      state.user = null
      state.token = null
      state.storyViewMode = false
      state.drawMode = false
      state.geomMediaMode = false
      EventBus.$emit('closePanel')

      // Reset state to initial values
      // for (const f in state) {
      //   console.log(f, initialState[f])
      //   Vue.set(state, f, initialState[f])
      // }
    },
    // Generic fail handling
    API_FAIL (state, error) {
      if (error.status === 401 || error.status === 403) {
        console.log((error))
        console.error("Authentication error found. Logging user out.")
        store.commit("DEAUTHENTICATE")
        getData()
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
      return api.post(apiRoot + '/upload_file/', datafile, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => {
          store.commit('API_FAIL', error)
          return error
        })
    },
    getDatasets (store) {
      return api.get(apiRoot + '/datasets/', { headers: getAuthHeader() })
        .then((response) => {
          store.commit('SET_INTERNAL_LAYERS', response.body)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    getInternalLayerStyle (store, layername) {
      return api.get(apiRoot + '/get_layer_style/?layername=' + layername, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    setInternalLayerStyle (store, payload) {
      return api.post(apiRoot + '/set_layer_style/', payload, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    deleteLayer (store, layername) {
      return api.post(apiRoot + '/delete_layer/', {'layername': layername}, { headers: getAuthHeader() })
        .then(() => {
          store.commit('DELETE_INTERNAL_LAYER', layername)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    renameLayer (store, payload) {
      return api.post(apiRoot + '/rename_layer/', payload, { headers: getAuthHeader() })
        .then(() => {
          store.commit('RENAME_INTERNAL_LAYER', payload)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    getInternalRasterLayerBbox (store, layername) {
      return api.get(apiRoot + '/get_layer_bbox/?layername=' + layername, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    getStories () {
      // To be filtered in the future based on the stories that the public/user has access
      return api.get(apiRoot + '/stories', { headers: getAuthHeader() })
      .then((response) => {
        store.commit('SET_STORIES', response)
        store.dispatch('getAllUsedStoriesGeometries')
      })
      .catch((error) => store.commit('API_FAIL', error))
    },
    getAtuas () {
      // To getall atuas
      return api.get(apiRoot + '/atuas', { headers: getAuthHeader() })
        .then((response) => {
          store.commit('SET_ALLATUAS', response)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    getStoryTypes () {
      // To getall storytypes
      return api.get(apiRoot + '/storytypes', { headers: getAuthHeader() })
        .then((response) => {
          store.commit('SET_ALLSTORYTYPES', response)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    getElementContentTypes () {
      // To getall contenttypes
      return api.get(apiRoot + '/contenttypes', { headers: getAuthHeader() })
        .then((response) => {
          store.commit('SET_ALL_ELEMENT_CONTENTTYPES', response)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    getStoryContent (store, storyid) {
      return api.get(apiRoot + '/stories/' + storyid + '/', { headers: getAuthHeader() })
        .then((response) => {
          if (response.body.story_type) {
            response.body.story_type_id = response.body.story_type.id
          }
          store.commit('SET_STORY_CONTENT', response.body)
          return response.body
          })
        .catch((error) => store.commit('API_FAIL', error))
    },
    getWebsiteTranslation () {
      return api.get(apiRoot + '/websitetranslation/', { headers: getAuthHeader() })
        .then((response) => {
          var result = {}
          response.body.forEach(function(item) {
            result[item.field_name]=item
          })
          store.commit('SET_TRANSLATION', result)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    saveStoryContent (store, story) {
      each(story.storyBodyElements, el =>{
        if (el.element_type === 'TEXT')
        {
          el.text = {
            eng: el.texteng,
            mao: el.textmao,
          }
          delete el['texteng']
          delete el['textmao']
        }
        if (el.element_type !== 'TEXT' && el.element_type !== 'GEOM')
        {
          delete el['tempMediaDescriptionEng']
          delete el['tempMediaDescriptionMao']
        }
      })
      story.storyBodyElements_temp = story.storyBodyElements
      delete story['storyBodyElements']
      story.atua_temp = story.atua
      story.title = {
        eng: story.titleeng,
        mao: story.titlemao,
      }
      story.summary = {
        eng: story.summaryeng,
        mao: story.summarymao,
      }
      delete story['atua']
      delete story['titleeng']
      delete story['titlemao']
      delete story['summaryeng']
      delete story['summarymao']

      return api.patch(apiRoot + '/stories/' + story.id + '/', story, { headers: getAuthHeader() })
        .then((response) => {
          store.dispatch('getStories')
          store.commit('SET_STORY_CONTENT', response.body)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    addStory (store, story) {
      each(story.storyBodyElements, el =>{
        if (el.element_type === 'TEXT')
        {
          el.text = {
            eng: el.texteng,
            mao: el.textmao,
          }
          delete el['texteng']
          delete el['textmao']
        }
      })
      story.storyBodyElements_temp = story.storyBodyElements
      delete story['storyBodyElements']
      story.atua_temp = story.atua
      story.title = {
        eng: story.titleeng,
        mao: story.titlemao
      }
      story.summary = {
        eng: story.summaryeng,
        mao: story.summarymao
      }
      delete story['atua']
      delete story['titleeng']
      delete story['titlemao']
      delete story['summaryeng']
      delete story['summarymao']
      return api.post(apiRoot + '/stories/', story, { headers: getAuthHeader() })
        .then((response) => {
          store.dispatch('getStories')
          store.commit('SET_STORY_CONTENT', response.body)
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    addMedia (store, media) {
      return api.post(apiRoot + '/upload_media_file/', media, {
        progress(e) {
          if (e.lengthComputable) {
            store.commit('SET_UPLOADMEDIA_PROGRESS', Math.trunc(e.loaded / e.total * 100))
          }
        },
        headers: { 'Content-Type': 'multipart/form-data',
                  'Authorization': 'JWT ' + localStorage.getItem('token') }
      })
        .then((response) => {
          return response
        })
        .catch((error) => {
          return error
        })
    },
    deleteStoryBodyElement (store, element) {
      return api.delete(apiRoot + '/storybodyelements/' + element.id + '/', { headers: getAuthHeader() })
        .then(() => store.commit('DELETE_ELEMENT', element))
        .catch((error) => store.commit('API_FAIL', error))
    },
    deleteUnusedMediaFiles () {
      return api.post(apiRoot + '/delete_unused_media/', {}, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    deleteUnusedGeomAttrs () {
      return api.post(apiRoot + '/delete_unused_geoms/', {}, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    deleteStory (store, storyid) {
      return api.delete(apiRoot + '/stories/' + storyid + '/', { headers: getAuthHeader() })
      .then(() => {
        store.dispatch('getStories')
        store.dispatch('deleteUnusedMediaFiles')
      })
      .catch((error) => store.commit('API_FAIL', error))
    },
    addGeometryAttrb (store, drawnfeature) {
      if (drawnfeature.geometry.geometry) {
        drawnfeature.geometry = drawnfeature.geometry.geometry
      }
      return api.post(apiRoot + '/storygeomsattrib/', drawnfeature, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    updateGeometryAttrb (store, drawnfeature) {
      if (drawnfeature.geometry.geometry) {
        drawnfeature.geometry = drawnfeature.geometry.geometry
      }
      return api.patch(apiRoot + '/storygeomsattrib/' + drawnfeature.id + '/', drawnfeature, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    addGeometryAttrbMedia (store, geomAttrMedia) {
      geomAttrMedia.mediafile_temp = geomAttrMedia.mediafile
      geomAttrMedia.geomattr_temp = geomAttrMedia.geom_attr
      delete geomAttrMedia['mediafile']
      delete geomAttrMedia['geom_attr']
      return api.post(apiRoot + '/storygeomsattribmedia/', geomAttrMedia, { headers: getAuthHeader() })
        .then((response) => {
          return response
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    updateGeometryAttrbMediaCaptions (store, geomAttrMediaFiles) {
      each(geomAttrMediaFiles, geomAttrMedia => {
        return api.patch(apiRoot + '/storygeomsattribmedia/' + geomAttrMedia.id + '/', geomAttrMedia, { headers: getAuthHeader() })
      })
    },
    deleteGeometryAttrbMedia (store, geomAttrMedia) {
      return api.delete(apiRoot + '/storygeomsattribmedia/' + geomAttrMedia.id + '/', { headers: getAuthHeader() })
    },
    getAllUsedStoriesGeometries () {
      api.get(apiRoot + '/storybodyelements', { headers: getAuthHeader() })
        .then((response) => {
          var allUsedGeoms = []
          var allUsedGeomsObj = {}
          response.body.forEach((elem) => {
            if (elem.element_type === 'GEOM') {
              allUsedGeoms.push(elem.geom_attr)
              allUsedGeomsObj[elem.geom_attr.id] = {'geomAttr': elem.geom_attr,
                                                    'story': {
                                                      'id': elem.story.id,
                                                      'title': elem.story.title,
                                                      'summary': elem.story.summary,
                                                      'storytype': elem.story.story_type.type
                                                    }
                                                  }
            }
          })
          store.commit('SET_ALL_USEDSTORIESGEOMETRIES', {'allusedgeoms': allUsedGeoms, 'allusedgeomsObj': allUsedGeomsObj})
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    // getGeometryUsage (store, geomAttr) {
    //   var storyDetail
    //   return api.get(apiRoot + '/storybodyelements/?geomattr=' + geomAttr.id, { headers: getAuthHeader() })
    //   .then((response) => {
    //     if (response.body[0]) {
    //       storyDetail = {
    //         'id': response.body[0].story.id,
    //         'title': response.body[0].story.title,
    //         'summary': response.body[0].story.summary,
    //         'storytype': response.body[0].story.story_type.type,
    //       }
    //       return storyDetail
    //     } else {
    //       return null
    //     }
    //
    //   })
    // },

    // Login using rest-auth with or without jwt enabled (the response brings a generated jwt or the token stored in db)
    logIn (store, payload) {
      return api.post(process.env.API_HOST + '/auth/login/', payload)
        .then((response) => {
          store.commit('SET_LOGIN', response)
          getData()
          router.push('/')
          store.commit('TOGGLE_CONTENT', 'map')
          return response
        })
        .catch((error) => {
          return error
        })
    },
    logOut () {
      store.commit('DEAUTHENTICATE')
      getData()
      store.commit('TOGGLE_CONTENT', 'welcome')
    },
    getUser (store) {
      // To check the token validation
      return api.get(apiRoot + '/check_user/', { headers: getAuthHeader() })
        .then( (response) => {
          store.commit('SET_LOGIN', response)
          getData()
        })
        .catch((error) => store.commit('API_FAIL', error))
    },
    addComment (store, comment) {
      return api.post(apiRoot + '/comments/', comment, { headers: getAuthHeader() })
        .then(() => {
          store.dispatch('getStoryContent', comment.story)
        })
        .catch((error) => store.commit('API_FAIL', error))
    }
  }
})

export default store
