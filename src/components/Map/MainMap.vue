<template>
  <div id="map" :class="[togglePanel ? 'col-md-6': 'col-md-12', 'map']">
    <div :class="[togglePanel ? 'col-sm-4': 'col-sm-2', 'card ol-control ol-custom']">
      <h6 id="legend" class="card-header">
        <div data-toggle="collapse" href="#collapse-legend" aria-expanded="true" aria-controls="collapse-legend">
          <font-awesome-icon icon="chevron-down" class="float-right" /> Legend
        </div>
      </h6>
      <div id="collapse-legend" class="collapse" aria-labelledby="legend">
        <div class="card-body">
          <div>
            <small><strong>Basemaps</strong></small>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio" checked @click="changeBasemap('osm')"><small>OpenStreetMap</small>
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio" @click="changeBasemap('terrain')"><small>Stamen Terrain</small>
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio" @click="changeBasemap('watercolor')"><small>Stamen Watercolor</small>
              </label>
            </div>
            <div class="form-check">
              <label class="form-check-label">
                <input type="radio" class="form-check-input" name="optradio" @click="changeBasemap('toner')"><small>Stamen Toner</small>
              </label>
            </div>
          </div>
          <div class="mt-2">
            <small><strong>Layers</strong></small>
            <small v-for="(layer, layerkey) in externalLayers" :key="layerkey">
              <div v-if="layer.visible">
                <div v-if="layer.geomtype == 0">
                  <p class="mb-1">
                    <svg class="svg">
                      <circle cx="7" cy="7" r="4" :fill="layer.style.getImage().getFill().getColor()" :stroke="layer.style.getImage().getStroke().getColor()" :stroke-width="layer.style.getImage().getStroke().getWidth()" />
                    </svg>
                    {{ layer.layername }}
                  </p>
                </div>
                <div v-if="layer.geomtype == 1">
                  <p class="mb-1">
                    <svg class="svg">
                      <line x1="14" y1="1" x2="1" y2="14" :stroke="layer.style.getStroke().getColor()" :stroke-width="layer.style.getStroke().getWidth()" />
                    </svg>
                    {{ layer.layername }}
                  </p>
                </div>
                <div v-if="layer.geomtype == 2">
                  <p class="mb-1">
                    <svg class="svg">
                      <rect x="1" y="1" width="12" height="12" rx="1" :fill="layer.style.getFill().getColor()" :stroke="layer.style.getStroke().getColor()" :stroke-width="layer.style.getStroke().getWidth()" />
                    </svg>
                    {{ layer.layername }}
                  </p>
                </div>
              </div>
            </small>
            <small v-for="(layer, layerkey) in internalLayers" :key="layerkey">
              <p v-if="layer.visible" class="mb-1">
                <img :src="layer.legendURL">
                <span v-if="layer.assigned_name">{{ layer.assigned_name }}</span>
                <span v-else>{{ layerkey }}</span>
              </p>
            </small>
          </div>
        </div>
      </div>
    </div>
    <div v-if="isUploadingData || isLoading" class="loading-background" />
    <div v-if="isUploadingData || isLoading" class="loader-upload" />
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

    <div id="restyleLayerModal" class="modal fade" data-keyboard="false" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Layer style</h5>
          </div>
          <div class="modal-body">
            <div class="container">
              <form>
                <div class="form-group">
                  <div class="mt-2">
                    <div v-if="isStyleInputVisible([0, 1, 2])">
                      <p class="mb-0">
                        <strong>Color</strong>
                      </p>
                      <input v-model="layerStyle.color" style="width:100%" type="color" class="form-control form-control-sm">
                    </div>
                    <div>
                      <p class="mt-4 mb-0">
                        <strong>Opacity</strong>
                      </p>
                      <div class="slidecontainer">
                        <input v-model="layerStyle.opacity" type="range" min="0" max="1" step="0.1" class="slider form-control form-control-sm">
                      </div>
                      <p class="float-right">
                        {{ layerStyle.opacity }}
                      </p>
                    </div>
                    <div v-if="isStyleInputVisible([1])">
                      <p class="mt-4 mb-0">
                        <strong>Line width</strong>
                      </p>
                      <div class="form-group container row">
                        <input v-model="layerStyle.linewidth" class="form-control form-control-sm col-sm-2" type="number" min="1">
                        <label class="col-sm-2 col-form-label col-form-label-sm">px</label>
                      </div>
                    </div>
                    <div v-if="isStyleInputVisible([0])">
                      <p class="mt-4 mb-0">
                        <strong>Point size</strong>
                      </p>
                      <div class="form-group container row">
                        <input v-model="layerStyle.pointsize" class="form-control form-control-sm col-sm-2" type="number" min="1">
                        <label class="col-sm-2 col-form-label col-form-label-sm">px</label>
                      </div>
                    </div>
                  </div>
                  <div v-if="isStyleInputVisible([0, 2])" class="mt-4">
                    <p class="mb-0">
                      <strong>Border color</strong>
                    </p>
                    <input v-model="layerStyle.bordercolor" class="form-control form-control-sm" style="width:100%" type="color">
                    <p class="mt-4 mb-0">
                      <strong>Border width</strong>
                    </p>
                    <div class="form-group container row">
                      <input v-model="layerStyle.borderwidth" class="form-control form-control-sm col-sm-2" type="number" min="0">
                      <label class="col-sm-2 col-form-label col-form-label-sm">px</label>
                    </div>
                  </div>
                  <div v-if="isStyleInputVisible([1, 2])">
                    <div class="form-check">
                      <input id="dashedLine" v-model="layerStyle.dashedline" type="checkbox" class="form-check-input">
                      <label class="form-check-label" for="dashedLine">Dashed line</label>
                    </div>
                    <div v-if="layerStyle.dashedline" class="form-group container row">
                      <label class="col-form-label col-form-label-sm mr-2">Drawn line</label>
                      <input v-model="layerStyle.drawnline" class="form-control form-control-sm col-sm-2" type="number" min="1">
                      <label class="col-form-label col-form-label-sm ml-1">px</label>
                      <label class="col-form-label col-form-label-sm ml-5 mr-2">Blank space</label>
                      <input v-model="layerStyle.blankspace" class="form-control form-control-sm col-sm-2" type="number" min="1">
                      <label class="col-form-label col-form-label-sm ml-1">px</label>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-success btn-ok" @click="createSLD()">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- <select id="layer-select" @change="onChangeBasemap($event)">
   <option value="'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'">openstreetmap</option>
 </select> -->
