var addAerialImageryWMTS = require('utils/externalMapServices').addAerialImageryWMTS
var addPropertyTitlesWFS = require('utils/externalMapServices').addPropertyTitlesWFS
var addProtectedAreasWFS = require('utils/externalMapServices').addProtectedAreasWFS
// var addSeaDrainingCatchmentsWFS = require('utils/externalMapServices').addSeaDrainingCatchmentsWFS
// var addMBTileLayer = require('utils/externalMapServices').addMBTileLayer
var _ = require('underscore')
const Style = require('ol/style/Style').default
const Stroke = require('ol/style/Stroke').default
const Fill = require('ol/style/Fill').default

var property_layer_style = new Style({
  fill: new Fill({
    color: 'rgba(255, 255, 255, 0)' // so it will be recognised on hover, otherwise only when hovering on the edges the feature would be identified
  }),
  stroke: new Stroke({
    color: 'rgba(0, 0, 255, 1.0)',
    width: 1
  })
})
var protected_layer_style =  new Style({
  fill: new Fill({
    color: 'rgba(255, 255, 255, 0.6)'
    // color: makePattern()
  }),
  stroke: new Stroke({
    color: '#319FD3',
    width: 1
  })
})

var extLayersObj = {
  linz_aerial_imagery_wmts: {
    legend: null,
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
    legend: getIconLegend(property_layer_style),
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
    legend: getIconLegend(protected_layer_style),
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

function getIconLegend(style) {
		var radius = 10;
    var strokeWidth = style.getStroke().getWidth();
    var dx = radius + strokeWidth;
    var svgElem = $('<svg />')
        .attr({
            width: dx * 2,
            height: dx * 2
       })

    $('<circle />')
        .attr({
            cx: dx,
            cy: dx,
            r: radius,
            stroke: style.getStroke().getColor(),
            'stroke-width': strokeWidth,
            fill: style.getFill().getColor()
        })
        .appendTo(svgElem);
    // Convert DOM object to string to overcome from some SVG manipulation related oddities
    return $('<div>').append(svgElem).html();
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
