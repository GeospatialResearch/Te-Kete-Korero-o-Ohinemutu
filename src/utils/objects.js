var addAerialImageryWMTS = require('utils/externalMapServices').addAerialImageryWMTS
var addPropertyTitlesWFS = require('utils/externalMapServices').addPropertyTitlesWFS
var addProtectedAreasWFS = require('utils/externalMapServices').addProtectedAreasWFS
// var addSeaDrainingCatchmentsWFS = require('utils/externalMapServices').addSeaDrainingCatchmentsWFS
// var addMBTileLayer = require('utils/externalMapServices').addMBTileLayer
var _ = require('underscore')

var extLayersObj = {
  linz_aerial_imagery_wmts: {
    layername: 'NZ Aerial Imagery',
    attribution_name: 'Land Information New Zealand',
    attribution: '<i>Sourced from the <a href="https://data.linz.govt.nz/">LINZ Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>',
    visible: false,
    zindex: 0,
    functionToCall: function (obj) {
      return addAerialImageryWMTS(obj)
    }
  },
  linz_property_titles_wfs: {
    layername: 'NZ Property Titles',
    attribution_name: 'Land Information New Zealand',
    attribution: '<i>Sourced from the <a href="https://data.linz.govt.nz/">LINZ Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>',
    visible: false,
    zindex: 1,
    minresolution: 0,
    maxresolution: 4.5,
    functionToCall: function (obj) {
      return addPropertyTitlesWFS(obj)
    }
  },
  linz_protected_areas_wfs: {
    layername: 'Protected Areas',
    attribution_name: 'Land Information New Zealand',
    attribution: '<i>Sourced from the <a href="https://data.linz.govt.nz/">LINZ Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>',
    visible: false,
    zindex: 3,
    minresolution: 0,
    maxresolution: 80,
    functionToCall: function (obj) {
      return addProtectedAreasWFS(obj)
    }
  }
  // mfe_sea_drainingcatch_wfs: {
  //   layername: 'Sea-draining catchments',
  //   attribution_name: 'Ministry for the Environment',
  //   attribution: '<i>Sourced from the <a href="https://data.mfe.govt.nz/">MfE Data Service</a> and licensed for reuse under the <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> licence.</i>',
  //   visible: false,
  //   zindex: 2,
  //   minresolution: 10,
  //   maxresolution: 300,
  //   functionToCall: function (obj) {
  //     return addSeaDrainingCatchmentsWFS(obj)
  //   }
  // }
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
