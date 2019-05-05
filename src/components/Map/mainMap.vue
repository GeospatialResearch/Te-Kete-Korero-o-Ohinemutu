<template>
  <div>
    <div id="map" />
  </div>
</template>

<script>

// Import everything from ol
import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import XYZ from 'ol/source/XYZ'
import * as proj from 'ol/proj'

export default {
  name: 'MapView',
  data() {
    return {}
  },
  mounted: function () {
    this.initMap()
  },
  methods: {
    initMap: function () {
      var mymap = new Map({
        target: 'map',
        layers: [
          new TileLayer({
            source: new XYZ({
              url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
          })
        ],
        view: new View({
          center: [19328172.72030281, -5320017.168648273],
          zoom: 5
        })
      })

      mymap.on('singleclick', function (evt) {
        console.log(evt.coordinate)
        console.log(mymap.getView().getZoom())
        console.log(mymap.getView().getCenter())

        // convert coordinate to EPSG-4326
        console.log(proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326'))
      })
    }
  }
}
</script>
