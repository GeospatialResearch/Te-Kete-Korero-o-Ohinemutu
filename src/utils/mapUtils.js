const store = require('store').default
var EventBus = require('store/event-bus.js').EventBus
const Style = require('ol/style/Style').default
const Fill = require('ol/style/Fill').default
const Stroke = require('ol/style/Stroke').default
const CircleStyle = require('ol/style/Circle').default
const Text = require('ol/style/Text').default
const Projection = require('ol/proj/Projection').default
const Feature = require('ol/Feature').default
const Point = require('ol/geom/Point').default
const LineString = require('ol/geom/LineString').default
const MultiLineString = require('ol/geom/MultiLineString').default
const Polygon = require('ol/geom/Polygon').default
const MultiPolygon = require('ol/geom/MultiPolygon').default
var createXYZ = require('ol/tilegrid').createXYZ
var geojsonvt = require('geojson-vt').default
const VectorSource = require('ol/source/Vector').default
const VectorLayer = require('ol/layer/Vector').default
const VectorTileSource = require('ol/source/VectorTile').default
const VectorTileLayer = require('ol/layer/VectorTile').default
const GeoJSON = require('ol/format/GeoJSON').default
var getWidth = require('ol/extent').getWidth
var extend = require('ol/extent').extend
var getCenter = require('ol/extent').getCenter
// var findByName = require('utils/olHelper').findByName
const extLayersObj = require('utils/objects').extLayersObj
var _ = require('underscore')
const AnimatedCluster = require('ol-ext/layer/AnimatedCluster').default
const Cluster = require('ol/source/Cluster').default


var singleClickCallbackFunction = function (evt) {
  const map = store.state.map
  EventBus.$emit('closeMapPopup')
  EventBus.$emit('resetSelectedFeatures')

  // console.log(map.getView().getZoom())
  // console.log(evt.coordinate)

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
    if (layer) {
      if (layer.get('name') !== 'storyGeomsLayer' && layer.get('name') !== 'allStoriesGeomsLayer' && layer.get('name') !== 'selectedFeaturesLayer') {
        nExpectedCount++
      }
    }
  }, { hitTolerance: store.state.hitTolerance })
  EventBus.$emit('defineExpectedCount', nExpectedCount)

  // Show allStoriesGeomsLayer features usage
  var features = map.getFeaturesAtPixel(evt.pixel, {
      layerFilter: function(layer) {
          return layer.get('name') === 'allStoriesGeomsLayer'
      }
  })
  var geomsUsage = []
  if (features) {

    // if using Cluster we need to get the features inside the Cluster feature
    features = features[0].get('features')

    if (store.state.reuseMode) {
      store.commit('ADD_FEATURES_FOR_REUSE', features)
      if (nExpectedCount == 0) {
        EventBus.$emit('showFeaturesReuse')
      }
    } else {
      features.forEach((feature) => {
        geomsUsage.push(store.state.allStoriesGeomsLayer.allUsedStoriesGeometriesObj[feature.getProperties().id])
      })
      if (features.length > 5) {
        // map.getView().setZoom(map.getView().getZoom()+1)
        var extent = features[0].getGeometry().getExtent().slice(0)
        features.forEach(function(feature){ extend(extent,feature.getGeometry().getExtent())});
        map.getView().fit(extent, { duration: 2000 })
      } else {
        EventBus.$emit('showGeomsUsage', geomsUsage)
      }
    }
  }

  if (nExpectedCount != 0) {

    // External vector layers
    map.forEachFeatureAtPixel(evt.pixel, (feature, layer) => {
      if (layer) {
        if (extLayersObj[layer.get('name')]) {  // if the extLayersObj has this layer name (in order to exclude the name storyGeomsLayer)
          EventBus.$emit('showLayersFeaturesPopup', {
            'features': [feature],
            'coordinate': evt.coordinate,
            'layername': extLayersObj[layer.get('name')].layername
          })
        }
      }
    }, { hitTolerance: store.state.hitTolerance })

    // Internal geoserser wms layers
    layers.forEach( (layer) => {
      var layername = layer.get('name')
      if (layer.getVisible() && !['Basemap', 'drawingLayer', 'storyGeomsLayer', 'allStoriesGeomsLayer', 'selectedFeaturesLayer'].includes(layername) && !Object.keys(store.state.externalLayers).includes(layername)) {
        $.ajax({
          url: layer.getSource().getGetFeatureInfoUrl(evt.coordinate, viewResolution, projection,  // creates the WMS getFeatureInfo request for us
            { 'INFO_FORMAT': 'text/javascript',
              'format_options': 'callback:' + layername,
              'FEATURE_COUNT': '50' // It needs to specify a number, otherwise only returns the first it gets
            }
          ),
          dataType: 'jsonp',
          jsonpCallback: layername // instead of a static name like 'getJson' to avoid the classic race issue
        }).done(function (response) {
          if (response.features.length > 0) {
            EventBus.$emit('showLayersFeaturesPopup', {
              'features': response.features,
              'coordinate': evt.coordinate,
              'layername': layername.split("__")[0]
            })
          } else {
            EventBus.$emit('showLayersFeaturesPopup', {
              'coordinate': evt.coordinate,
            })
          }
        })
      }
    })
  } // end if nExpectedCount != 0


  // Show storyGeomsLayer features info
  map.forEachFeatureAtPixel(evt.pixel, (feature, layer) => {
    if (layer) {
      if (layer.get('name') === 'storyGeomsLayer') {
        EventBus.$emit('getStoryGeomInfo', feature)
      }
    }
  }, { hitTolerance: store.state.hitTolerance })

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
  if (map) {
    map.un('singleclick', singleClickCallbackFunction)
  }
}

