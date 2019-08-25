const store = require('store').default
var EventBus = require('store/event-bus.js').EventBus
var ImageLayer = require('ol/layer').Image
var ImageWMS = require('ol/source/ImageWMS').default

var getCorrectExtent = require('utils/mapUtils').getCorrectExtent
const generatePointSLD = require('utils/sld').generatePointSLD
const generateLineSLD = require('utils/sld').generateLineSLD
const generatePolygonSLD = require('utils/sld').generatePolygonSLD

// TODO: get the domain and workspace name through variables

var addGeoserverWMS = function (layername) {
  const map = store.state.map

  var layerWMS = new ImageLayer({
    name: layername,
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

var zoomToGeoserverLayer = function (layername) {
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
      var vectorExtent =  getCorrectExtent(response)
      map.getView().fit(vectorExtent, { duration: 2000 })
      store.state.isLoading = false
  })
}

var setSLDstyle = function (styleObj) {
  $.ajax( process.env.WEB_HOST + ':8080/geoserver/ows', {
    type: 'GET',
    data: {
        service: 'WFS',
        version: '1.1.0',
        request: 'getFeature',
        maxfeatures: 1,
        typename: 'storyapp:' + styleObj.layername,
        outputFormat: 'text/javascript',
        format_options: 'callback:getJson'
    },
    dataType: 'jsonp',
    jsonpCallback:'getJson'
  }).done(function (response) {
    var sld
    if (response.features[0].geometry.type == "MultiPoint") {
      sld = generatePointSLD(styleObj)
    } else if (response.features[0].geometry.type == "MultiLineString") {
      sld = generateLineSLD(styleObj)
    } else if (response.features[0].geometry.type == "MultiPolygon") {
      sld = generatePolygonSLD(styleObj)
    }

    store.dispatch('setInternalLayerStyle', {'layername': styleObj.layername, 'sld': sld})
    .then(() => {
      EventBus.$emit('refreshLayer', styleObj.layername)
    })
  })
}

module.exports = { addGeoserverWMS, zoomToGeoserverLayer, setSLDstyle }
