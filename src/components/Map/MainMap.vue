<template>
  <div id="map" class="map">
    <div class="ol-custom ol-control">
      <button class="ol-zoom-in" type="button" title="Show Me">
        O
      </button>
    </div>
    <div v-if="isUploadingData" class="loadingBackground" />
    <div v-if="isUploadingData" class="loaderUpload" />
    <div v-if="isUploadingData">
      <p class="loadingInfo">
        Uploading data
      </p>
    </div>
  </div>
  <!-- <select id="layer-select" @change="onChangeBasemap($event)">
   <option value="'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'">openstreetmap</option>
 </select> -->
</template>

<script>

import { EventBus } from 'store/event-bus'
import { enableEventListeners, addSelectInteraction } from 'utils/mapUtils'
// import { flyTo } from 'utils/olHelper'
import { delay } from 'underscore'
// Import everything from ol
import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import XYZ from 'ol/source/XYZ'
// import OSM from 'ol/source/OSM'
// import TileJSON from 'ol/source/TileJSON'

// import VectorTileSource from 'ol/source/VectorTile'
// import VectorTileLayer from 'ol/layer/VectorTile'
// import MVT from 'ol/format/MVT'
import VectorSource from 'ol/source/Vector'
import VectorLayer from 'ol/layer/Vector'
import GeoJSON from 'ol/format/GeoJSON'
import { getWidth } from 'ol/extent' // getCenter,
import { get as getProjection, transform } from 'ol/proj'
import { Fill, Stroke, Style } from 'ol/style' // Circle as CircleStyle
import { Zoom, Attribution, ScaleLine } from 'ol/control'

export default {
  name: 'MapView',
  data() {
    return {

    }
  },
  computed: {
    mapView () {
      var view = new View({
        center: [19328172.72030281, -5320017.168648273],
        zoom: 5
      })
      return view
    },
    isUploadingData () {
      return this.$store.state.isUploadingData
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

    EventBus.$on('updateMapWidth', () => {
      console.log("it's a test")
      this.fixContentWidth()
    })

    EventBus.$on('addLayer', (geojsonObj) => {

      // Vector layer from a geojson object
      var gjsonLayer = new VectorLayer({
        source: new VectorSource({
          features: (new GeoJSON()).readFeatures(geojsonObj)
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

      this.$store.state.map.addLayer(gjsonLayer)

      var vectorExtent = this.getCorrectExtent(geojsonObj)
      console.log(transform([vectorExtent[0], vectorExtent[1]], 'EPSG:3857', 'EPSG:4326'))
      console.log(transform([vectorExtent[2], vectorExtent[3]], 'EPSG:3857', 'EPSG:4326'))
      this.$store.state.map.getView().fit(vectorExtent, { duration: 2000 })
      this.$store.state.isUploadingData = false

    })
  },
  methods: {
    initMap () {
      // strategy: ol.loadingstrategy.bbox

      var themap = new Map({
        target: 'map',
        layers: [
          // new TileLayer({
          //   source: new OSM()
          // })
          new TileLayer({
            source: new XYZ({
              url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
          })
          // new VectorTileLayer({
          //   source: new VectorTileSource({
          //     format: new MVT(),
          //     url: 'https://data.esp.gritool.com/christchurch/data/{z}/{x}/{y}.pbf',
          //     maxZoom: 24,
          //     type: 'base'
          //   })
          // })
        ],
        projection: 'EPSG:3857',
        view: this.mapView,
        controls: [
          new Zoom(),
          new ScaleLine(),
          new Attribution({
            collapsible: true
          })
        ]
      })

      // Update the store with the new map we made
      this.$store.commit('SET_MAP', themap)
      // Fix map height
      this.fixContentHeight()
      // Fix map width (only on Desktop since the sidebar is open on start)
      if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        this.fixContentWidth()
      }

      console.log(getProjection('EPSG:3857').getExtent())
      console.log(getProjection('EPSG:4326').getExtent())

      // Declaration of select interactions
      addSelectInteraction()

      // Declaration of map events
      enableEventListeners()

    },
    updateSizeMap () {
      this.$store.state.map.updateSize()
    },
    fixContentHeight () {
      var viewHeight = $(window).height()
      var navBarHeight = $("#navbar").outerHeight()
      var contentHeight = viewHeight - navBarHeight
      $("#map").height(contentHeight)
      this.$store.state.map.updateSize()
    },
    fixContentWidth () {
      var viewWidth = $(window).width()
      var sideBarWidth = $("#sidebar").width()
      var contentWidth
      if (parseInt($("#sidebar").css("left"), 10) < 0) {  // sidebar is closed (negative css left attribute)
        contentWidth = viewWidth
      } else { // sidebar is open (css left attribute is 0)
        contentWidth = viewWidth - sideBarWidth
      }

      $("#map").width(contentWidth)
      this.$store.state.map.updateSize()
    },
    getCorrectExtent (geojsonObj) {
      var tempLayer = new VectorLayer({
        source: new VectorSource({
          features: (new GeoJSON()).readFeatures(geojsonObj)
        })
      })
      // run a transform on all the feature coordinates (to change the range to 0 to 360) in OpenLayers
      var wrapWidth = getWidth(this.$store.state.map.getView().getProjection().getExtent());
      function wrapTransform(input, opt_output, opt_dimension) {
        var length = input.length;
        var dimension = opt_dimension !== undefined ? opt_dimension : 2;
        var output = opt_output !== undefined ? opt_output : new Array(length);
        var i, j;
        for (i = 0; i < length; i += dimension) {
          output[i] = input[i] < 0 ? input[i] + wrapWidth : input[i];
          for (j = dimension - 1; j >= 1; --j) {
            output[i + j] = input[i + j];
          }
        }
        return output;
      }
      tempLayer.getSource().forEachFeature(function(feature){
        feature.getGeometry().applyTransform(wrapTransform);
      })

      return tempLayer.getSource().getExtent()
    },
    displayFeatureInfo (pixel) {
      var features = []
      this.$store.state.map.forEachFeatureAtPixel(pixel, function(feature) {
       features.push(feature)
      })
      console.log(features)
    }
    // onChangeBasemap (e) {
    //   console.log(e.target.value)
    // }
  }
}
</script>