var enableEventListenerSingleClick = function () {
  const map = store.state.map
  if (map) {
    map.on('singleclick', singleClickCallbackFunction)
  }
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


var addAllStoriesGeomsLayer = function (geoms) {
  const map = store.state.map

  EventBus.$emit('removeLayer', 'allStoriesGeomsLayer')
  EventBus.$emit('resetDrawnFeature')

  // // Create an empty allStoriesGeomsLayer layer
  // var allStoriesGeomsSource = new VectorSource({
  //   format: new GeoJSON()
  // })
  // var allstoriesGeomsVector = new VectorLayer({
  //   source: allStoriesGeomsSource,
  //   name: 'allStoriesGeomsLayer',
  //   style: allStoriesGeomsStyle,
  //   zIndex: 30
  // })
  // map.addLayer(allstoriesGeomsVector)

  // Cluster Source
  var clusterSource = new Cluster({
    distance: 40,
    source: new VectorSource()
  });
  // Animated cluster layer
  var clusterLayer = new AnimatedCluster({
    name: 'allStoriesGeomsLayer',
    source: clusterSource,
    animationDuration: 700,
    // Cluster style
    style: getClusterStyle,
    zIndex: 30
  });
  map.addLayer(clusterLayer);

  // Add features to layer
  var featuresToAdd = []
  var ol_geom
  _.each(geoms, (geom) => {
    ol_geom = olFeatureFromJsonGeom(geom)
    featuresToAdd.push(new Feature({
        geometry: ol_geom,
        id: geom.id,
        label: geom.name.eng
    }))
  })

  // Make the centers to be the geometries so can be used in the cluster
  _.each(featuresToAdd, (feat) => {
    var aa = feat.getGeometry().getExtent()
    var oo = getCenter(aa)
    feat.set('feat_geometry', feat.getGeometry())
    feat.set('geometry', new Point(oo)) // center
  })

  // allStoriesGeomsSource.addFeatures(featuresToAdd)
  clusterLayer.getSource().getSource().clear()
  clusterLayer.getSource().getSource().addFeatures(featuresToAdd)

  // var extent = allstoriesGeomsVector.getSource().getExtent()
  // map.getView().fit(extent, { duration: 2000 })

  EventBus.$emit('setallStoriesGeomsLayerLegend', allStoriesGeomsStyle)

  removeStoryGeomsFromStoriesGeomsLayer()

}


var removeStoryGeomsFromStoriesGeomsLayer = function () {
  const map = store.state.map
  var storyfeaturesId = []

  map.getLayers().forEach( (layer) => {
    if (layer.get('name') === 'storyGeomsLayer') {
      var storyfeatures = layer.getSource().getFeatures()
      _.each(storyfeatures, (feature) => {
        storyfeaturesId.push(feature.getProperties().name)
      })
    }
  })

  if (storyfeaturesId.length > 0) {
    map.getLayers().forEach( (layer) => {
      if (layer.get('name') === 'allStoriesGeomsLayer') {

        // getting the features of all clusters
        var features = layer.getSource().getSource().getFeatures()
        if (features.length != store.state.allStoriesGeomsLayer.allUsedStoriesGeometries.length) {
          store.commit('RESTORE_ALL_USEDSTORIESGEOMETRIES')
          return
        }

        // remove story geoms from all geoms
        var featuresToAdd = []
        _.each(features, (feature) => {
          if (!storyfeaturesId.includes(feature.getProperties().id)) {
            featuresToAdd.push(feature)
          }
        })

        // we need to reach clusterSource of allStoriesGeomsLayer
        layer.getSource().getSource().clear()
        layer.getSource().getSource().addFeatures(featuresToAdd)
      }
    })
  }
}


var addSelectedFeaturesLayer = function (features) {
  const map = store.state.map

  var featuresToAdd = []
  _.each(features, (feature) => {
    try {
      feature.getProperties()
      featuresToAdd.push(feature) // external services (OL feature from forEachFeatureAtPixel)
    } catch (e) {
      if (feature.geometry) {
        var ol_geom = olFeatureFromJsonGeom(feature) // internal services (json geometry from getGetFeatureInfoUrl)
        featuresToAdd.push(new Feature({
            geometry: ol_geom,
            // id: geom.id,
            // label: geom.name
        }))
      }
    }
  })

  // Create an empty allStoriesGeomsLayer layer
  var selectedFeaturesSource = new VectorSource({
    format: new GeoJSON()
  })
  var selectedFeaturesVector = new VectorLayer({
    source: selectedFeaturesSource,
    name: 'selectedFeaturesLayer',
    style: selectedFeaturesStyle,
    zIndex: 60
  })
  map.addLayer(selectedFeaturesVector)
  selectedFeaturesSource.addFeatures(featuresToAdd)
}


var olFeatureFromJsonGeom = function (geom) {
  var ol_geom
  if (geom.geometry.type == 'Polygon') {
    ol_geom = new Polygon(geom.geometry.coordinates)
  } else if (geom.geometry.type == 'MultiPolygon') {
    ol_geom = new MultiPolygon(geom.geometry.coordinates)
  } else if (geom.geometry.type == 'LineString') {
    ol_geom = new LineString(geom.geometry.coordinates)
  } else if (geom.geometry.type == 'MultiLineString') {
    ol_geom = new MultiLineString(geom.geometry.coordinates)
  } else {
    ol_geom = new Point(geom.geometry.coordinates)
  }

  return ol_geom
}


// Styles
var drawingStyle = new Style({
                    fill: new Fill({
                      color: 'rgba(255, 204, 51, 0.5)'
                    }),
                    stroke: new Stroke({
                      color: 'rgba(255, 204, 51, 1)',
                      width: 3
                    }),
                    image: new CircleStyle({
                      radius: 5,
                      fill: new Fill({
                        color: 'rgba(255, 204, 51, 0.5)'
                      }),
                      stroke: new Stroke({
                        color: 'rgba(255, 204, 51, 1)',
                        width: 3
                      })
                    })
                  })


// var allStoriesGeomsStyle = new Style({
//                     fill: new Fill({
//                       color: 'rgba(195, 12, 12, 0.7)'
//                     }),
//                     stroke: new Stroke({
//                       color: 'rgba(195, 12, 12, 1)',
//                       width: 2
//                     }),
//                     image: new CircleStyle({
//                       radius: 5,
//                       fill: new Fill({
//                         color: 'rgba(195, 12, 12, 0.7)'
//                       }),
//                       stroke: new Stroke({
//                         color: 'rgba(195, 12, 12, 1)',
//                         width: 2
//                       })
//                     })
//                   })

var allStoriesGeomsStyle = new Style({
                                  image: new CircleStyle({
                                    radius: Math.max(8, Math.min(5*0.75, 20)),
                                    stroke: new Stroke({
                                      color: "rgba(0,128,0,0.5)",
                                      width: 13,
                                      // lineDash: dash_,
                                      lineCap: "butt"
                                    }),
                                    fill: new Fill({
                                      color:"rgba(0,128,0,1)"
                                    })
                                  }),
                                  text: new Text({
                                    text: '1',
                                    font: 'bold 13px sans-serif',
                                    //textBaseline: 'top',
                                    fill: new Fill({
                                      color: '#fff'
                                    })
                                  })
                                })


var defaultStoryGeomStyle = function (feature) {
  return new Style({
             fill: new Fill({
               color: 'rgba(31, 109, 224, 0.1)'
             }),
             stroke: new Stroke({
               color: 'rgba(31, 109, 224, 1)',
               width: 4
             }),
             image: new CircleStyle({
               radius: 5,
               fill: new Fill({
                 color: 'rgba(31, 109, 224, 0.5)'
               }),
               stroke: new Stroke({
                 color: 'rgba(31, 109, 224, 1)',
                 width: 4
               })
             }),
             text: new Text({
               font: 'bold 15px Calibri,sans-serif',
               fill: new Fill({ color: '#2b2828' }),
               stroke: new Stroke({
                 color: '#ffffff', width: 4
               }),
               text: typeof feature == 'string' ? feature : feature.get('label'),
               offsetY:15,
               overflow: true
             })
           })
}


var selectedFeaturesStyle = new Style({
                    fill: new Fill({
                      color: 'rgba(29, 214, 192, 0)'
                    }),
                    stroke: new Stroke({
                      color: 'rgba(29, 226, 226, 1)',
                      width: 3
                    }),
                    image: new CircleStyle({
                      radius: 6,
                      fill: new Fill({
                        color: 'rgba(29, 214, 192, 0)'
                      }),
                      stroke: new Stroke({
                        color: 'rgba(29, 226, 226, 1)',
                        width: 3
                      })
                    })
                  })


var defaultStoryGeomLayerStyle = function (feature) {
  return [defaultStoryGeomStyle(feature)]
}

// Style for the clusters
var styleCache = {};
function getClusterStyle (feature){
  var size = feature.get('features').length;
  var style = styleCache[size];
  if (!style) {
    var color = size>25 ? "192,0,0" : size>8 ? "255,128,0" : "0,128,0";
    var radius = Math.max(8, Math.min(size*0.75, 20));
    // var dash = 2*Math.PI*radius/6;
    // var dash_ = [ 0, dash, dash, dash, dash, dash, dash ];
    style = styleCache[size] = new Style({
      image: new CircleStyle({
        radius: radius,
        stroke: new Stroke({
          color: "rgba("+color+",0.5)",
          width: 13,
          // lineDash: dash_,
          lineCap: "butt"
        }),
        fill: new Fill({
          color:"rgba("+color+",1)"
        })
      }),
      text: new Text({
        text: size.toString(),
        font: 'bold 13px sans-serif',
        //textBaseline: 'top',
        fill: new Fill({
          color: '#fff'
        })
      })
    });
  }
  return style;
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
                drawingStyle, defaultStoryGeomStyle, defaultStoryGeomLayerStyle, addAllStoriesGeomsLayer,
                removeStoryGeomsFromStoriesGeomsLayer, olFeatureFromJsonGeom, addSelectedFeaturesLayer}
