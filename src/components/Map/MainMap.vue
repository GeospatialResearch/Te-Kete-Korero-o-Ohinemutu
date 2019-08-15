<template>
  <div id="map" :class="[togglePanel ? 'col-md-8': 'col-md-12', 'map']">
    <div class="card ol-control ol-custom col-xs-3 col-sm-3 ">
      <h5 class="card-header">
        <a id="heading-example" data-toggle="collapse" href="#collapse-example" aria-expanded="true" aria-controls="collapse-example" class="d-block">
          Legend
          <i class="fa fa-chevron-down pull-right" />
        </a>
      </h5>
      <div id="collapse-example" class="col-xs-4  collapse" aria-labelledby="heading-example">
        <div class="card-body">
          <small v-for="(layer, layerkey) in externalLayers" :key="layerkey">
            <div v-if=" layer.legend "> <span v-html=" layer.legend " /> {{ layer.layername }}
            </div>
          </small>
        </div>
      </div>
    </div>
    <div v-if="isUploadingData" class="loading-background" />
    <div v-if="isUploadingData" class="loader-upload" />
    <div v-if="isUploadingData">
      <p class="loading-info text-center">
        Uploading data... <br>
        This may take several minutes
      </p>
    </div>
    <div class="resolution-box text-center">
      <p>
        <small>Resolution:</small>
      </p>
      <p>
        <small>{{ mapResolution }}</small>
      </p>
      <!-- <p>
        <small>Zoom: {{ mapZoom }}</small>
      </p> -->
    </div>
    <div style="display: none;">
      <div id="feature_popup" />
    </div>
  </div>
  <!-- <select id="layer-select" @change="onChangeBasemap($event)">
   <option value="'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'">openstreetmap</option>
 </select> -->
</template>

<script>

import { EventBus } from 'store/event-bus'
import { addGeoserverWMS, zoomToGeoserverLayer } from 'utils/internalMapServices'
import { enableEventListeners, addInteractions, getCorrectExtent, createGeojsonLayer, createGeojsonVTlayer } from 'utils/mapUtils'
import { extLayersObj } from 'utils/objects'
import { delay, each } from 'underscore'
// Import everything from ol
import Map from 'ol/Map'
import View from 'ol/View'
import {Tile as TileLayer} from 'ol/layer'
// import Stamen from 'ol/source/Stamen'
import XYZ from 'ol/source/XYZ'
// import OSM from 'ol/source/OSM'
// import TileJSON from 'ol/source/TileJSON'
// import VectorSource from 'ol/source/Vector'
// import VectorLayer from 'ol/layer/Vector'
// import GeoJSON from 'ol/format/GeoJSON'
// import { getWidth } from 'ol/extent' // getCenter,
import Overlay from 'ol/Overlay'
// import { Fill, Stroke, Style } from 'ol/style' // Circle as CircleStyle
import { Zoom, Attribution, ScaleLine } from 'ol/control'
// import { tile } from 'ol/loadingstrategy' // bbox as bboxStrategy,
// import { createXYZ } from 'ol/tilegrid'


$(document).on("click", ".popover .close" , function(){
  $(this).parents(".popover").popover('hide');
});

