<template>
  <!-- <div id="map" :class="[togglePanel ? 'col-md-7': 'col-md-12', 'map']"> -->
  <div id="map" :class="[getOrientation === 'portrait' ? {'col-sm-12 col-xs-12 map-top':togglePanel, 'col-sm-12 col-xs-12 map':!togglePanel}: {'col-sm-7 col-xs-7 map':togglePanel, 'col-sm-12 col-xs-12 map':!togglePanel}]">
    <div class="card ol-control ol-custom">
      <h6 id="legend" class="card-header pt-2 pb-2">
        <div data-toggle="collapse" href="#collapse-legend" aria-expanded="true" aria-controls="collapse-legend">
          <small>
            <font-awesome-icon icon="list" />
          </small>
          <span class="align-middle"><font-awesome-icon icon="chevron-down" class="float-right" /> Legend &nbsp;&nbsp;&nbsp;&nbsp;</span>
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
          <div class="mt-2 printme_2">
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
                <span v-else>{{ layer.name }}</span>
              </p>
            </small>
            <small v-if="allStoriesGeomsLayer">
              <div v-if="allStoriesGeomsLayer.style && allStoriesGeomsLayer.visible">
                <p class="mb-1">
                  <svg class="svg">
                    <circle cx="7" cy="7" r="4" :fill="allStoriesGeomsLayer.style.getImage().getFill().getColor()" :stroke="allStoriesGeomsLayer.style.getImage().getStroke().getColor()" :stroke-width="6" />
                  </svg>
                  Geometries in Narratives
                </p>
              </div>
            </small>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isDrawMode" class="ol-control draw-buttons">
      <button v-if="!drawnFeature.geometry" type="button" title="Add point coordinate" @click="addPointCoord()">
        <i><font-awesome-icon icon="map-marked-alt" color="white" style="padding-left:2px; padding-right:2px;" /></i>
      </button>
      <button v-if="!drawnFeature.geometry" type="button" title="Draw point" @click="drawGeom('Point')">
        <img src="static/img/drawPoint.png" class="draw-img">
      </button>
      <button v-if="!drawnFeature.geometry" type="button" title="Draw line" @click="drawGeom('LineString')">
        <img src="static/img/drawLine.png" class="draw-img">
      </button>
      <button v-if="!drawnFeature.geometry" type="button" title="Draw polygon" @click="drawGeom('Polygon')">
        <img src="static/img/drawPolygon.png" class="draw-img">
      </button>
      <button v-if="drawnFeature.geometry && !drawnFeature.id" type="button" title="Remove geometry" @click="deleteGeom()">
        <img src="static/img/trash.png" class="draw-img">
      </button>
      <button type="button" style="background-color: #a21515;" title="Stop drawing geometry" @click="stopDrawing()">
        <i><font-awesome-icon icon="ban" color="white" /></i>
      </button>
    </div>

    <div v-if="isReuseMode" class="ol-control draw-buttons">
      <button type="button" style="background-color: #a21515;" title="Stop reusing geometry" @click="stopReuse()">
        <i><font-awesome-icon icon="ban" color="white" /></i>
      </button>
    </div>

    <div v-if="isUploadingData || isLoading" class="loading-background" />
    <div v-if="isUploadingData || isLoading" class="loader-loading" :style="togglePanel?'left: 38%;':'left: 55%;'" />
    <div v-if="isUploadingData">
      <p class="loading-info text-center" :style="togglePanel?'left: 34.5%;':'left: 51.5%;'">
        Uploading data... <br>
        This may take several minutes
      </p>
    </div>

    <div class="resolution-box text-center">
      <p>
        <small>Resolution: {{ mapResolution }}</small>
      </p>
      <!-- <p>
        <small>Zoom: {{ mapZoom }}</small>
      </p> -->
    </div>

    <!-- Map services feature popup -->
    <div style="display: none;">
      <div id="feature_popup" />
    </div>

    <!-- Content of the menu -->
    <div style="display: none;">
      <div id="storygeom_overlay">
        <!-- <div class="col-md-12">
        <div class="row"> -->
        <div class="col-sm-12">
          <div class="d-flex flex-sm-row justify-content-between">
            <h6 class="col-md-8">
              <span v-if="isGeomMediaMode"><strong>Feature Media Manager</strong></span>
              <span v-else><strong>Story Feature Info</strong></span>
            </h6>
            <div class="col-md-4">
              <font-awesome-icon v-if="!isDrawMode && !isGeomMediaMode" icon="times" class="float-right pointer" size="lg" @click="hideStoryGeomInfo()" />
              <font-awesome-icon v-if="!isDrawMode && isGeomMediaMode && drawnFeature.geomAttribMedia.length==0" icon="times" class="float-right pointer" size="lg" @click="$store.commit('SET_GEOM_MEDIA_MODE', false)" />
              <font-awesome-icon v-if="isDrawMode && !drawnFeature.id" icon="times" class="float-right pointer" size="lg" @click="deleteGeom()" />
            </div>
          </div>
        </div>
        <hr class="mt-0 mb-0">
        <!-- <div class="row"> -->
        <div class="d-flex flex-sm-row justify-content-between">
          <div class="col-sm-5">
            <form id="geomAttrForm" class="ml-2">
              <p v-if="isDrawMode" class="text-muted mb-0 mt-2">
                <font-awesome-icon icon="info-circle" />
                <small>Snap the yellow geometry and drag the blue point to change the feature's shape.</small>
              </p>
              <div>
                <label class="mt-3"><b>Name</b></label>
                <div class="col-sm-12 col-form-label col-form-label-sm">
                  <div v-if="storyViewLang === 'eng'">
                    <input v-if="isDrawMode" v-model="drawnFeature.name.eng" required type="text" class="form-control form-control-sm" placeholder="Name of the geographical feature">
                    <div v-else>
                      <span v-if="drawnFeature.name.eng">{{ drawnFeature.name.eng }}</span>
                      <span v-else class="text-muted font-italic">No name defined in English</span>
                    </div>
                  </div>
                  <div v-if="storyViewLang === 'mao'">
                    <input v-if="isDrawMode" v-model="drawnFeature.name.mao" required type="text" class="form-control form-control-sm" placeholder="Ingoa o te wāhi whenua">
                    <div v-else>
                      <span v-if="drawnFeature.name.mao">{{ drawnFeature.name.mao }}</span>
                      <span v-else class="text-muted font-italic">No name defined in Te Reo</span>
                    </div>
                  </div>
                </div>
                <label class="mt-3"><b>Description</b></label>
                <div class="col-sm-12 col-form-label col-form-label-sm">
                  <div v-if="storyViewLang === 'eng'">
                    <textarea v-if="isDrawMode" v-model="drawnFeature.description.eng" required rows="4" class="form-control form-control-sm" placeholder="Description of what the geographical feature represents" />
                    <div v-else>
                      <span v-if="drawnFeature.description.eng">{{ drawnFeature.description.eng }}</span>
                      <span v-else class="text-muted font-italic">No description defined in English</span>
                    </div>
                  </div>
                  <div v-if="storyViewLang === 'mao'">
                    <textarea v-if="isDrawMode" v-model="drawnFeature.description.mao" required rows="4" class="form-control form-control-sm" placeholder="Whakaahuatanga o te tohu o te waahi whenua" />
                    <div v-else>
                      <span v-if="drawnFeature.description.mao">{{ drawnFeature.description.mao }}</span>
                      <span v-else class="text-muted font-italic">No description defined in Te Reo</span>
                    </div>
                  </div>
                </div>
              </div>
            </form>
            <div class="pt-3">
              <button v-if="isDrawMode" type="button" class="btn btn-sm btn-danger" @click="stopDrawing()">
                Cancel
              </button>
              <button v-if="isDrawMode" type="button" class="btn btn-sm btn-success" @click="saveGeomAttrb()">
                <span v-if="!drawnFeature.id">Add feature to story</span>
                <span v-else>Update feature</span>
              </button>
            </div>
          </div>
          <div v-if="drawnFeature.geometry" :class="[isGeomMediaMode ? '': 'pt-4', 'col-7 pl-5 pr-5 geometry-media-section']">
            <div v-if="isGeomMediaMode" class="mb-1 text-center">
              <button type="button" class="btn btn-sm btn-primary" @click="addMediaFileToGeom()">
                Add new media
              </button>
              <button v-if="drawnFeature.geomAttribMedia.length > 0" type="button" class="btn btn-sm btn-success" @click="saveCaptions()">
                Save
              </button>
              <!-- <button type="button" class="btn btn-sm btn-secondary" data-dismiss="modal" @click="hideAddNewMedia()">
                Close
              </button> -->
            </div>
            <div v-if="drawnFeature.geomAttribMedia" class="carousel slide" data-ride="carousel" data-interval="false">
              <div class="row m-0">
                <div class="col-1 p-0">
                  <a class="carousel-control-prev" role="button" @click="slidePrev()">
                    <font-awesome-icon v-if="drawnFeature.geomAttribMedia.length > 1" icon="chevron-circle-left" color="black" class="pointer" size="lg" />
                  </a>
                </div>
                <div class="col-10 p-0">
                  <p v-if="drawnFeature.geomAttribMedia.length > 0" class="text-center mb-1 media-caption">
                    <small>{{ drawnFeature.geomAttribMedia.length }} media</small>
                  </p>
                  <p v-if="!drawnFeature.geomAttribMedia || drawnFeature.geomAttribMedia.length == 0" class="text-center mb-1 media-caption">
                    No media files
                  </p>
                  <div class="carousel-inner text-center">
                    <div v-for="(media, idx) in drawnFeature.geomAttribMedia" :key="media.id" class="carousel-item" :class="{ active: idx==0 }">
                      <div v-if="media.media_type == 'IMG'">
                        <img :src="mediaRoot + media.mediafile_name" alt="" class="geometry-media">
                        <i v-if="isGeomMediaMode"><font-awesome-icon icon="trash-alt" size="lg" color="red" class="positioner-delete" title="Delete media" @click="deleteMediaFromGeom(media)" /></i>
                        <span v-else class="fa-stack fa-1x positioner-magnify" @click="magnifyImage(media)">
                          <i class="fa fa-circle fa-stack-2x icon-background" />
                          <i class="fa fa-search-plus fa-stack-1x" />
                        </span>
                      </div>
                      <div v-if="media.media_type == 'VIDEO'">
                        <video controls controlsList="nodownload" class="geometry-media">
                          <source :src="mediaRoot + media.mediafile_name" type="video/mp4">
                          Your browser does not support the video tag.
                        </video>
                        <i v-if="isGeomMediaMode"><font-awesome-icon icon="trash-alt" size="lg" color="red" class="positioner-delete" title="Delete media" @click="deleteMediaFromGeom(media)" /></i>
                      </div>
                      <div v-if="media.media_type == 'AUDIO'">
                        <audio controls controlsList="nodownload">
                          <source :src="mediaRoot + media.mediafile_name" type="audio/mpeg">
                          Your browser does not support the audio element.
                        </audio>
                        <i v-if="isGeomMediaMode"><font-awesome-icon icon="trash-alt" size="lg" color="red" class="positioner-delete" title="Delete media" @click="deleteMediaFromGeom(media)" /></i>
                      </div>
                      <div v-if="isGeomMediaMode">
                        <textarea v-show="media.media_description && storyViewLang === 'eng'" v-model="media.media_description.eng" rows="1" class="form-control form-control-sm mt-2" placeholder="Media caption" />
                        <textarea v-show="media.media_description && storyViewLang === 'mao'" v-model="media.media_description.mao" rows="1" class="form-control form-control-sm mt-2" placeholder="Media caption" />
                      </div>
                      <p v-else class="media-caption">
                        <span v-show="media.media_description && storyViewLang === 'eng'">{{ media.media_description.eng }}</span>
                        <span v-show="media.media_description && storyViewLang === 'mao'">{{ media.media_description.mao }}</span>
                      </p>
                    </div>
                  </div>
                </div>
                <div class="col-1 p-0">
                  <a class="carousel-control-next" role="button" @click="slideNext()">
                    <font-awesome-icon v-if="drawnFeature.geomAttribMedia.length > 1" icon="chevron-circle-right" color="black" class="pointer" size="lg" />
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <div id="drawInfoModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content modal-margin-top">
          <div class="modal-header">
            <h5>Attention</h5>
          </div>
          <div class="modal-body text-center">
            <h6>
              Use the drawing buttons along the left margin of the map to locate your narrative as a point (
              <img src="static/img/drawPoint.svg">
              ), a line (
              <img src="static/img/drawLine.svg">
              ) or a polygon(
              <img src="static/img/drawPolygon.svg">
              ).
              <br><br>
              Use the button
              <button style="background-color: #a21515;" disabled>
                <i><font-awesome-icon icon="ban" color="white" /></i>
              </button>
              to stop drawing.
            </h6>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Got it!
            </button>
          </div>
        </div>
      </div>
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
                  <!-- <div class="form-check">
                    <input id="classifyByProperty" v-model="layerStyle.classifyby" type="checkbox" class="form-check-input">
                    <label class="form-check-label" for="classifyByProperty">Classify by property</label>
                  </div>
                  <select v-if="layerStyle.classifyby" v-model="layerStyle.classifybyproperty" required class="form-control form-control-sm mb-3">
                    <option key="SELECT" value="" selected disabled>
                      Select layer property
                    </option>
                    <option v-for="(property, index) in layerProperties" :key="`property-${index}`" :value="property">
                      {{ property }}
                    </option>
                  </select> -->
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

    <div id="restyleStoryGeomModal" class="modal fade" data-keyboard="false" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Feature style</h5>
          </div>
          <div class="modal-body">
            <div class="container">
              <form>
                <div class="form-group">
                  <div class="mt-2">
                    <div>
                      <p class="mb-0">
                        <strong>Color</strong>
                      </p>
                      <input v-model="storyGeomStyle.color" style="width:100%" type="color" class="form-control form-control-sm">
                    </div>
                    <div>
                      <p class="mt-4 mb-0">
                        <strong>Opacity</strong>
                      </p>
                      <div class="slidecontainer">
                        <input v-model="storyGeomStyle.opacity" type="range" min="0" max="1" step="0.1" class="slider form-control form-control-sm">
                      </div>
                      <p class="float-right">
                        {{ storyGeomStyle.opacity }}
                      </p>
                    </div>
                    <div>
                      <p class="mt-4 mb-0">
                        <strong>Line width</strong>
                      </p>
                      <div class="form-group container row">
                        <input v-model="storyGeomStyle.linewidth" class="form-control form-control-sm col-sm-2" type="number" min="1">
                        <label class="col-sm-2 col-form-label col-form-label-sm">px</label>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelsetOLStyle()">
              Cancel
            </button>
            <button class="btn btn-success btn-ok" @click="setOLStyle()">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="deleteGeomMediaModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Attention</h5>
          </div>
          <div class="modal-body text-center">
            <h6>Are you sure you want to delete this media from the geometry?</h6>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" @click="deleteGeomMedia()">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="geomsReuseModal" class="modal fade" data-backdrop="static" data-keyboard="false">
      <div class="modal-dialog modal-lg">
        <div class="modal-content modal-margin-top">
          <div class="modal-header">
            <h3 class="mb-0">
              Reuse geometries in the story
            </h3>
          </div>
          <div class="modal-body pt-0 pb-0 ml-2">
            <div v-for="geom in geomsForReuse" :key="geom.id" class="mt-4">
              <div class="row">
                <div class="col-sm-9">
                  <h6 title="Geometry to reuse">
                    <i><font-awesome-icon icon="map-marked-alt" />
                      <span v-if="geom.geometry.type.includes('Point')">&nbsp;Point </span>
                      <span v-if="geom.geometry.type.includes('String')">&nbsp;Line </span>
                      <span v-if="geom.geometry.type.includes('Polygon')">&nbsp;Polygon </span>
                    </i>
                    <span v-if="geom.id"> (from a layer)</span>
                    <span v-else> (from a story)</span>
                  </h6>
                  <h6 class="text-muted">
                    <div v-if="geom.id">
                      <span v-for="(value, propertykey) in geom.properties" :key="propertykey">
                        <small v-if="propertykey.toLowerCase() != 'id' && !Array.isArray(value) && value != null && value != '' && value != 'NULL'">{{ propertykey }}: {{ value }}; </small>
                      </span>
                    </div>
                    <div v-else>
                      <span v-for="(value, propertykey) in geom.properties" :key="propertykey">
                        <small v-if="propertykey.toLowerCase() == 'label'">{{ propertykey }}: {{ value }}; </small>
                      </span>
                    </div>
                  </h6>
                </div>
                <div class="col-sm-3 text-center">
                  <button type="button" class="btn btn-sm btn-primary" @click="reuseGeometryInStory(geom)">
                    Reuse geometry
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer mt-3">
            <div class="btn btn-secondary btn-ok" data-dismiss="modal" @click="$store.commit('SET_REUSE_MODE', false)">
              Close
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="addPointCoordModal" class="modal fade" data-keyboard="false" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content modal-margin-top">
          <div class="modal-header">
            <h5>Add point coordinates</h5>
          </div>
          <div class="modal-body">
            <p>Please insert coordinates in Decimal degrees</p>
            <div class="input-group mb-3">
              <div class="input-group-prepend">
                <span class="input-group-text"><small>Coordinates (WGS84)</small></span>
              </div>
              <input v-model.number="pointFromCoord.lat" type="number" step="any" class="form-control" placeholder="Latitude">
              <input v-model.number="pointFromCoord.long" type="number" step="any" class="form-control" placeholder="Longitude">
            </div>
            <button type="button" class="btn btn-sm btn-secondary" @click="getMyLocation()">
              Get my location
            </button>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-success btn-ok" :disabled="!pointFromCoord.lat || !pointFromCoord.long" @click="drawPointFromCoord()">
              Ok
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="magnifyGeomImageModal" class="modal fade">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-body text-center pt-5 magnify-modal">
            <img v-if="magnifyImageElem" :src="mediaRoot + magnifyImageElem.mediafile_name" class="story-elem-img mb-3" style="width:1000px;">
            <div v-if="magnifyImageElem">
              <div v-if="storyViewLang === 'eng'">
                <span v-if=" magnifyImageElem.media_description.eng">{{ magnifyImageElem.media_description.eng }}</span>
                <span v-else class="text-muted font-italic">No description defined in English</span>
              </div>
              <div v-if="storyViewLang === 'mao'">
                <span v-if=" magnifyImageElem.media_description.mao">{{ magnifyImageElem.media_description.mao }}</span>
                <span v-else class="text-muted font-italic">No description defined in Maori</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div class="btn btn-secondary btn-ok" data-dismiss="modal">
              Close
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { EventBus } from 'store/event-bus'
import { addGeoserverWMS, zoomToGeoserverVectorLayer, zoomToGeoserverLayerBbox, setSLDstyle } from 'utils/internalMapServices'
import { enableEventListeners, getCorrectExtent, createGeojsonLayer, createGeojsonVTlayer, disableEventListenerSingleClick, enableEventListenerSingleClick,
  drawingStyle, defaultStoryGeomStyle, defaultStoryGeomLayerStyle, addAllStoriesGeomsLayer, removeStoryGeomsFromStoriesGeomsLayer, olFeatureFromJsonGeom,
  addSelectedFeaturesLayer } from 'utils/mapUtils'
