const store = require('store').default
var EventBus = require('store/event-bus.js').EventBus
const Select = require('ol/interaction/Select').default
const DragAndDrop = require('ol/interaction/DragAndDrop').default
const condition = require('ol/events/condition')
const Style = require('ol/style/Style').default
const Fill = require('ol/style/Fill').default
const Stroke = require('ol/style/Stroke').default
const Circle = require('ol/style/Circle').default
const Projection = require('ol/proj/Projection').default
var createXYZ = require('ol/tilegrid').createXYZ
var geojsonvt = require('geojson-vt').default
const VectorSource = require('ol/source/Vector').default
const VectorLayer = require('ol/layer/Vector').default
const VectorTileSource = require('ol/source/VectorTile').default
const VectorTileLayer = require('ol/layer/VectorTile').default
const GeoJSON = require('ol/format/GeoJSON').default
const KML = require('ol/format/KML').default

var selectedPolyStyle = new Style({
                      fill: new Fill({
                        color: 'rgba(255,0,0,0.5)'
                      }),
                      stroke: new Stroke({
                        color: '#ff0000',
                        width: 2
                    })
                  })

var hoveredPolyStyle = new Style({
                      fill: new Fill({
                        color: 'rgba(255,0,0,0.2)'
                      }),
                      stroke: new Stroke({
                        color: '#f00',
                        width: 1
                      })
                    })

var fill = new Fill({
        color: 'rgba(0,0,0,0.2)'
      });

var stroke = new Stroke({
  color: 'rgba(0,0,0,0.4)'
})

var circle = new Circle({
  radius: 6,
  fill: fill,
  stroke: stroke
})

var vectorStyle = new Style({
  fill: fill,
  stroke: stroke,
  image: circle
})


var enableEventListeners = function () {
  const map = store.state.map

  var currZoom = map.getView().getZoom()
  map.on('moveend', () => {
    var newZoom = map.getView().getZoom()
    if (currZoom != newZoom) {
      currZoom = newZoom
      store.commit('SET_MAP_RESOLUTION', map.getView().getResolution())
      store.commit('SET_MAP_ZOOM', map.getView().getZoom())
    }
  })
}

var addInteractions = function () {
  const map = store.state.map

  // Note: The primary purpose of vector tiles is rendering. It splits up features across tile layers,
  // leaving them with the same id. It prevents you from using ol.interaction.Select
  // You can use map.forEachFeatureAtPixel instead to get interactivity in this case (TODO).

  // select interaction working on "click"
  var selectOnClick = new Select({
    condition: condition.click,
    style: selectedPolyStyle
  })
  selectOnClick.on('select', (e) => {
    EventBus.$emit('showMapPopup', {
      'features': e.target.getFeatures().getArray(), 
      'coordinate': e.mapBrowserEvent.coordinate
    })
  })
  map.addInteraction(selectOnClick)

  // dragAndDrop interaction to load a dataset
  var dragAndDrop = new DragAndDrop({
    formatConstructors: [
      GeoJSON,
      KML
    ]
  })
  dragAndDrop.on('addfeatures', function(event) {
    if (event.features.length < 10000) {
      var vectorSource = new VectorSource({
        features: event.features,
        projection: event.projection
      });
      map.addLayer(new VectorLayer({
        source: vectorSource,
        style: vectorStyle
      }));
      var view = map.getView();
      view.fit(vectorSource.getExtent(), map.getSize());
    } else {
      alert('The dataset has more than 10000 features: ' + event.features.length)
    }
  })
  map.addInteraction(dragAndDrop)

  // select interaction working on "pointermove"
  var selectOnHover = new Select({
    condition: condition.pointerMove,
    style: hoveredPolyStyle
  })
  selectOnHover.on('select', function () {
    // console.log(e.target.getFeatures().getArray())
  })
  map.addInteraction(selectOnHover)
}

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


module.exports = {enableEventListeners, addInteractions, createGeojsonLayer, createGeojsonVTlayer}
