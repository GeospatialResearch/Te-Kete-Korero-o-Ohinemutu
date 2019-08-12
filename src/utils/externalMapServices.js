const Style = require('ol/style/Style').default
const Stroke = require('ol/style/Stroke').default
const Fill = require('ol/style/Fill').default
const GeoJSON = require('ol/format/GeoJSON').default
const VectorSource = require('ol/source/Vector').default
const VectorLayer = require('ol/layer/Vector').default
var createXYZ = require('ol/tilegrid').createXYZ
var tile = require('ol/loadingstrategy').tile
var TileLayer = require('ol/layer/Tile').default
var XYZ = require('ol/source/XYZ').default
var VectorTileSource = require('ol/source/VectorTile').default
var VectorTileLayer = require('ol/layer/VectorTile').default
var MVT = require('ol/format/MVT').default
var Feature = require('ol/Feature').default

const store = require('store').default
const linzKey = process.env.LINZ_ACCESS_KEY
const mfeKey = process.env.MFE_ACCESS_KEY


// function makePattern() {
// 	var cnv = document.createElement('canvas');
//   var ctx = cnv.getContext('2d');
//   cnv.width = 6;
//   cnv.height = 6;
//   ctx.fillStyle = 'rgb(255, 0, 0)';
//
//   for(var i = 0; i < 6; ++i) {
//     ctx.fillRect(i, i, 1, 1);
//   }
//   return ctx.createPattern(cnv, 'repeat');
// }

var addPropertyTitlesWFS = function (obj) {
  const map = store.state.map

  var vs = new VectorSource({
    // loader: function(extent) {
    //   $.ajax('https://data.linz.govt.nz/services;key=068f37bc27874c79aee57d4fb4d1455d/wfs',{
    //     type: 'GET',
    //     data: {
    //         service: 'WFS',
    //         version: '2.0.0',
    //         request: 'GetFeature',
    //         typename: 'layer-50804',
    //         srsname: 'EPSG:3857',
    //         outputFormat: 'application/json',
    //         bbox: extent.join(',') + ',EPSG:3857'
    //         },
    //     }).done(function(response) {
    //         var geoJSON = new GeoJSON();
    //         vs.addFeatures(geoJSON.readFeatures(response))
    //       })
    // },
    format: new GeoJSON(),
    url: function(extent) {
       return 'https://data.linz.govt.nz/services;key=' + linzKey + '/wfs?service=WFS&' +
        'version=2.0.0&request=GetFeature&typename=layer-50804&' +
        'outputFormat=application/json&srsname=EPSG:3857&' +
        'bbox=' + extent.join(',') + ',EPSG:3857';
    },
    strategy: tile(new createXYZ({
        maxZoom: 19
        }))
  })

  var vl = new VectorLayer({
    source: vs,
		name: obj.keyname,
		zIndex: obj.zindex,
    minResolution: obj.minresolution,
    maxResolution: obj.maxresolution,
    style: obj.property_layer_style
  })

  map.addLayer(vl)
}

var addProtectedAreasWFS = function (obj) {
  const map = store.state.map

  var vs = new VectorSource({
    format: new GeoJSON(),
    url: function(extent) {
       return 'https://data.linz.govt.nz/services;key=' + linzKey + '/wfs?service=WFS&' +
        'version=2.0.0&request=GetFeature&typename=layer-53564&' +
        'outputFormat=application/json&srsname=EPSG:3857&' +
        'bbox=' + extent.join(',') + ',EPSG:3857';
    },
    strategy: tile(new createXYZ({
        maxZoom: 19
        }))
  })

  var vl = new VectorLayer({
    source: vs,
		name: obj.keyname,
		zIndex: obj.zindex,
    minResolution: obj.minresolution,
    maxResolution: obj.maxresolution,
    style: obj.protected_layer_style
  })

  map.addLayer(vl)
}

var addSeaDrainingCatchmentsWFS = function (obj) {
  const map = store.state.map

  var vs = new VectorSource({
    format: new GeoJSON(),
    url: function(extent) {
       return 'https://data.mfe.govt.nz/services;key=' + mfeKey + '/wfs?service=WFS&' +
        'version=2.0.0&request=GetFeature&typename=layer-99776&' +
        'outputFormat=application/json&srsname=EPSG:3857&' +
        'bbox=' + extent.join(',') + ',EPSG:3857';
    },
    strategy: tile(new createXYZ({
        maxZoom: 19
        }))
  })

  var vl = new VectorLayer({
    source: vs,
		name: obj.keyname,
		zIndex: obj.zindex,
    minResolution: obj.minresolution,
    maxResolution: obj.maxresolution,
    style: new Style({
      fill: new Fill({
        color: 'rgba(119, 215, 224, 0.6)'
      }),
      stroke: new Stroke({
        color: '#309ed2',
        width: 2
      })
    })
  })

  map.addLayer(vl)
}

var addAerialImageryWMTS = function (obj) {
	const map = store.state.map

  var tl = new TileLayer({
    source: new XYZ({
      url: 'http://tiles-a.data-cdn.linz.govt.nz/services;key=' + linzKey + '/tiles/v4/set=4702/EPSG:3857/{z}/{x}/{y}.png'
    }),
		name: obj.keyname,
		zIndex: obj.zindex
  })

  map.addLayer(tl)
}

var addMBTileLayer = function () {
  const map = store.state.map

  var vtl = new VectorTileLayer({
    source: new VectorTileSource({
      format: new MVT({featureClass: Feature}),
      url: 'https://data.esp.gritool.com/christchurch/data/{z}/{x}/{y}.pbf'
    }),
    maxResolution: 5
  })

  map.addLayer(vtl)
}

module.exports = {addPropertyTitlesWFS, addProtectedAreasWFS, addSeaDrainingCatchmentsWFS, addAerialImageryWMTS, addMBTileLayer}

// // Note: loading a WFS with the bboxStrategy it doesn't work so well as using the tile createXYZ strategy
// // import { bbox as bboxStrategy } from 'ol/loadingstrategy'

// new VectorLayer({
//   source: new VectorSource({
//     format: new GeoJSON(),
//     url: function(extent) {
//       return 'https://data.linz.govt.nz/services;key=068f37bc27874c79aee57d4fb4d1455d/wfs?service=WFS&' +
//           'version=2.0.0&request=GetFeature&typeNames=layer-50804&' +
//           'outputFormat=application/json&srsname=EPSG:3857&' +
//           'bbox=' + extent.join(',') + ',EPSG:3857';
//     },
//     strategy: bboxStrategy
//   }),
//   minResolution: 0,
//   maxResolution: 3,
//   style: new Style({
//     stroke: new Stroke({
//       color: 'rgba(0, 0, 255, 1.0)',
//       width: 1
//     })
//   })
// })
