<template>
  <div id="map" :class="{'col-md-8':isOpen, 'col-md-11':!isOpen}" class="map" />
</template>

<script>
import { EventBus } from '../../store/event-bus.js'
import { delay } from 'underscore'
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
  computed: {
    isOpen () {
      return this.$store.state.showLeftPanel
    }
  },
  mounted: function () {
    this.initMap(),

    EventBus.$on('updatesize-map', timeout => {
      if (timeout === undefined) {
        this.updateSizeMap()
      } else {
        delay(this.updateSizeMap, timeout)
      }
    })
  },
  methods: {
    initMap () {
      var themap = new Map({
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

      // Update the store with the new map we made
      this.$store.commit('SET_MAP', themap)

      themap.on('singleclick', function (evt) {
        console.log(evt.coordinate)
        console.log(themap.getView().getZoom())
        console.log(themap.getView().getCenter())

        // convert coordinate to EPSG-4326
        console.log(proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326'))
      })
    },
    updateSizeMap () {
      this.$store.state.map.updateSize()
    }
  }
}
</script>
