// to include the utility functions to deal with js objects
const Style = require('ol/style/Style').default
const Stroke = require('ol/style/Stroke').default
const Fill = require('ol/style/Fill').default
const Circle = require('ol/style/Circle').default


var hexToRgba = function (hex,opacity) {
    hex = hex.replace('#','')
    var r, g, b
    r = parseInt(hex.substring(0,2), 16)
    g = parseInt(hex.substring(2,4), 16)
    b = parseInt(hex.substring(4,6), 16)

    var result = 'rgba('+r+','+g+','+b+','+opacity+')'
    return result
}


var hexToRgb = function (hex) {
  var rgb = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return rgb ? {
    r: parseInt(rgb[1], 16),
    g: parseInt(rgb[2], 16),
    b: parseInt(rgb[3], 16)
  } : null
}

var polygonStyle = function (color) {
  return new Style({
    fill: new Fill({
      color: 'rgba(' + hexToRgb(color).r + ', ' + hexToRgb(color).g + ', ' + hexToRgb(color).b + ', 0.5)'
      // color: makePattern()
    }),
    stroke: new Stroke({
      color: 'rgba(' + hexToRgb(color).r + ', ' + hexToRgb(color).g + ', ' + hexToRgb(color).b + ', 1)',
      width: 2
    })
  })
}

var lineStyle = function (color) {
  return new Style({
       stroke: new Stroke({
         color: 'rgba(' + hexToRgb(color).r + ', ' + hexToRgb(color).g + ', ' + hexToRgb(color).b + ', 1)',
         width: 3
    })
   })
}

var pointStyle = function (color) {
  return new Style({
      image: new Circle({
        radius: 3,
        fill: new Fill({
          color: 'rgba(' + hexToRgb(color).r + ', ' + hexToRgb(color).g + ', ' + hexToRgb(color).b + ', 0.5)'
        }),
        stroke: new Stroke({
          color: 'rgba(' + hexToRgb(color).r + ', ' + hexToRgb(color).g + ', ' + hexToRgb(color).b + ', 1)',
          width: 2
        })
      })
    })
}

var imgFormats = ['jpg', 'jpeg', 'png', 'svg', 'bmp']
var videoFormats = ['mp4']
var audioFormats = ['mp3']


module.exports = { polygonStyle, lineStyle, pointStyle, imgFormats, videoFormats, audioFormats, hexToRgba, hexToRgb }
