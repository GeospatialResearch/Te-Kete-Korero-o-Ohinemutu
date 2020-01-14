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
var getWidth = require('ol/extent').getWidth
var Feature = require('ol/Feature').default
var Polygon = require('ol/geom/Polygon').default
const VectorSource = require('ol/source/Vector').default
const VectorLayer = require('ol/layer/Vector').default

// TODO: get the domain and workspace name through variables

var addGeoserverWMS = function (layername) {
  const map = store.state.map
  store.commit('SET_LOADING', true)

  var layerWMS = new ImageLayer({
    name: layername,
    zIndex: 20,
    source: new ImageWMS({
      url: process.env.GEOSERVER_HOST + '/storyapp/wms',
      params: {'LAYERS': 'storyapp:' + layername },
      ratio: 1,
      serverType: 'geoserver'
    })
  })
  map.addLayer(layerWMS)

  EventBus.$emit('refreshLayer', (layername))
  store.commit('SET_LOADING', false)
}

var zoomToGeoserverVectorLayer = function (layername) {
  const map = store.state.map
  store.commit('SET_LOADING', true)

  $.ajax( process.env.GEOSERVER_HOST + '/wfs', {
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
    store.commit('SET_LOADING', false)
  })
}

var zoomToGeoserverLayerBbox = function (layername) {
  const map = store.state.map
  store.commit('SET_LOADING', true)

  store.dispatch('getInternalRasterLayerBbox', layername)
  .then((response) => {
    console.log(response.body.bbox)
    var extentmin = transform([response.body.bbox[0], response.body.bbox[3]].map(Number), 'EPSG:4326', 'EPSG:3857')
    var extentmax = transform([response.body.bbox[1], response.body.bbox[2]].map(Number), 'EPSG:4326', 'EPSG:3857')
    var extentx = [extentmin[0], extentmax[0]].sort((a, b) => a - b) // For ascending sort
    var extenty = [extentmin[1], extentmax[1]].sort((a, b) => a - b) // For ascending sort

    var wrapWidth = getWidth(store.state.map.getView().getProjection().getExtent());
    function wrapTransform(input, opt_output, opt_dimension) {
      var length = input.length;
      var dimension = opt_dimension !== undefined ? opt_dimension : 2;
      var output = opt_output !== undefined ? opt_output : new Array(length);
      var i, j;
      for (i = 0; i < length; i += dimension) {
        output[i] = input[i] < 0 ? input[i] + wrapWidth : input[i];
        for (j = dimension - 1; j >= 1; --j) {
          output[i + j] = input[i + j];
        }
      }
      return output;
    }

    var polygon = new Polygon([[
                  [extentx[0], extenty[1]],
                  [extentx[1], extenty[1]],
                  [extentx[0], extenty[0]],
                  [extentx[1], extenty[0]]
                ]])

    var feature = new Feature(polygon)

    var tempLayer = new VectorLayer({
      source: new VectorSource({
        features: [feature]
      })
    })

    tempLayer.getSource().forEachFeature(function(feature){
      feature.getGeometry().applyTransform(wrapTransform)
    })

    map.getView().fit(tempLayer.getSource().getExtent(), { duration: 2000 })
    store.commit('SET_LOADING', false)
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

module.exports = { addGeoserverWMS, zoomToGeoserverVectorLayer, zoomToGeoserverLayerBbox, setSLDstyle }
