const store = require('store').default
var EventBus = require('store/event-bus.js').EventBus
const Style = require('ol/style/Style').default
const Fill = require('ol/style/Fill').default
const Stroke = require('ol/style/Stroke').default
const CircleStyle = require('ol/style/Circle').default
const Text = require('ol/style/Text').default
const Projection = require('ol/proj/Projection').default
var createXYZ = require('ol/tilegrid').createXYZ
var geojsonvt = require('geojson-vt').default
const VectorSource = require('ol/source/Vector').default
const VectorLayer = require('ol/layer/Vector').default
const VectorTileSource = require('ol/source/VectorTile').default
const VectorTileLayer = require('ol/layer/VectorTile').default
const GeoJSON = require('ol/format/GeoJSON').default
var getWidth = require('ol/extent').getWidth
// var findByName = require('utils/olHelper').findByName
const extLayersObj = require('utils/objects').extLayersObj
var _ = require('underscore')


var singleClickCallbackFunction = function (evt) {
  const map = store.state.map
  EventBus.$emit('closeMapPopup')

  // Attempt to find a marker from the map layers
  var layers = map.getLayers()
  var viewResolution = map.getView().getResolution()
  var projection = map.getView().getProjection()

  // Define nExpectedCount
  var nExpectedCount = 0
  _.each(store.state.internalLayers, (layer) => {
    if (layer.visible) {
      nExpectedCount++
    }
  })
  map.forEachFeatureAtPixel(evt.pixel, (feature, layer) => {
    if (layer.get('name') !== 'storyGeomsLayer') {
      nExpectedCount++
    }
  })
  EventBus.$emit('defineExpectedCount', nExpectedCount)

  // External vector layers
  map.forEachFeatureAtPixel(evt.pixel, (feature, layer) => {
    if (extLayersObj[layer.get('name')]) {  // if the extLayersObj has this layer name (in order to exclude the name storyGeomsLayer)
      EventBus.$emit('showLayersFeaturesPopup', {
        'features': [feature],
        'coordinate': evt.coordinate,
        'layername': extLayersObj[layer.get('name')].layername
      })
    }
  })

  // Internal geoserser wms layers
  layers.forEach( (layer) => {
    var layername = layer.get('name')
    if (layer.getVisible() && !['Basemap', 'drawingLayer', 'storyGeomsLayer'].includes(layername) && !Object.keys(store.state.externalLayers).includes(layername)) {
      $.ajax({
        url: layer.getSource().getGetFeatureInfoUrl(evt.coordinate, viewResolution, projection,  // creates the WMS getFeatureInfo request for us
          { 'INFO_FORMAT': 'text/javascript',
            'format_options': 'callback:' + layername,
          }
        ),
        dataType: 'jsonp',
        jsonpCallback: layername // instead of a static name like 'getJson' to avoid the classic race issue
      }).done(function (response) {
        if (response.features.length > 0) {
          EventBus.$emit('showLayersFeaturesPopup', {
            'features': response.features,
            'coordinate': evt.coordinate,
            'layername': layername
          })
        } else {
          EventBus.$emit('showLayersFeaturesPopup', {
            'coordinate': evt.coordinate,
          })
        }
      })
    }
  })

  // Show storyGeomsLayer features info
  map.forEachFeatureAtPixel(evt.pixel, (feature, layer) => {
    if (layer.get('name') === 'storyGeomsLayer') {
      EventBus.$emit('getStoryGeomInfo', feature)
    }
  })

}


var enableEventListeners = function () {
  const map = store.state.map

  map.on('movestart', () => {
      EventBus.$emit('closeMapPopup')
  })

  map.on('moveend', () => {
    store.commit('SET_MAP_RESOLUTION', map.getView().getResolution())
    store.commit('SET_MAP_ZOOM', map.getView().getZoom())

    // check if there are active layers and show resolution notification if needed
    EventBus.$emit('resolutionNotification')
  })

  map.on('singleclick', singleClickCallbackFunction)

  map.on('pointermove', (evt) => {
    if (evt.dragging) {
      EventBus.$emit('closeMapPopup')
    }
  })
}

var disableEventListenerSingleClick = function () {
  const map = store.state.map
  map.un('singleclick', singleClickCallbackFunction)
}

var enableEventListenerSingleClick = function () {
  const map = store.state.map
  map.on('singleclick', singleClickCallbackFunction)
}

var getCorrectExtent = function (geojsonObj) {
  var tempLayer = new VectorLayer({
    source: new VectorSource({
      features: (new GeoJSON()).readFeatures(geojsonObj, {
        featureProjection: 'EPSG:3857'
      })
    })
  })
  // run a transform on all the feature coordinates (to change the range to 0 to 360)
  // due to issue with dateline in OpenLayers
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
  tempLayer.getSource().forEachFeature(function(feature){
    feature.getGeometry().applyTransform(wrapTransform);
  })

  return tempLayer.getSource().getExtent()
}

// Other testing types of OpenLayers layers