import { extLayersObj } from 'utils/objects'
import { hexToRgba, hexToRgb } from 'utils/objectUtils'
import { delay, each, isString, some, difference } from 'underscore'
// Import everything from ol
import Map from 'ol/Map'
import View from 'ol/View'
import { Tile as TileLayer } from 'ol/layer'
import Stamen from 'ol/source/Stamen'
// import XYZ from 'ol/source/XYZ'
import OSM from 'ol/source/OSM'
// import TileJSON from 'ol/source/TileJSON'
import VectorSource from 'ol/source/Vector'
import VectorLayer from 'ol/layer/Vector'
import { Draw, Snap, Modify } from 'ol/interaction'
import Feature from 'ol/Feature'
import { Point } from 'ol/geom' //, LineString, MultiLineString, Polygon, MultiPolygon
import GeoJSON from 'ol/format/GeoJSON'
// import { getWidth } from 'ol/extent' // getCenter,
import Overlay from 'ol/Overlay'
import { Fill, Stroke, Style, Circle as CircleStyle, Text } from 'ol/style'
import { Zoom, Attribution, ScaleLine } from 'ol/control'
// import { tile } from 'ol/loadingstrategy' // bbox as bboxStrategy,
// import { createXYZ } from *'ol/tilegrid'
import { defaults } from 'ol/interaction'
import { transform } from 'ol/proj'
import Geolocation from 'ol/Geolocation'
import Geocoder from 'ol-geocoder'
import { flyTo } from 'utils/olHelper'
import controlOverlay from 'ol-ext/control/Overlay'

