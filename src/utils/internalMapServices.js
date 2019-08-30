const store = require('store').default
var EventBus = require('store/event-bus.js').EventBus
var ImageLayer = require('ol/layer').Image
var ImageWMS = require('ol/source/ImageWMS').default
var transform = require('ol/proj').transform
var getCorrectExtent = require('utils/mapUtils').getCorrectExtent
const generatePointSLD = require('utils/sld').generatePointSLD
const generateLineSLD = require('utils/sld').generateLineSLD
const generatePolygonSLD = require('utils/sld').generatePolygonSLD
const generateRasterSLD = require('utils/sld').generateRasterSLD

// TODO: get the domain and workspace name through variables

var addGeoserverWMS = function (layername) {
  const map = store.state.map

  var layerWMS = new ImageLayer({
    name: layername,
    zIndex: 10,
    source: new ImageWMS({
      url: process.env.WEB_HOST + ':8080/geoserver/storyapp/wms',
      params: {'LAYERS': 'storyapp:' + layername },
      ratio: 1,
      serverType: 'geoserver'
    })
  })
  map.addLayer(layerWMS)

  EventBus.$emit('refreshLayer', (layername))
}

var zoomToGeoserverVectorLayer = function (layername) {
  const map = store.state.map
  store.state.isLoading = true

  $.ajax( process.env.WEB_HOST + ':8080/geoserver/wfs', {
    type: 'GET',
    data: {
        service: 'WFS',
        version: '1.1.0',
        request: 'GetFeature',
        typename: 'storyapp:' + layername,
        srsname: 'EPSG:3857',
        outputFormat: 'text/javascript',
        format_options: 'callback:getJson',
        myData: Math.random()
        // The key myData will be URL encoded into the request sent to the WMS provider and the request is now changed due to the new value of myData.
        // This doesn't clear the cache, but it tells the browser that the request is different from the one it previously cached.
    },
    dataType: 'jsonp',
    jsonpCallback:'getJson'
  }).done(function (response) {
    var vectorExtent = getCorrectExtent(response)
    map.getView().fit(vectorExtent, { duration: 2000 })
    store.state.isLoading = false
  })
}

var zoomToGeoserverRasterLayer = function (layername) {
  const map = store.state.map
  store.state.isLoading = true

  store.dispatch('getInternalRasterLayerBbox', layername)
  .then((response) => {
    var extentmin = transform([response.body.bbox[0], response.body.bbox[3]].map(Number), 'EPSG:4326', 'EPSG:3857')
    var extentmax = transform([response.body.bbox[1], response.body.bbox[2]].map(Number), 'EPSG:4326', 'EPSG:3857')
    var extentx = [extentmin[0], extentmax[0]].sort((a, b) => a - b) // For ascending sort
    var extenty = [extentmin[1], extentmax[1]].sort((a, b) => a - b) // For ascending sort
    map.getView().fit([extentx[0], extenty[0], extentx[1], extenty[1]], { duration: 2000 })
    store.state.isLoading = false
  })

}

var setSLDstyle = function (styleObj) {
  var sld
  if (store.state.internalLayers[styleObj.layername].geomtype === 0) {
    sld = generatePointSLD(styleObj)
  } else if (store.state.internalLayers[styleObj.layername].geomtype === 1) {
    sld = generateLineSLD(styleObj)
  } else if (store.state.internalLayers[styleObj.layername].geomtype === 2) {
    sld = generatePolygonSLD(styleObj)
  } else {
    sld = generateRasterSLD(styleObj)
  }

  store.dispatch('setInternalLayerStyle', {'layername': styleObj.layername, 'sld': sld})
  .then(() => {
    EventBus.$emit('refreshLayer', styleObj.layername)
  })
}

module.exports = { addGeoserverWMS, zoomToGeoserverVectorLayer, zoomToGeoserverRasterLayer, setSLDstyle }