export default {
  name: 'MapView',
  data() {
    return {
    }
  },
  computed: {

    mapView () {
      var view = new View({
        projection: 'EPSG:3857',
        center: [19410113.214624517, -5044843.866821633],
        // projection: 'EPSG:4326',  // this distorts the view
        // center: [172.79296875, -41.868896484375],
        zoom: 6,
        minZoom: 2
      })
      return view
    },
    mapPopup () {
      var popup = new Overlay({
        element: $("#feature_popup")[0] // the same as document.getElementById('feature_popup')
      })
      return popup
    },
    togglePanel (){
      return this.$store.state.isPanelOpen
    },
    isUploadingData () {
      return this.$store.state.isUploadingData
    },
    externalLayers () {
      return this.$store.state.externalLayers
    },
    internalLayers () {
      return this.$store.state.internalLayers
    },
    map () {
      return this.$store.state.map
    },
    mapResolution () {
      return this.$store.state.map_resolution.toFixed(1)
    },
    mapZoom () {
      return this.$store.state.map_zoom.toFixed(1)
    }
  },
  created: function () {
    // Set external layers
    this.$store.commit('SET_EXTERNAL_LAYERS', $.extend(true, {}, extLayersObj))

    // Set internal layers and other stuff before creating the map
    Promise.all([
      this.$store.dispatch('getDatasets')
    ]).then(() => {
      // Create the map
      this.initMap()
    }).catch((e) => {
      console.error("Map loading failed with error: ", e)
    })
  },
  mounted: function () {

    // ------------------
    // EventBus events
    // ------------------
    EventBus.$on('adjustMap', (timeout) => {
      if (timeout === undefined) {
        this.updateSizeMap()
      } else {
        delay(this.updateSizeMap, timeout)
      }
    })

    EventBus.$on('updateMapWidth', () => {
      this.fixContentWidth()
    })

    EventBus.$on('createLayer', (layer, servType) => {
      if (servType === 'external') {
        extLayersObj[layer.keyname].functionToCall.call(null, layer)
      } else if (servType === 'internal') {
        addGeoserverWMS(layer)
      }
    })

    EventBus.$on('removeLayer', (layername) => {
      var lyr_list = []
      this.map.getLayers().forEach(function (layer) {
        if (layer.get('name') === layername) {
          lyr_list.push(layer)
        }
      })
      each(lyr_list, (l) => {
        this.map.removeLayer(l)
      })
    })

    EventBus.$on('addLayer', (payload, geoserverLayer=true) => {

      var geojsonObj = payload.jsonlayer
      var layername = payload.filename

      if (geoserverLayer) {
        EventBus.$emit('createLayer', layername, 'internal')
        this.$store.commit('ADD_INTERNAL_LAYER', layername)
        zoomToGeoserverLayer(layername)
      } else {
        // conditional to the dataset size (number of features)
        if (geojsonObj.features.length > 10000) {
          // Vector tile layer using geojson-vt
          createGeojsonVTlayer(geojsonObj)
        } else {
          // Vector layer from a geojson object
          createGeojsonLayer(geojsonObj)
        }

        // get extention to zoom to data
        var vectorExtent =  getCorrectExtent(geojsonObj)
        this.$store.state.map.getView().fit(vectorExtent, { duration: 2000 })
      }
    })

    EventBus.$on('showMapPopup', (obj) => {
      var element = this.mapPopup.getElement()
      var coordinate = obj.coordinate
      var features = obj.features

      var features_info = ''

      // TODO: show all features info, not only the one at the top
      each(features, (f) => {
        var feature_properties = f.getProperties()
        each(feature_properties, (value, key) => {
          if (key != "geometry" && value != null) {
            features_info = features_info + '<p><strong>' + key.replace(/_/g, " ") + ':</strong> ' + value + '</p>'
          }
        })
      })

      $(element).popover('dispose')
      if (features.length > 0) {
        this.mapPopup.setPosition(coordinate)
        $(element).popover({
          placement: 'top',
          animation: false,
          html: true,
          title: 'Feature Info <a href="#" class="close" data-dismiss="alert">&times;</a>',
          template:	'<div class="popover feature-popup" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
          content: features_info
        })
        $(element).popover('show')
      }
    })

    EventBus.$on('resolutionNotification', () => {
      var mapResolution = this.map.getView().getResolution()

      each(this.externalLayers, (layer, key) => {

        if (layer.hasOwnProperty('maxresolution')) {
          if (layer.visible && mapResolution > layer.maxresolution) {
            if (window['resolutionNotify_' + key] == null || window['resolutionNotify_' + key] == undefined) {
              window['resolutionNotify_' + key] = $.notify({
                                              message: "<strong>Resolution Info</strong><br />The layer <i>" + layer.layername + "</i> is active but to be visible on the map you must zoom in to the <strong>Resolution " + layer.maxresolution + "</strong>. <br />Please, zoom to the right resolution or deactivate the layer." ,
                                              icon: 'fa fa-exclamation-circle'
                                            }, {
                                              type: 'warning',
                                              z_index: 2000,
                                              animate: {
                                                enter: 'animated fadeInDown',
                                                exit: 'animated fadeOutUp'
                                              },
                                              allow_dismiss: false,
                                              delay: 0,
                                              placement: {
                                                from: "top",
                                                align: "center"
                                              },
                                            })
            }
          } else {
            if (window['resolutionNotify_' + key] != null && window['resolutionNotify_' + key] != undefined) {
              window['resolutionNotify_' + key].close()
              window['resolutionNotify_' + key] = null
            }
          }
        }

      })
    })

  },
  methods: {

    initMap () {

      var themap = new Map({
        target: 'map',
        layers: [
          // new TileLayer({
          //   source: new OSM()
          // }) OR
          new TileLayer({
            name: 'Basemap',
            source: new XYZ({
              url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
          }),
          // new TileLayer({
          //   source: new Stamen({
          //     layer: 'terrain'
          //   })
          // }),
          // new TileLayer({
          //   source: new Stamen({
          //     layer: 'terrain-labels'
          //   })
          // })
        ],
        view: this.mapView,
        controls: [
          new Zoom(),
          new ScaleLine(),
          new Attribution()
        ]
      })

      // Update the store with the new map we made
      this.$store.commit('SET_MAP', themap)

      // Set map resolution and zoom
      this.$store.commit('SET_MAP_RESOLUTION', themap.getView().getResolution())
      this.$store.commit('SET_MAP_ZOOM', themap.getView().getZoom())

      // Add external map services to the map if visible
      each(this.externalLayers, (layer) => {
        if (layer.visible) {
          EventBus.$emit('createLayer', layer, 'external') // we need to send the configurations of the layer
        }
      })

      // Add internal map services to the map (geoserver) if visible
      each(this.internalLayers, (layer, layerkey) => {
        if (layer.visible) {
          EventBus.$emit('createLayer', layerkey, 'internal') // the layerkey is enough to request the geoserver layer
        }
      })

      // Declaration of select interactions
      addInteractions()

      // Declaration of map events
      enableEventListeners()

      // Popup where the user clicked
      themap.addOverlay(this.mapPopup)

      // Fix map height
      this.fixContentHeight()
      // Fix map width (only on Desktop since the sidebar is open on start)
      if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        this.fixContentWidth()
      }

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
      $("#map").width(100)
      delay(this.updateSizeMap, 50)
    }
  }
}
</script>
