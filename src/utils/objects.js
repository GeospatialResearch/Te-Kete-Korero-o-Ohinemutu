var addAerialImageryWMTS = require('utils/externalMapServices').addAerialImageryWMTS
var addLinzWFS = require('utils/externalMapServices').addLinzWFS
var addMfeWFS = require('utils/externalMapServices').addMfeWFS
// var addMBTileLayer = require('utils/externalMapServices').addMBTileLayer
var polygonStyle = require('utils/objectUtils').polygonStyle
var lineStyle = require('utils/objectUtils').lineStyle
var pointStyle = require('utils/objectUtils').pointStyle
var _ = require('underscore')


var extLayersObj = {
  linz_aerial_imagery_wmts: {
    layername: 'NZ Aerial Imagery',
    attribution_name: 'Land Information New Zealand',
    attribution: `<p><strong>Layer name:</strong> NZ Aerial Imagery</p>
                  <i>Sourced from the <a href="https://data.linz.govt.nz/">LINZ Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>`,
    visible: false,
    zindex: 1,
    functionToCall: function (obj) {
      return addAerialImageryWMTS(obj)
    }
  },
  linz_property_titles_wfs: {
    layername: 'NZ Property Titles',
    attribution_name: 'Land Information New Zealand',
    attribution: `<p><strong>Layer name:</strong> NZ Property Titles</p>
                  <i>Sourced from the <a href="https://data.linz.govt.nz/">LINZ Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>`,
    layer_id: 'layer-50804',
    visible: false,
    zindex: 10,
    minresolution: 0,
    maxresolution: 4.5,
    functionToCall: function (obj) {
      return addLinzWFS(obj)
    },
    style: polygonStyle("#164bc1"),
    geomtype: 2
  },
  linz_protected_areas_wfs: {
    layername: 'Protected Areas',
    attribution_name: 'Land Information New Zealand',
    attribution: `<p><strong>Layer name:</strong> Protected Areas</p>
                  <i>Sourced from the <a href="https://data.linz.govt.nz/">LINZ Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>`,
    layer_id: 'layer-53564',
    visible: false,
    zindex: 10,
    minresolution: 0,
    maxresolution: 80,
    functionToCall: function (obj) {
      return addLinzWFS(obj)
    },
    style: polygonStyle("#1bd597"),
    geomtype: 2
  },
  linz_height_points_wfs: {
    layername: 'NZ Height Points',
    attribution_name: 'Land Information New Zealand',
    attribution: `<p><strong>Layer name:</strong> NZ Height Points (Topo, 1:50k)</p>
                  <i>Sourced from the <a href="https://data.linz.govt.nz/">LINZ Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>`,
    layer_id: 'layer-50284',
    visible: false,
    zindex: 10,
    minresolution: 0,
    maxresolution: 200,
    functionToCall: function (obj) {
      return addLinzWFS(obj)
    },
    style: pointStyle("#d5691b"),
    geomtype: 0
  },
  linz_rivers_centrelines_wfs: {
    layername: 'NZ River Centrelines',
    attribution_name: 'Land Information New Zealand',
    attribution: `<p><strong>Layer name:</strong> NZ River Centrelines (Topo, 1:250k)</p>
                  <i>Sourced from the <a href="https://data.linz.govt.nz/">LINZ Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>`,
    layer_id: 'layer-50182',
    visible: false,
    zindex: 10,
    minresolution: 0,
    maxresolution: 100,
    functionToCall: function (obj) {
      return addLinzWFS(obj)
    },
    style: lineStyle("#1ba3d5"),
    geomtype: 1
  },
  mfe_sea_drainingcatch_wfs: {
    layername: 'Sea-draining catchments',
    attribution_name: 'Ministry for the Environment',
    attribution: `<p><strong>Layer name:</strong> Sea-draining catchments</p>
                  <i>Sourced from the <a href="https://data.mfe.govt.nz/">MfE Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>`,
    layer_id: 'layer-99776',
    visible: false,
    zindex: 10,
    minresolution: 0,
    maxresolution: 300,
    functionToCall: function (obj) {
      return addMfeWFS(obj)
    },
    style: polygonStyle("#1bcad5"),
    geomtype: 2
  }
}

// iterate over extLayersObj elements to auto assign an attribute keyname with its own key
_.each(extLayersObj, function (value, key) {
  value.keyname = key
})

// generate global variables to be used for the notifications about resolution
_.each(extLayersObj, (l, key) => {
  if (l.hasOwnProperty('maxresolution')) {
    window['resolutionNotify_' + key]
  }
})

module.exports = { extLayersObj }
