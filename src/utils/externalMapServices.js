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

// // to be used as color attribute value in fill property of an OL style
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


var addLinzWFS = function (obj) {
  const map = store.state.map

  var vs = new VectorSource({
    format: new GeoJSON(),
    url: function(extent) {
       return 'https://data.linz.govt.nz/services;key=' + linzKey + '/wfs?service=WFS&' +
        'version=2.0.0&request=GetFeature&typename=' + obj.layer_id + '&' +
        'outputFormat=application/json&srsname=EPSG:3857&' +
        'bbox=' + extent.join(',') + ',EPSG:3857';
    },
    strategy: tile(new createXYZ({
        maxZoom: 19
      })),
    crossOrigin: "Anonymous"
  })

  var vl = new VectorLayer({
    source: vs,
		name: obj.keyname,
		zIndex: obj.zindex,
    minResolution: obj.minresolution,
    maxResolution: obj.maxresolution,
    style: obj.style
  })

  map.addLayer(vl)
}


var addMfeWFS = function (obj) {
  const map = store.state.map

  var vs = new VectorSource({
    format: new GeoJSON(),
    url: function(extent) {
       return 'https://data.mfe.govt.nz/services;key=' + mfeKey + '/wfs?service=WFS&' +
        'version=2.0.0&request=GetFeature&typename=' + obj.layer_id + '&' +
        'outputFormat=application/json&srsname=EPSG:3857&' +
        'bbox=' + extent.join(',') + ',EPSG:3857';
    },
    strategy: tile(new createXYZ({
        maxZoom: 19
      })),
    crossOrigin: "Anonymous"
  })

  var vl = new VectorLayer({
    source: vs,
		name: obj.keyname,
		zIndex: obj.zindex,
    minResolution: obj.minresolution,
    maxResolution: obj.maxresolution,
    style: obj.style
  })

  map.addLayer(vl)
}

var addAerialImageryWMTS = function (obj) {
	const map = store.state.map

  var tl = new TileLayer({
    source: new XYZ({
      url: 'http://tiles-a.data-cdn.linz.govt.nz/services;key=' + linzKey + '/tiles/v4/set=4702/EPSG:3857/{z}/{x}/{y}.png',
      crossOrigin: "Anonymous"
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

module.exports = { addAerialImageryWMTS, addMBTileLayer, addLinzWFS, addMfeWFS }
