const store = require('store').default
var transform = require('ol/proj').transform
const Select = require('ol/interaction/Select').default
const condition = require('ol/events/condition')
const Style = require('ol/style/Style').default
const Stroke = require('ol/style/Stroke').default

var selectedPolyStyle = new Style({
                      stroke: new Stroke({
                        color: '#ff0000',
                        width: 2
                    })
                  })

module.exports = {
  enableEventListeners: function () {
    const map = store.state.map

    map.on('singleclick', (evt) => {
      console.log(evt.coordinate)
      // console.log(themap.getView().getZoom())
      // console.log(themap.getView().getCenter())
      // convert coordinate to EPSG-4326
      console.log(transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326'))
      // this.displayFeatureInfo(evt.pixel)
    })
  },
  addSelectInteraction: function () {
    const map = store.state.map

    // select interaction working on "click"
    var selectOnClick = new Select({
      condition: condition.click,
      style: selectedPolyStyle
    })
    // select interaction working on "pointermove"
    var selectOnHover = new Select({
      condition: condition.pointerMove
    })

    map.addInteraction(selectOnClick)
    selectOnClick.on('select', function (e) {
      console.log(e.target.getFeatures())
    })
    map.addInteraction(selectOnHover)
    selectOnHover.on('select', function () {
      // console.log(e.target.getFeatures())
    })
  }
}