var draw, snap, modify // global so we can remove them later
var mapDrawingNotify

// Esc key to remove last drawn point during drawing interaction
document.addEventListener('keydown', function(e) {
  if (e.which == 27)
      draw.removeLastPoint()
})

export default {
  name: 'MapView',
  data() {
    return {
      mapView_projection: 'EPSG:3857', // 'EPSG:4326',  // this distorts the view
      // mapView_center: [19410113.214624517, -5044843.866821633], // [172.79296875, -41.868896484375]
      // mapView_zoom: 6,
      mapView_center: [19626582.878728133, -4621535.604178325],
      mapView_zoom: 9,
      features_info: '',
      layersFeaturesPopupCount: 0,
      nExpectedCount: null,
      layerProperties: [],
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
         layername: null,
         classifyby: false,
         classifybyproperty: ""
       },
       drawingSource: null,
       drawnFeature: {
         geometry: null,
         name: {eng:'',mao:''},
         description: {eng:'',mao:''}
       },
       storyGeomStyle: {
         color: '#1f6de0',
         opacity: 0.5,
         linewidth: 2
       },
       mediaRoot: process.env.API_HOST + '/media/',
       geomMediaToDelete: null,
       selectedFeatures: [],
       pointFromCoord: {
         lat: null,
         long: null
       },
       magnifyImageElem: null,
    }
  },
  computed: {

    mapView () {
      var view = new View({
        projection: this.mapView_projection,
        center: this.mapView_center,
        zoom: this.mapView_zoom,
        minZoom: 2
      })
      return view
    },
    getOrientation(){
      return this.$store.state.orientation
    },
    mapPopup () {
      var popup = new Overlay({
        element: $("#feature_popup")[0], // the same as document.getElementById('feature_popup')
        stopEvent: false,
        dragging: false
      })
      return popup
    },
    storyGeomInfoOverlay () {
      var storygeom_overlay = new controlOverlay({
        // closeBox: true,
        className: "slide-up menu",
        content: $("#storygeom_overlay").get(0)
      })
      return storygeom_overlay
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
    },
    isDrawMode () {
      return this.$store.state.drawMode
    },
    isStoryViewMode () {
      return this.$store.state.storyViewMode
    },
    storyViewLang () {
      return this.$store.state.storyViewLang
    },
    isGeomMediaMode () {
      return this.$store.state.geomMediaMode
    },
    isReuseMode () {
      return this.$store.state.reuseMode
    },
    geomsForReuse () {
      var features = []
      each(this.$store.state.featuresForReuse, (feature) => {
        try {
          feature.getProperties() // it comes from the allStoriesGeomsLayer
          // Get GeoJSON
          var writer = new GeoJSON()
          var geojsonStr = JSON.parse(writer.writeFeatures([feature]))
          features.push(geojsonStr.features[0])
        } catch (e) {
          if (feature.geometry) { // it comes from layers (if it's a raster layer the geometry is null, so ignore it)
            features.push(feature)
          }
        }
      })
      return features
    },
    allStoriesGeomsLayer () {
      return this.$store.state.allStoriesGeomsLayer
    }
  },
  created: function () {
    // Set external layers
    this.$store.commit('SET_EXTERNAL_LAYERS', $.extend(true, {}, extLayersObj))
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
     this.$store.state.isMobile = true
     this.$store.state.hitTolerance = 10
   }
    // Set internal layers and other stuff before creating the map
    Promise.all([
      this.$store.dispatch('getDatasets'),
      this.$store.dispatch('getUsers'),
      this.$store.dispatch('getWebsiteTranslation'),
      this.$store.dispatch('getSectors'),
      this.$store.dispatch('getNests'),
      this.$store.dispatch('getAllPublications'),
      this.$store.dispatch('getKaitiakis'),
      this.$store.dispatch('getStories'),
      this.$store.dispatch('getAtuas'),
      this.$store.dispatch('getProfiles'),
      this.$store.dispatch('getStoryTypes'),
      this.$store.dispatch('getElementContentTypes')
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
    EventBus.$on('updateMapHeight', () => {
      this.fixContentHeight()
    })
    EventBus.$on('createLayer', (layer, servType) => {
      if (servType === 'external') {
        var layerconfigs = layer
        extLayersObj[layer.keyname].functionToCall.call(null, layerconfigs)
      } else if (servType === 'internal') {
        var layerid = layer
        addGeoserverWMS(layerid)
      } else if (servType === 'allstoriesgeoms') {
        var geoms = layer
        addAllStoriesGeomsLayer(geoms)
      } else if (servType === 'selectedfeatures') {
        var features = layer
        addSelectedFeaturesLayer(features)
      }
    })

    EventBus.$on('removeLayer', (layername) => {
      var lyr_list = []
      if (this.map) {
        this.map.getLayers().forEach(function (layer) {
          if (layer.get('name') === layername) {
            lyr_list.push(layer)
          }
        })
        each(lyr_list, (l) => {
          this.map.removeLayer(l)
        })
      }

    })

    EventBus.$on('refreshLayer', (layername) => {
      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === layername) {
          layer.getSource().updateParams({"time": Date.now()})
          this.refreshInternalLegend()
        }
      })
    })

    EventBus.$on('addUploadedLayer', (payload, geoserverLayer=true) => {
      var geojsonObj = payload.jsonlayer
      var layerid = payload.id

      if (geoserverLayer) {
        EventBus.$emit('createLayer', layerid, 'internal')
        // this.$store.commit('ADD_INTERNAL_LAYER', payload)
        if (payload.geomtype != 'raster') {
          zoomToGeoserverVectorLayer(layerid)
        } else {
          zoomToGeoserverLayerBbox(layerid)
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
      if (this.nExpectedCount !== 0) {
        this.$store.commit('SET_LOADING', true)
      }
    })

    EventBus.$on('showLayersFeaturesPopup', (obj) => {
      var element = this.mapPopup.getElement()
      // var coordinate = obj.coordinate // in case we want to show the popover in the clicked coordinate

      if (obj.hasOwnProperty('features')) {
        var features = obj.features
        var layername = obj.layername
        var assignedname = this.$store.state.internalLayers[layername] ? this.$store.state.internalLayers[layername].assigned_name : ''

        this.selectedFeatures = this.selectedFeatures.concat(features)

        if (this.features_info !== '') {
          this.features_info = this.features_info + '<hr />'
        }

        if (this.isReuseMode) {
          this.$store.commit('ADD_FEATURES_FOR_REUSE', features)
        }

        var feature_properties
        each(features, (f, index) => {
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

          if (index === 0) {
            this.features_info = this.features_info + '<p class="text-center mb-2">Layer: ' + layertitle + '</p>'
          } else {
            this.features_info = this.features_info + '<br />'
          }

          each(feature_properties, (value, key) => {
            if (key.toLowerCase() != "geometry" && key.toLowerCase() != "bbox" && key.toLowerCase() != "id" && value != null && value != "" && value != "NULL") {
              if (isString(value) && value.includes('http')) {
                this.features_info = this.features_info + '<p><strong>' + key.replace(/_/g, " ") + ':</strong> <a href="' + value + '" target="_blank">' + key.replace(/_/g, " ") + ' link' + '</a></p>'
              } else {
                this.features_info = this.features_info + '<p><strong>' + key.replace(/_/g, " ") + ':</strong> ' + value + '</p>'
              }
            }
          })

          // this.features_info = this.features_info + '<hr />'
        })
      }

      this.layersFeaturesPopupCount++

      if (this.layersFeaturesPopupCount === this.nExpectedCount) {
        if (this.isReuseMode && this.geomsForReuse.length != 0) {
          EventBus.$emit('showFeaturesReuse')
        } else {

          EventBus.$emit('createLayer', this.selectedFeatures, 'selectedfeatures')
          $(element).popover('dispose')

          if (this.features_info != "") {
            // // show the popover on the clicked coordinate
            // var coordinate = obj.coordinate
            // this.mapPopup.setPosition(coordinate)

            // show the popover in the left side of the map
            var mapextent = this.map.getView().calculateExtent(this.map.getSize())
            var meanlat = (mapextent[3]-mapextent[1])/2.0
            this.mapPopup.setPosition([mapextent[0], mapextent[3]-meanlat])
            $(element).popover({
              animation: false,
              html: true,
              title: 'Layers Feature Info <a href="#" class="close" data-dismiss="alert">&times;</a>',
              // placement: 'top',
              // template:	'<div class="popover feature-popup" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
              template:	'<div class="popover feature-popup" role="tooltip"><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
              content: this.features_info
            })
            $(element).popover('show')
          }
        }
        this.layersFeaturesPopupCount = 0
        this.features_info = ''
        this.$store.commit('SET_LOADING', false)
      }
    })

    EventBus.$on('closeMapPopup', () => {
      var element = this.mapPopup.getElement()
      $(element).popover('dispose')
    })

    EventBus.$on('showFeaturesReuse', () => {
      $('#geomsReuseModal').modal('show')
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
                                              }
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
      if (payload.hasOwnProperty('layerType')) {
        if (payload.layerType === "internal") {
          // if (this.internalLayers[payload.layerName].geomtype != 3) {
          //   // // for vector layers created with JDBCVirtualTable, the bbox is not generated,
          //   // //so it's necessary to getFeatures from WFS to get the extent (but it takes more time)
          //   zoomToGeoserverVectorLayer(payload.layerName)
          // } else {
          //   zoomToGeoserverLayerBbox(payload.layerName)
          // }
          each(this.internalLayers, (layer) => {
            if (layer.gs_layername === payload.layerName) {
              zoomToGeoserverLayerBbox(layer.id)
            }
          })

        }
      } else {
        this.map.getLayers().forEach( (layer) => {
          if (layer.get('name') === payload.layerName) {
            var extent = layer.getSource().getExtent()
            if (layer.getSource().getFeatures().length > 1) {
              this.map.getView().fit(extent, { duration: 2000 })
            } else {
              this.map.getView().fit(extent, { duration: 2000, maxZoom:18 })
            }
          }
        })
      }

    })

    EventBus.$on('restyleLayer', (layerid) => {

      var layerName = this.internalLayers[layerid].gs_layername

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
         layername: layerName,
         layerid: layerid,
         classifyby: false,
         classifybyproperty: ""
       }

      // Get current geoserver layer style (SLD) and fill the layerStyle object accordingly
      this.$store.dispatch('getInternalLayerStyle', layerName)
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

        if (this.internalLayers[layerid].geomtype != 3) {
          $.ajax( process.env.GEOSERVER_HOST + '/wms', {
            type: 'GET',
            data: {
                service: 'WFS',
                version: '1.1.0',
                request: 'DescribeFeatureType',
                typename: 'storyapp:' + layerName,
                outputFormat: 'text/javascript',
                format_options: 'callback:getJson',
                myData: Math.random()
            },
            dataType: 'jsonp',
            jsonpCallback:'getJson'
          }).done( (response) => {
            var geoserverLayerProperties = response.featureTypes[0].properties.map(a => a.name)
            var layerProperties = difference(geoserverLayerProperties, ["the_geom", "id"])
            this.layerProperties = $.extend(true, [], layerProperties)
            $('#restyleLayerModal').modal('show')
          })
        } else {
          $('#restyleLayerModal').modal('show')
        }

      })

    })

    EventBus.$on('addDrawingLayer', () => {

      EventBus.$emit('resetDrawnFeature')

      disableEventListenerSingleClick()
      this.showDrawingNotify()
      $('#drawInfoModal').modal('show')

      this.createDrawingLayer()
    })


    EventBus.$on('addStoryGeomsToMap', (storyBodyElements) => {
      EventBus.$emit('removeLayer', 'storyGeomsLayer')
      EventBus.$emit('resetDrawnFeature')
      this.hideStoryGeomInfo()

      // Create an empty storyGeomsLayer layer
      var storyGeomsSource = new VectorSource({
        format: new GeoJSON()
      })
      var storyGeomsVector = new VectorLayer({
        source: storyGeomsSource,
        name: 'storyGeomsLayer',
        style: defaultStoryGeomLayerStyle,
        zIndex: 40
      })
      this.map.addLayer(storyGeomsVector)

      // Get storybodyelements of type GEOM
      var geoms = []
      each(storyBodyElements, (elem) => {
        if (elem.element_type === 'GEOM') {
          geoms.push(elem)
        }
      })
      if (geoms.length === 0) {
        EventBus.$emit('zoomToMapView')

      } else {
        var featuresToAdd = []
        var geomAttrStyles = {}
        var ol_geom
        each(geoms, (geomElem) => {

          ol_geom = olFeatureFromJsonGeom(geomElem.geom_attr)
          featuresToAdd.push(new Feature({
              geometry: ol_geom,
              name: geomElem.geom_attr.id,
              label: geomElem.geom_attr.name[this.$store.state.storyViewLang]
          }))

          geomAttrStyles[geomElem.geom_attr.id] = geomElem.geom_attr.style
        })
        storyGeomsSource.addFeatures(featuresToAdd)

        // Set specific styles when geom_attr.style is not null
        var features = storyGeomsSource.getFeatures()
        features.forEach((feature) => {
          if (geomAttrStyles[feature.getProperties().name]) {
            var geomAttrStyle = this.createOLStyle({ 'label': feature.getProperties().label, 'styleObj': geomAttrStyles[feature.getProperties().name] })

            feature.setStyle(geomAttrStyle)
          }
        })

        EventBus.$emit('zoomToStoryGeoms')
      }

      removeStoryGeomsFromStoriesGeomsLayer()

    })


    EventBus.$on('zoomToStoryGeoms', () => {
      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === 'storyGeomsLayer') {
          var extent = layer.getSource().getExtent()
          if (layer.getSource().getFeatures().length > 1) {
            this.map.getView().fit(extent, { duration: 2000 })
          } else {
            this.map.getView().fit(extent, { duration: 2000, maxZoom:18 })
          }
        }
      })
    })


    EventBus.$on('addNewStoryGeomToMap', (geomAttr) => {
      var ol_geom = olFeatureFromJsonGeom(geomAttr)

      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === 'storyGeomsLayer') {
          var feature = new Feature({
              geometry: ol_geom,
              name: geomAttr.id,
              label: geomAttr.name[this.$store.state.storyViewLang]
          })
          layer.getSource().addFeatures([feature])
        }
      })
    })


    EventBus.$on('removeStoryGeomFromMap', (geomAttr) => {
      EventBus.$emit('resetDrawnFeature')
      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === 'storyGeomsLayer') {
          var features = layer.getSource().getFeatures()
          features.forEach((feature) => {
            if (feature.getProperties().name === geomAttr.id) {
              layer.getSource().removeFeature(feature)
            }
          })
        }
      })
    })


    EventBus.$on('showStoryGeomInfo', (geomAttr) => {
      if (!$("#storygeom_overlay").parent().hasClass('ol-visible')) {
        this.storyGeomInfoOverlay.toggle()
      }
      if (geomAttr) {
        this.drawnFeature = $.extend(true, {}, geomAttr) // clone object to avoid binding
      }
    })


    EventBus.$on('zoomToGeometry', (geomAttr) => {

      var features
      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === 'storyGeomsLayer') {
          features = layer.getSource().getFeatures()
        }
      })
      if (features) {
        features.forEach( (feature) => {
          if (feature.getProperties().name === geomAttr.id) {
            var extent = feature.getGeometry().getExtent()
            var extent_translated = [extent[0], extent[1]-100, extent[2], extent[3]-100]
            this.map.getView().fit(extent_translated, { duration: 2000, maxZoom:18 })
          }
        })
      }
    })


    EventBus.$on('editGeomAttr', (geomAttr) => {
      EventBus.$emit('zoomToGeometry', geomAttr)
      EventBus.$emit('showStoryGeomInfo', geomAttr)

      this.$store.commit('SET_DRAW_MODE', true)
      this.$store.commit('SET_GEOM_MEDIA_MODE', false)
      this.drawnFeature = $.extend(true, {}, geomAttr)

      disableEventListenerSingleClick()
      this.showDrawingNotify()

      this.createDrawingLayer()

      // Add editing geometry to drawing layer
      var ol_geom = olFeatureFromJsonGeom(geomAttr)

      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === 'drawingLayer') {
          var feature = new Feature({
              geometry: ol_geom,
              name: geomAttr.id
          })
          layer.getSource().addFeatures([feature])
        }
      })

      // Add only interactions snap and modify
      snap = new Snap({source: this.drawingSource})
      this.map.addInteraction(snap)
      modify = new Modify({source: this.drawingSource})
      this.map.addInteraction(modify)

      modify.on('modifyend', (e) => {
        // Get GeoJSON
        var writer = new GeoJSON()
        var geojsonStr = JSON.parse(writer.writeFeatures([e.features.getArray()[0]]))
        this.drawnFeature.geometry = geojsonStr.features[0]
      }) //modifyend event
    })


    EventBus.$on('replaceStoryGeomToMap', (geomAttr) => {
      EventBus.$emit('resetDrawnFeature')

      var ol_geom = olFeatureFromJsonGeom(geomAttr)

      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === 'storyGeomsLayer') {
          var features = layer.getSource().getFeatures()
          features.forEach((feature) => {
            if (feature.getProperties().name === geomAttr.id) {
              feature.setGeometry(ol_geom)
              var geomAttrStyle = this.createOLStyle({ 'label': geomAttr.name[this.$store.state.storyViewLang], 'styleObj': geomAttr.style })
              feature.setStyle(geomAttrStyle)
            }
          })
        }
      })
    })


    EventBus.$on('editGeomStyle', (geomAttr) => {
      EventBus.$emit('zoomToGeometry', geomAttr)
      this.$store.commit('SET_GEOM_MEDIA_MODE', false)
      this.$store.commit('SET_DRAW_MODE', false)

      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === 'storyGeomsLayer') {
          var features = layer.getSource().getFeatures()
          features.forEach((feature) => {
            if (feature.getProperties().name === geomAttr.id) {
              if (geomAttr.style !== null) {
                this.storyGeomStyle = geomAttr.style
              } else {
                this.storyGeomStyle = {
                  'color': '#1f6de0', // it needs to be hex code instead of rgb(31, 109, 224)
                  'opacity': 0.5,
                  'linewidth': 4
                }
              }
              this.storyGeomStyle.feature = feature
              this.storyGeomStyle.geomAttr = geomAttr
              $('#restyleStoryGeomModal').modal('show')
            }
          })
        }
      })
    })


    EventBus.$on('resetDrawnFeature', () => {
      if ($("#storygeom_overlay").parent().hasClass('ol-visible')) {
        EventBus.$emit('toggleStoryGeomInfoOverlay')
      }
      this.drawnFeature = {
        geometry: null,
        name: {eng:'',mao:''},
        description: {eng:'',mao:''}
      }
    })


    EventBus.$on('zoomToMapView', () => {
      this.map.getView().setZoom(this.mapView_zoom)
      this.map.getView().setCenter(this.mapView_center)
    })


    EventBus.$on('setallStoriesGeomsLayerLegend', (style) => {
      this.allStoriesGeomsLayer.style = style
    })

    EventBus.$on('resetSelectedFeatures', () => {
      EventBus.$emit('removeLayer', 'selectedFeaturesLayer')
      this.selectedFeatures = []
    })

    EventBus.$on('toggleStoryGeomInfoOverlay', () => {
      this.storyGeomInfoOverlay.toggle()
    })

  },
  methods: {

    initMap () {
      // Detect and set orientation of the screen
      // if(window.outerWidth > window.outerHeight || window.outerWidth > 1023 || window.outerHeight > 1023)
      if(window.outerWidth > window.outerHeight) {
        this.$store.commit('SET_ORIENTATION', 'landscape')
      } else {
        this.$store.commit('SET_ORIENTATION', 'portrait')
      }

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
        ],
        interactions: defaults({ doubleClickZoom: false, handfree: false })
      })

      // Add geocoder to the map
      var geocoder = new Geocoder('nominatim', {
                                      provider: 'osm',
                                      lang: 'en-US',
                                      placeholder: 'Search for ...',
                                      targetType: 'glass-button',
                                      limit: 30,
                                      keepOpen: true,
                                      preventDefault: true,
                                      autoComplete: true,
                                      autoCompleteMinLength: 2
                                    })
      themap.addControl(geocoder)

      geocoder.on('addresschosen', (evt) => {
        // this.map.getView().fit([evt.coordinate[0], evt.coordinate[1], evt.coordinate[0], evt.coordinate[1]], { duration: 2000, maxZoom:16 })
        flyTo(evt.coordinate, this.map.getView(), function() {})
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
      each(this.internalLayers, (layer) => {
        if (layer.visible) {
          EventBus.$emit('createLayer', layer.id, 'internal')
        }
      })


      // Declaration of map events
      enableEventListeners()

      // Popup where the user clicked
      themap.addOverlay(this.mapPopup)

      // Overlay for Feature Info toggle
      themap.addControl(this.storyGeomInfoOverlay)

      // Fix map height and width
      this.fixContentHeight()

      this.fixContentWidth()

    },
    updateSizeMap () {
      if(this.$store.state.map){
        this.$store.state.map.updateSize()
      }
    },
    fixContentHeight () {
      var navBarHeight = $("#navbar").outerHeight()
      $("#map").height($(window)[0].innerHeight - navBarHeight)
      if(this.$store.state.map){
        this.$store.state.map.updateSize()
      }
    },
    fixContentWidth () {
      // if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
      //   // if (screen.width >= 768) {
      //   //   $("#map").width(100)
      //   //   delay(this.updateSizeMap, 100)
      //   // }
      // } else {
      //   $("#map").width(100)
      //   delay(this.updateSizeMap, 100)
      // }
      $("#map").css({'width': '100%'})
      delay(this.updateSizeMap, 200)
    },
    createSLD () {
      setSLDstyle(this.layerStyle)
      $('#restyleLayerModal').modal('hide')
    },
    getInternalLayerLegend (layer) {
      return process.env.GEOSERVER_HOST + "/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=storyapp:" + layer.gs_layername + "&myData:" + Math.random()
    },
    refreshInternalLegend () {
      each(this.internalLayers, (layer) => {
        layer.legendURL = this.getInternalLayerLegend(layer)
      })
    },
    isStyleInputVisible (geomTypeArray) {
      if (this.internalLayers[this.layerStyle.layerid]) {
        return geomTypeArray.includes(this.internalLayers[this.layerStyle.layerid].geomtype)
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
    },
    addPointCoord () {
      this.pointFromCoord = {
        lat: null,
        long: null
      }
      $("#addPointCoordModal").modal('show')
    },
    drawPointFromCoord () {
      $("#addPointCoordModal").modal('hide')

      this.map.removeInteraction(draw)
      this.map.removeInteraction(snap)
      this.map.removeInteraction(modify)

      var lonLat = transform([this.pointFromCoord.long, this.pointFromCoord.lat], 'EPSG:4326', 'EPSG:3857')
      var olFeature = new Feature({
                        geometry: new Point(lonLat)
                      })

      this.drawingSource.addFeatures([olFeature])

      // Get GeoJSON
      var writer = new GeoJSON()
      var geojsonStr = JSON.parse(writer.writeFeatures([olFeature]))
      this.drawnFeature.geometry = geojsonStr.features[0]
      EventBus.$emit('zoomToLayer', {layerName:'drawingLayer'})
      EventBus.$emit('showStoryGeomInfo')

      snap = new Snap({source: this.drawingSource})
      this.map.addInteraction(snap)
      modify = new Modify({source: this.drawingSource})
      this.map.addInteraction(modify)

      modify.on('modifyend', (e) => {
        // Get GeoJSON
        var writer = new GeoJSON()
        var geojsonStr = JSON.parse(writer.writeFeatures([e.features.getArray()[0]]))

        this.drawnFeature.geometry = geojsonStr.features[0]
      }) //modifyend event

    },
    drawGeom (geomtype) {

      this.map.removeInteraction(draw)
      this.map.removeInteraction(snap)
      this.map.removeInteraction(modify)

      draw = new Draw({
        source: this.drawingSource,
        type: geomtype,
        freehand: false
      })
      this.map.addInteraction(draw)
      snap = new Snap({source: this.drawingSource})
      this.map.addInteraction(snap)
      modify = new Modify({source: this.drawingSource})
      this.map.addInteraction(modify)

      draw.on('drawend', (e) => {
        // Get GeoJSON
        var writer = new GeoJSON()
        var geojsonStr = JSON.parse(writer.writeFeatures([e.feature]))

        this.drawnFeature.geometry = geojsonStr.features[0]
        this.map.removeInteraction(draw)
        EventBus.$emit('showStoryGeomInfo')
      }) //drawend event

      modify.on('modifyend', (e) => {
        // Get GeoJSON
        var writer = new GeoJSON()
        var geojsonStr = JSON.parse(writer.writeFeatures([e.features.getArray()[0]]))

        this.drawnFeature.geometry = geojsonStr.features[0]
      }) //modifyend event
    },
    deleteGeom () {
      EventBus.$emit('resetDrawnFeature')
      var features = this.drawingSource.getFeatures()
      var lastFeature = features[features.length - 1]
      this.drawingSource.removeFeature(lastFeature)
    },
    saveGeomAttrb () {
      var geomform = document.getElementById("geomAttrForm")

      if (geomform.checkValidity()) {

        // Create or update
        if (this.drawnFeature.id) {
          this.$store.dispatch('updateGeometryAttrb', this.drawnFeature)
          .then((response) => {
            EventBus.$emit('updateGeometryElement', response.body)
            this.stopDrawing()
          })
        } else {
          this.$store.dispatch('addGeometryAttrb', this.drawnFeature)
          .then((response) => {
            if (response.ok) {
              if (response.body) {
                EventBus.$emit('addGeometryElement', response.body)
                this.stopDrawing()
              }
            } else {
              if (response.body[0].indexOf('Request') == -1) {
                // this.uploadError = response.body[0]
              } else {
                // this.uploadError = response.body.split('Request')[0]
              }
            }
          })
          .catch((err) => {
            console.log(err)
          })
        }

        // Remove validated class
        geomform.classList.remove("was-validated")
      } else {
        geomform.classList.add("was-validated")
      }

    },
    showDrawingNotify () {
      mapDrawingNotify = $.notify({
                            message: "<div class='text-center'><i class='fa fa-pen' /><strong>&nbsp;&nbsp;Map drawing interaction is active</strong></div>"
                          }, {
                            type: 'info',
                            newest_on_top: true,
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
                            }
                          })
    },
    stopDrawing () {
      this.$store.commit('SET_DRAW_MODE', false)
      mapDrawingNotify.close()
      this.drawingSource = null
      enableEventListenerSingleClick()
      EventBus.$emit('removeLayer', 'drawingLayer')
      this.map.removeInteraction(draw)
      this.map.removeInteraction(modify)
      this.map.removeInteraction(snap)
      this.hideStoryGeomInfo()
    },
    stopReuse () {
      this.$store.commit('SET_REUSE_MODE', false)
    },
    hideStoryGeomInfo () {
      EventBus.$emit('resetDrawnFeature')
    },
    cancelsetOLStyle(){
      delete this.storyGeomStyle['feature']
      delete this.storyGeomStyle['geomAttr']
    },
    setOLStyle () {
      var style = this.createOLStyle({'label': this.storyGeomStyle['geomAttr'].name[this.$store.state.storyViewLang], 'styleObj': this.storyGeomStyle})

      this.storyGeomStyle.feature.setStyle(style)
      $('#restyleStoryGeomModal').modal('hide')

      // Save geomAttr style
      var geomAttr = this.storyGeomStyle['geomAttr']
      delete this.storyGeomStyle['feature']
      delete this.storyGeomStyle['geomAttr']
      geomAttr.style = this.storyGeomStyle
      this.$store.dispatch('updateGeometryAttrb', geomAttr)
      .then((response) => {
        EventBus.$emit('updateGeometryElement', response.body)
      })
    },
    createOLStyle (obj) {
      if (!obj.styleObj) {
        return defaultStoryGeomStyle(obj.label)
      } else {
        var color = obj.styleObj.color
        var style = new Style({
                        fill: new Fill({
                          color: hexToRgba(color, obj.styleObj.opacity)
                        }),
                        stroke: new Stroke({
                          color: 'rgba(' + hexToRgb(color).r + ', ' + hexToRgb(color).g + ', ' + hexToRgb(color).b  + ', 1)',
                          width: obj.styleObj.linewidth
                        }),
                        image: new CircleStyle({
                          radius: 5,
                          fill: new Fill({
                            color: hexToRgba(color, obj.styleObj.opacity)
                          }),
                          stroke: new Stroke({
                            color: 'rgba(' + hexToRgb(color).r + ', ' + hexToRgb(color).g + ', ' + hexToRgb(color).b  + ', 1)',
                            width: obj.styleObj.linewidth
                          })
                        }),
                        text: new Text({
                          font: 'bold 15px Calibri,sans-serif',
                          fill: new Fill({ color: '#2b2828' }),
                          stroke: new Stroke({
                            color: '#ffffff', width: 4
                          }),
                          text: obj.label,
                          offsetY: 15,
                          overflow: true
                        })
                      })
        return style
      }
    },
    createDrawingLayer () {
      this.drawingSource = new VectorSource()
      var drawingVector = new VectorLayer({
        source: this.drawingSource,
        name: 'drawingLayer',
        style: drawingStyle,
        zIndex: 50
      })
      this.map.addLayer(drawingVector)
    },
    addMediaFileToGeom () {
      $('.carousel').carousel(0) // reinitialise the carousel before adding new media
      EventBus.$emit('addMediaToGeomAttr', this.drawnFeature)
    },
    hideAddNewMedia() {
      this.$store.commit('SET_GEOM_MEDIA_MODE', false)
    },
    saveCaptions () {
      this.$store.commit('SET_GEOM_MEDIA_MODE', false)
      this.$store.dispatch('updateGeometryAttrbMediaCaptions', this.drawnFeature.geomAttribMedia)

      // Despite the geomAttribMedia are saved in the db, we need to update the geomAttribMedia of storyBodyElement geometry without
      // requesting the updated story, otherwise the not saved changes of the elements order will be lost if we refresh the story before saving it.
      each(this.$store.state.storyContent.storyBodyElements, (el) => {
        if (el.geom_attr) {
          if (el.geom_attr.id === this.drawnFeature.id) {
            el.geom_attr.geomAttribMedia = this.drawnFeature.geomAttribMedia
          }
        }
      })
    },
    deleteMediaFromGeom (media) {
      $("#deleteGeomMediaModal").modal('show')
      this.geomMediaToDelete = media
    },
    deleteGeomMedia () {
      $("#deleteGeomMediaModal").modal('hide')
      this.$store.dispatch('deleteGeometryAttrbMedia', this.geomMediaToDelete)

      // Despite the geomAttribMedia are delete from the db, we need to update the geomAttribMedia of storyBodyElement geometry without
      // requesting the updated story, otherwise the not saved changes of the elements order will be lost if we refresh the story before saving it.
      each(this.$store.state.storyContent.storyBodyElements, (el) => {
        if (el.geom_attr) {
          if (el.geom_attr.id === this.drawnFeature.id) {
            some(el.geom_attr.geomAttribMedia, (gAttMedia, i) => {
              if (gAttMedia.id === this.geomMediaToDelete.id) {
                el.geom_attr.geomAttribMedia.splice(i, 1)
                // Update drawngeom info
                $('.carousel').carousel(0) // reinitialise the carousel before update drawngeom info
                EventBus.$emit('showStoryGeomInfo', el.geom_attr)
                return true
              }
            })
          }
        }
      })
      this.$store.dispatch('deleteUnusedMediaFiles')

    },
    reuseGeometryInStory (geom) {
      $('#geomsReuseModal').modal('hide')
      this.$store.commit('SET_REUSE_MODE', false)
      this.$store.commit('SET_DRAW_MODE', true)
      this.$store.commit('SET_GEOM_MEDIA_MODE', false)

      EventBus.$emit('resetDrawnFeature')
      delete geom['properties'] // remove the properties of the copied geometry
      this.drawnFeature.geometry = geom

      disableEventListenerSingleClick()
      this.showDrawingNotify()

      this.createDrawingLayer()

      // Add editing geometry to drawing layer
      var ol_geom = olFeatureFromJsonGeom(geom)

      this.map.getLayers().forEach( (layer) => {
        if (layer.get('name') === 'drawingLayer') {
          var feature = new Feature({
              geometry: ol_geom
          })
          layer.getSource().addFeatures([feature])
        }
      })

      EventBus.$emit('zoomToLayer', {layerName:'drawingLayer'})
      EventBus.$emit('showStoryGeomInfo')

      // Add only interactions snap and modify
      this.map.removeInteraction(draw)
      snap = new Snap({source: this.drawingSource})
      this.map.addInteraction(snap)
      modify = new Modify({source: this.drawingSource})
      this.map.addInteraction(modify)

      modify.on('modifyend', (e) => {
        // Get GeoJSON
        var writer = new GeoJSON()
        var geojsonStr = JSON.parse(writer.writeFeatures([e.features.getArray()[0]]))

        this.drawnFeature.geometry = geojsonStr.features[0]
      }) //modifyend event
    },
 magnifyImage (element) {
   this.magnifyImageElem = element
   $('#magnifyGeomImageModal').modal('show')
 },
 getMyLocation () {
   var geolocation = new Geolocation({
     // take the projection to use from the map's view
     projection: this.map.getView().getProjection(),
     tracking: true,
     trackingOptions: {
         enableHighAccuracy: true
     }
   })

   // listen to changes in position
   geolocation.on('change', () => {
     var position = geolocation.getPosition()
     var lonLat = transform([position[0], position[1]], 'EPSG:3857', 'EPSG:4326')
     this.pointFromCoord = {
       lat: lonLat[1],
       long: lonLat[0]
     }
     geolocation.setTracking(false)
   })

   // handle geolocation error.
   geolocation.on('error', function(error) {
     console.log(error.message)
   })
 },
 slidePrev() {
   $('.carousel').carousel('prev')
 },
 slideNext() {
   $('.carousel').carousel('next')
    }
  }
}
</script>