var createGeojsonLayer = function (geojson) {
  const map = store.state.map

  var gjsonLayer = new VectorLayer({
    source: new VectorSource({
      features: (new GeoJSON()).readFeatures(geojson, {
        featureProjection: 'EPSG:3857'
      }
      )
    }),
    style: new Style({
       fill: new Fill({
            color: 'rgba(255,255,255,0.3)'
       }),
       stroke: new Stroke({
            color: 'blue',
            width: 1
       })
    })
  })
  map.addLayer(gjsonLayer)
}

var createGeojsonVTlayer = function (geojson) {
  // Note: geojson-vt requires de source geojson to be in WGS84

  const map = store.state.map

  var replacer = function(key, value) {
    if (value && value.geometry) {
      var type
      var rawType = value.type
      var geometry = value.geometry

      if (rawType === 1) {
        type = geometry.length === 1 ? 'Point' : 'MultiPoint'
      } else if (rawType === 2) {
        type = geometry.length === 1 ? 'LineString' : 'MultiLineString'
      } else if (rawType === 3) {
        type = geometry.length === 1 ? 'Polygon' : 'MultiPolygon'
      }

      return {
        'type': 'Feature',
        'geometry': {
          'type': type,
          'coordinates': geometry.length == 1 ? geometry : [geometry]
        },
        'properties': value.tags
      };
    } else {
      return value;
    }
  };

  var tilePixels = new Projection({
    code: 'TILE_PIXELS',
    units: 'tile-pixels'
  });
  var tileIndex = geojsonvt(geojson, {
    extent: 4096,
    debug: 1
  });
  var vectorSource = new VectorTileSource({
    format: new GeoJSON(),
    tileGrid: createXYZ(),
    tilePixelRatio: 16,
    tileLoadFunction: (tile, tileCoord) => {
      var format = tile.getFormat()
      var data = tileIndex.getTile.apply(tileIndex, tileCoord)

      if (data) {
        var features = format.readFeatures(
          JSON.stringify({
            type: 'FeatureCollection',
            features: data.features
          }, replacer));
        tile.setLoader(() => {
          tile.setFeatures(features)
          tile.setProjection(tilePixels)
        });
      }
    },
    tileUrlFunction: function(tileCoord) {
      return [tileCoord[0], tileCoord[1], -tileCoord[2] - 1]
    }
  })
  var vectorLayer = new VectorTileLayer({
    source: vectorSource
  })
  map.addLayer(vectorLayer)
}

var isLayerDisplayed = function (layer) {
  const map = store.state.map
  var viewResolution = map.getView().getResolution()
  if ( isFinite(layer.get('maxResolution')) ) {
    return (viewResolution < layer.get('maxResolution') && viewResolution > layer.get('minResolution'))
  } else {
    return true
  }
}


// Styles
var drawingStyle = new Style({
                    fill: new Fill({
                      color: 'rgba(255, 204, 51, 0.5)'
                    }),
                    stroke: new Stroke({
                      color: 'rgba(255, 204, 51, 1)',
                      width: 2
                    }),
                    image: new CircleStyle({
                      radius: 5,
                      fill: new Fill({
                        color: 'rgba(255, 204, 51, 0.5)'
                      }),
                      stroke: new Stroke({
                        color: 'rgba(255, 204, 51, 1)',
                        width: 2
                      })
                    })
                  })

var defaultStoryGeomStyle = function (feature) {
  return new Style({
             fill: new Fill({
               color: 'rgba(31, 109, 224, 0.5)'
             }),
             stroke: new Stroke({
               color: 'rgba(31, 109, 224, 1)',
               width: 2
             }),
             image: new CircleStyle({
               radius: 5,
               fill: new Fill({
                 color: 'rgba(31, 109, 224, 0.5)'
               }),
               stroke: new Stroke({
                 color: 'rgba(31, 109, 224, 1)',
                 width: 2
               })
             }),
             text: new Text({
               font: 'bold 13px Calibri,sans-serif',
               fill: new Fill({ color: '#000' }),
               stroke: new Stroke({
                 color: '#f2a2a2', width: 4
               }),
               text: typeof feature == 'string' ? feature : feature.get('label'),
               offsetY:15,
               overflow: true
             })
           })
}


var defaultStoryGeomLayerStyle = function (feature) {
  return [defaultStoryGeomStyle(feature)]
}


// Closes the map popup when clicking the cross button
$(document).on("click", ".popover .close" , function(){
  $(this).parents(".popover").popover('hide')
})

// Hide the map layers feature popup when the anywhere else in the body is clicked
$('body').on('click', function (e) {
  $('.feature-popup').each(function () {
    if (!$(this).is(e.target) && $(this).has(e.target).length === 0 ) {
      $(this).popover('hide')
    }
  })
})


module.exports = {enableEventListeners, getCorrectExtent, createGeojsonLayer, createGeojsonVTlayer,
                isLayerDisplayed, disableEventListenerSingleClick, enableEventListenerSingleClick,
                drawingStyle, defaultStoryGeomStyle, defaultStoryGeomLayerStyle}