</template>

<script>

import { EventBus } from 'store/event-bus'
import { addGeoserverWMS, zoomToGeoserverVectorLayer, zoomToGeoserverLayerBbox, setSLDstyle } from 'utils/internalMapServices'
import { enableEventListeners, getCorrectExtent, createGeojsonLayer, createGeojsonVTlayer } from 'utils/mapUtils'
import { extLayersObj } from 'utils/objects'
import { delay, each, isString } from 'underscore'
// Import everything from ol
import Map from 'ol/Map'
import View from 'ol/View'
import {Tile as TileLayer} from 'ol/layer'
import Stamen from 'ol/source/Stamen'
// import XYZ from 'ol/source/XYZ'
import OSM from 'ol/source/OSM'
// import TileJSON from 'ol/source/TileJSON'
// import VectorSource from 'ol/source/Vector'
// import VectorLayer from 'ol/layer/Vector'
// import { Point, MultiPoint, LineString, MultiLineString} from 'ol/geom'
// import GeoJSON from 'ol/format/GeoJSON'
// import { getWidth } from 'ol/extent' // getCenter,
import Overlay from 'ol/Overlay'
// import { Fill, Stroke, Style } from 'ol/style' // Circle as CircleStyle
import { Zoom, Attribution, ScaleLine } from 'ol/control'
// import { tile } from 'ol/loadingstrategy' // bbox as bboxStrategy,
// import { createXYZ } from 'ol/tilegrid'


