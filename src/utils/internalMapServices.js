const store = require('store').default
var ImageLayer = require('ol/layer').Image
var ImageWMS = require('ol/source/ImageWMS').default

var getCorrectExtent = require('utils/mapUtils').getCorrectExtent

// TODO: get the domain and workspace name through variables

var addGeoserverWMS = function (layername) {
  const map = store.state.map

  var layerWMS = new ImageLayer({
    name: layername,
    source: new ImageWMS({
      url: 'http://localhost:8080/geoserver/storyapp/wms',
      params: {'LAYERS': 'storyapp:' + layername },
      ratio: 1,
      serverType: 'geoserver',
    })
  })
  map.addLayer(layerWMS)
}

var zoomToGeoserverLayer = function (layername) {
  const map = store.state.map

  $.ajax('http://localhost:8080/geoserver/wfs', {
      type: 'GET',
      data: {
          service: 'WFS',
          version: '1.1.0',
          request: 'GetFeature',
          typename: 'storyapp:' + layername,
          srsname: 'EPSG:3857',
          outputFormat: 'text/javascript',
          format_options: 'callback:getJson'
      },
      dataType: 'jsonp',
      jsonpCallback:'getJson'
  }).done(function (response) {
      var vectorExtent =  getCorrectExtent(response)
      map.getView().fit(vectorExtent, { duration: 2000 })
  })
}

module.exports = { addGeoserverWMS, zoomToGeoserverLayer }