export default {
  name: 'MapView',
  data() {
    return {
      features_info: '',
      layersFeaturesPopupCount: 0,
      nExpectedCount: null,
      layerStyle: {
         color: '#ffffff',
         opacity: 1,
         linewidth: 1,
         pointsize: 6,
         bordercolor: '#000000',
         borderwidth: 1,
         dashedline: false,
         drawnline: 5,
         blankspace: 8,
         layername: null
       }
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
    isLoading () {
      return this.$store.state.isLoading
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

    EventBus.$on('refreshLayer', (layername) => {
      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === layername) {
          layer.getSource().updateParams({"time": Date.now()})
          this.refreshInternalLegend()
        }
      })
    })

    EventBus.$on('addLayer', (payload, geoserverLayer=true) => {
      var geojsonObj = payload.jsonlayer
      var layername = payload.filename

      if (geoserverLayer) {
        EventBus.$emit('createLayer', layername, 'internal')
        this.$store.commit('ADD_INTERNAL_LAYER', payload)
        if (payload.geomtype != 'raster') {
          zoomToGeoserverVectorLayer(layername)
        } else {
          zoomToGeoserverLayerBbox(layername)
        }
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

    EventBus.$on('defineExpectedCount', (count) => {
      this.nExpectedCount = count
    })

    EventBus.$on('showLayersFeaturesPopup', (obj) => {
      var element = this.mapPopup.getElement()
      var coordinate = obj.coordinate

      if (obj.hasOwnProperty('features')) {
        var features = obj.features
        var layername = obj.layername
        var assignedname = this.$store.state.internalLayers[layername] ? this.$store.state.internalLayers[layername].assigned_name : ''

        if (this.features_info !== '') {
          this.features_info = this.features_info + '<hr />'
        }

        var feature_properties
        each(features, (f) => {
          try {
            feature_properties = f.getProperties()
          } catch (e) {
            if (f.hasOwnProperty('properties')) {
              feature_properties = f.properties
            } else {
              feature_properties = f
            }
          }
          var layertitle = assignedname ? assignedname : layername
          this.features_info = this.features_info + '<p class="text-center mb-2">Layer: ' + layertitle + '</p>'

          each(feature_properties, (value, key) => {
            if (key.toLowerCase() != "geometry" && key.toLowerCase() != "bbox" && key.toLowerCase() != "id" && value != null && value != "") {
              if (isString(value) && value.includes('http')) {
                this.features_info = this.features_info + '<p><strong>' + key.replace(/_/g, " ") + ':</strong> <a href="' + value + '" target="_blank">' + value + '</a></p>'
              } else {
                this.features_info = this.features_info + '<p><strong>' + key.replace(/_/g, " ") + ':</strong> ' + value + '</p>'
              }
            }
          })
        })
      }

      this.layersFeaturesPopupCount++

      if (this.layersFeaturesPopupCount === this.nExpectedCount) {
        $(element).popover('dispose')
        if (this.features_info != "") {
          this.mapPopup.setPosition(coordinate)
          $(element).popover({
            placement: 'top',
            animation: false,
            html: true,
            title: 'Feature Info <a href="#" class="close" data-dismiss="alert">&times;</a>',
            template:	'<div class="popover feature-popup" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
            content: this.features_info
          })
          $(element).popover('show')
        }
        this.layersFeaturesPopupCount = 0
        this.features_info = ''
      }
    })

    EventBus.$on('closeMapPopup', () => {
      var element = this.mapPopup.getElement()
      $(element).popover('dispose')
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

    EventBus.$on('zoomToLayer', (payload) => {
      if (payload.layerType === "internal") {
        if (this.internalLayers[payload.layerName].geomtype != 3) {
          // // for vector layers created with JDBCVirtualTable, the bbox is not generated,
          // //so it's necessary to getFeatures from WFS to get the extent (but it takes more time)
          // zoomToGeoserverVectorLayer(payload.layerName)
          zoomToGeoserverLayerBbox(payload.layerName)
        } else {
          zoomToGeoserverLayerBbox(payload.layerName)
        }
      }
    })

    EventBus.$on('restyleLayer', (payload) => {
      if (payload.layerType === "internal") {
        // Set the layer for style editing
        this.layerStyle = {
           color: '#ffffff',
           opacity: 1,
           linewidth: 1,
           pointsize: 6,
           bordercolor: '#000000',
           borderwidth: 1,
           dashedline: false,
           drawnline: 5,
           blankspace: 8,
           layername: payload.layerName
         }
        // Get current geoserver layer style (SLD) and fill the layerStyle object accordingly
        this.$store.dispatch('getInternalLayerStyle', payload.layerName)
        .then((response) => {

          // Remove the sld: from each tag and parse the string to xml
          var stringxml = response.body.sld.replace(/sld:/g, "")
          var xml = $.parseXML(stringxml)

          if (response.body.stylename !== 'generic') {
            if ($(xml).find("CssParameter[name='stroke']").text()) {
              this.layerStyle.bordercolor = $(xml).find("CssParameter[name='stroke']").text()
              this.layerStyle.color = $(xml).find("CssParameter[name='stroke']").text()
            }
            if ($(xml).find("CssParameter[name='fill']").text()) {
              this.layerStyle.color = $(xml).find("CssParameter[name='fill']").text()
            }
            if ($(xml).find("CssParameter[name='fill-opacity']").text()) {
              this.layerStyle.opacity = $(xml).find("CssParameter[name='fill-opacity']").text()
            }
            if ($(xml).find("CssParameter[name='stroke-opacity']").text()) {
              this.layerStyle.opacity = $(xml).find("CssParameter[name='stroke-opacity']").text()
            }
            if ($(xml).find("Opacity").text()) {
              this.layerStyle.opacity = $(xml).find("Opacity").text()
            }
            if ($(xml).find("CssParameter[name='stroke-width']").text()) {
              this.layerStyle.borderwidth = $(xml).find("CssParameter[name='stroke-width']").text()
              this.layerStyle.linewidth = $(xml).find("CssParameter[name='stroke-width']").text()
            }
            if ($(xml).find("CssParameter[name='stroke-dasharray']").text()) {
              var dasharray = $(xml).find("CssParameter[name='stroke-dasharray']").text().split(" ")
              this.layerStyle.dashedline = true
              this.layerStyle.drawnline = dasharray[0]
              this.layerStyle.blankspace = dasharray[1]
            }
            if ($(xml).find("Size").text()) {
              this.layerStyle.pointsize = $(xml).find("Size").text()
            }
          }

          $('#restyleLayerModal').modal('show')
        })
      }
    })

  },
  methods: {

    initMap () {

      var themap = new Map({
        target: 'map',
        layers: [
          new TileLayer({
            name: 'Basemap',
            zIndex: 0,
            source: new OSM()
          })
          // new TileLayer({
          //   name: 'Basemap',
          //   source: new XYZ({
          //     url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
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
    },
    createSLD () {
      setSLDstyle(this.layerStyle)
      $('#restyleLayerModal').modal('hide')
    },
    getInternalLayerLegend (layerkey) {
      return process.env.WEB_HOST + ":8080/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=storyapp:" + layerkey + "&myData:" + Math.random()
    },
    refreshInternalLegend () {
      each(this.internalLayers, (layer, layerkey) => {
        layer.legendURL = this.getInternalLayerLegend(layerkey)
      })
    },
    isStyleInputVisible (geomTypeArray) {
      if (this.internalLayers[this.layerStyle.layername]) {
        return geomTypeArray.includes(this.internalLayers[this.layerStyle.layername].geomtype)
      }
    },
    changeBasemap (basemap_name) {
      EventBus.$emit('removeLayer', 'Basemap')

      var basemap_layer
      if (basemap_name === 'osm') {
        basemap_layer = new TileLayer({
                          name: 'Basemap',
                          zIndex: 0,
                          source: new OSM()
                        })
      } else {
        basemap_layer = new TileLayer({
                          name: 'Basemap',
                          zIndex: 0,
                          source: new Stamen({
                            layer: basemap_name
                          })
                        })
      }
      this.map.addLayer(basemap_layer)
    }
  }
}
</script>
