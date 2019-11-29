<template>
  <div id="sidePanel" :class="{'col-md-5':togglePanel, 'col-md-0':!togglePanel}">
    <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closeStory()" />

    <div v-if="isStoryViewMode" class="mt-5 mb-5">
      <span class="badge badge-warning mb-2 p-2" style="vertical-align: middle;">{{ story.status }}</span>
      <h4 v-html="story.length == 0 ? '' : story.title" />
      <p class="story-summary" v-html="story.length == 0 ? '' : story.summary" />
      <hr />
      <div v-for="element in story.storyBodyElements" :key="element.id" class="col-md-12">
        <div v-if="element.element_type == 'TEXT'">
          <div class="ql-text" v-html="element.text" />
        </div>
        <div v-if="element.element_type == 'GEOM'">
          <div :id="element.geom_attr.id" class="text-center m-4 geometry-name">
            <i><font-awesome-icon icon="map-marked-alt" size="lg" class="pointer" title="Zoom to geometry" @click="zoomToGeometry(element)" /></i>&nbsp;
            <strong><span class="ql-text" v-html="element.geom_attr.name" /></strong>
          </div>
        </div>
        <div class="align-center">
          <div v-if="element.element_type == 'IMG'">
            <img :src="mediaRoot + element.mediafile_name" class="story-elem-img img-fluid">
            <i><font-awesome-icon icon="search-plus" size="lg" class="positioner-magnify" @click="magnifyImage(element)" /></i>
          </div>

          <video v-if="element.element_type == 'VIDEO'" controls controlsList="nodownload" class="story-elem-video">
            <source :src="mediaRoot + element.mediafile_name" type="video/mp4">
            Your browser does not support the video tag.
          </video>
          <audio v-if="element.element_type == 'AUDIO'" controls controlsList="nodownload">
            <source :src="mediaRoot + element.mediafile_name" type="audio/mpeg">
            Your browser does not support the audio element.
          </audio>
          <p v-if="element.element_type != 'TEXT'" class="media-caption">
            {{ element.media_description }}
          </p>
        </div>
      </div>
    </div>
    <div v-else>
      <form :id="story.id + '_storyform'">
        <div class="row col-md-12">
          <h5 class="mb-0">
            Title
          </h5>
          <input v-model="story.title" required type="text" class="form-control form-control-sm mb-3" title="Title of the story">
          <h5 class="mb-0">
            Summary
          </h5>
          <textarea v-model="story.summary" required class="form-control form-control-sm" title="Story summary" />
        </div>
      </form>

      <hr />
      <p class="text-muted">
        <font-awesome-icon icon="info-circle" />
        Use the button below to add new elements to the story and reorder the elements dragging and dropping them.
      </p>
      <div class="btn-group dropright mb-4">
        <button type="button" :disabled="isDrawMode || isGeomMediaMode || isReuseMode" class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Add element to the story
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#" @click="addEmptyVueEditor()">New Text field</a>
          <a class="dropdown-item" href="#" @click="uploadFileClicked(isGeomMedia=false)">Upload Media file</a>
          <a class="dropdown-item" href="#" @click="drawGeometry()">Draw map geometry</a>
          <a class="dropdown-item" href="#" @click="reuseGeometry()">Reuse map geometry</a>
        </div>
      </div>

      <div class="row col-md-12 pl-5">
        <draggable v-model="story.storyBodyElements" class="width-inherit" ghost-class="ghost" handle=".handle" @start="dragging = true" @end="dragging = false">
          <div v-for="element in story.storyBodyElements" :key="element.id" class="row mb-2">
            <div class="col-md-11 mt-3">
              <div class="text-center handle">
                <button class="btn btn-sm btn-secondary drag-element handle">
                  Drag me&nbsp;
                  <i><font-awesome-icon icon="arrows-alt" /></i>
                </button>
              </div>
              <div v-if="element.element_type == 'GEOM'">
                <div class="story-elem-geom text-center">
                  <button type="button" class="btn pr-0" title="Zoom to geometry" @click="zoomToGeometry(element)">
                    <i><font-awesome-icon icon="map-marked-alt" class="pointer" />&nbsp;</i>
                  </button>
                  <span>
                    <i><strong>{{ element.geom_attr.name }}</strong></i>
                  </span>
                  <button type="button" class="btn pr-0" title="Edit geometry" @click="editGeometry(element.geom_attr)">
                    <i><font-awesome-icon icon="edit" /></i>
                  </button>
                  <button type="button" class="btn p-0" title="Edit geometry style" @click="editGeometryStyle(element.geom_attr)">
                    <i><font-awesome-icon icon="paint-brush" /></i>
                  </button>
                  <button type="button" class="btn pl-0" title="Manage media about the geometry" @click="manageGeomAttrMedia(element.geom_attr)">
                    <i><font-awesome-icon icon="images" /></i>
                  </button>
                </div>
              </div>
              <div v-if="element.element_type == 'TEXT'">
                <vue-editor v-model="element.text" :editor-toolbar="customToolbar" class="custom-ql-editor" />
              </div>
              <div class="align-center">
                <img v-if="element.element_type == 'IMG'" :src="mediaRoot + element.mediafile_name" class="story-elem-img img-fluid">
                <video v-if="element.element_type == 'VIDEO'" controls controlsList="nodownload" class="story-elem-video">
                  <source :src="mediaRoot + element.mediafile_name" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
                <audio v-if="element.element_type == 'AUDIO'" controls controlsList="nodownload" class="story-elem-video">
                  <source :src="mediaRoot + element.mediafile_name" type="audio/mpeg">
                  Your browser does not support the audio element.
                </audio>
              </div>
              <textarea v-if="!['TEXT','GEOM'].includes(element.element_type)" v-model="element.media_description" rows="1" class="form-control form-control-sm mt-1" title="Media description" placeholder="Media description (optional)" />
            </div>
            <div class="col-md-1 delete-element">
              <font-awesome-icon disabled icon="times-circle" size="lg" color="grey" class="pointer" title="Delete element" @click="deleteElementModal(element)" />
            </div>
          </div>
        </draggable>
      </div>
    </div>
    <div class="clear" />
    <div :class="[togglePanel ? 'col-md-6 visible': 'invisible', 'row sidepanel-footer']">
      <div class="col-md-10">
        <button v-if="story.hasOwnProperty('id') && !isStoryViewMode" type="button" class="btn btn-success" @click="saveStory()">
          Update story
        </button>
        <button v-if="!story.hasOwnProperty('id') && !isStoryViewMode" type="button" class="btn btn-success" @click="saveStory()">
          Save story
        </button>
        <button v-if="!isStoryViewMode" type="button" class="btn btn-danger ml-2" @click="showCancelStorySavingModal()">
          Cancel
        </button>
        <button v-if="story.hasOwnProperty('id') && isStoryViewMode" type="button" class="btn btn-primary" @click="editStory()">
          Edit story
        </button>
        <div v-if="isStoryViewMode" class="btn-group dropup ml-3">
          <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <font-awesome-icon icon="share-alt" class="mr-2" />
          </button>
          <div class="dropdown-menu">
            <a class="dropdown-item" href="#">Co-create story</a>
            <a class="dropdown-item" href="#">Share story</a>
            <a class="dropdown-item" href="#">Submit story</a>
            <a class="dropdown-item" href="#">Publish story</a>
          </div>
        </div>
        <button v-if="isStoryViewMode" type="button" class="btn btn-secondary float-right" @click="closeStory()">
          Close story
        </button>
      </div>
    </div>

    <div id="uploadFileModal" class="modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Upload file (video/audio/image)
            </h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form v-if="!uploadError" enctype="multipart/form-data" novalidate>
              <div class="dropbox">
                <input type="file" :name="uploadFieldName" class="input-file" @change="fileChange($event.target.files)">
                <p v-if="!uploadedFile">
                  Click to browse or drop a media file here
                </p>
                <p v-else>
                  {{ uploadedFile.name }}
                </p>
              </div>
              <h6 class="mb-1 mt-3">
                Media description (optional)
              </h6>
              <textarea v-model="tempMediaDescription" class="form-control form-control-sm" title="Media description" />
            </form>
            <div v-if="uploadError" class="alert alert-danger text-center">
              <h5>Upload failed with error:</h5>
              <code>{{ uploadError }}</code>
              <hr>
              <p>Please check that your data is valid and try again.</p>
            </div>
          </div>
          <div class="modal-footer">
            <!-- <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelAddMediaElement()">
              <span v-if="!uploadError">Cancel</span>
              <span v-else>Close</span>
            </button> -->
            <button v-if="!uploadError && !isGeomMedia" :disabled="!uploadedFile" type="button" class="btn btn-primary" data-dismiss="modal" @click="addMediaElement()">
              Add media to story
            </button>
            <button v-if="!uploadError && isGeomMedia" :disabled="!uploadedFile" type="button" class="btn btn-primary" data-dismiss="modal" @click="addGeomAttrMedia()">
              Add media to geometry
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="deleteElementModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Delete element</h5>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this element?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="deleteElement()">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="editingWarningModal" class="modal fade">
      <div class="modal-dialog">
        <div :class="[isDrawMode ? 'draw-info': '', 'modal-content']">
          <div class="modal-header">
            <h5>Attention</h5>
          </div>
          <div class="modal-body text-center">
            <div v-if="isDrawMode">
              <h6>The map drawing interaction is active, please stop drawing before close the story.</h6>
            </div>
            <div v-else>
              <h6>Don't forget to save changes before closing the story panel.</h6>
              <h6>Are you sure you want to cancel editing?</h6>
            </div>
          </div>
          <div class="modal-footer">
            <div v-if="isDrawMode" class="btn btn-secondary btn-ok" data-dismiss="modal">
              Got it!
            </div>
            <div v-else>
              <button type="button" class="btn btn-danger" data-dismiss="modal">
                No
              </button>
              <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="cancelStorySaving()">
                Yes
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="magnifyImageModal" class="modal fade">
      <div class="modal-dialog modal-xl">
        <div class="modal-content" style="background-color: #FFE;">
          <div class="modal-body text-center mt-5">
            <img v-if="magnifyImageElem" :src="mediaRoot + magnifyImageElem.mediafile_name" class="story-elem-img mb-3" style="width:1000px;">
            <p v-if="magnifyImageElem">
              {{ magnifyImageElem.media_description }}
            </p>
          </div>
          <div class="modal-footer">
            <div class="btn btn-secondary btn-ok" data-dismiss="modal">
              Close
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="geomsUsageModal" class="modal fade">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="mb-0">
              Features in Cultural Narratives
              <p class="mb-0 mt-2" style="font-size:18px;">
                Check out the features you clicked on and the related cultural narratives
              </p>
            </h3>
          </div>
          <div class="modal-body pt-0 pb-0 ml-2">
            <div v-for="usage in geomsUsage" :key="usage.geomAttr.id" class="mt-4">
              <h6 title="Feature name">
                <strong><i><font-awesome-icon icon="map-marked-alt" /></i>&nbsp;&nbsp;{{ usage.geomAttr.name }}</strong>
              </h6>
              <div class="row">
                <div class="col-sm-9 geom-usage">
                  <h6 title="Narrative title" class="text-muted">
                    <i><font-awesome-icon icon="book-open" /></i>&nbsp;&nbsp;{{ usage.story.title }}
                  </h6>
                  <h6 title="Narrative summary" class="ml-4">
                    <i>{{ usage.story.summary }}</i>
                  </h6>
                </div>
                <div class="col-sm-3 text-center">
                  <button type="button" class="btn btn-sm btn-primary" title="Open narrative" @click="openNarrative(usage.story.id, usage.geomAttr)">
                    Open narrative
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer mt-3">
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
import draggable from "vuedraggable"
import { VueEditor } from "vue2-editor"
import { imgFormats, videoFormats, audioFormats } from 'utils/objectUtils'
import { some, each, delay } from 'underscore'
import { EventBus } from 'store/event-bus'
import { disableEventListenerSingleClick, enableEventListenerSingleClick } from 'utils/mapUtils'

export default {
  components: {
    draggable,
    VueEditor
  },
  data() {
    return {
      mediaRoot: process.env.API_HOST + '/media/',
      uploadFieldName: 'file',
      uploadError: null,
      dragging: false,
      customToolbar: [
        // [{ 'font': [] }],
        // [{ 'header': [false, 1, 2, 3, 4, 5, 6, ] }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        ['bold', 'italic', 'underline'],
        [{'align': ''}, {'align': 'center'}, {'align': 'right'}, {'align': 'justify'}],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'color': [] }, { 'background': [] }],
        ['link']
      ],
      tempMediaDescription: null,
      uploadedFile: null,
      elementToDelete: null,
      magnifyImageElem: null,
      isGeomMedia: false,
      mediaForGeomAttr: null,
      geomsUsage: null
    }
  },
  computed: {
    draggingInfo() {
      return this.dragging ? "under drag" : ""
    },
    togglePanel (){
      return this.$store.state.isPanelOpen
    },
    story() {
      return this.$store.state.storyContent
    },
    isStoryViewMode () {
      return this.$store.state.storyViewMode
    },
    isDrawMode () {
      if (this.$store.state.drawMode) {
        disableEventListenerSingleClick()
        $('#sidePanel :button').prop('disabled', true)
      }else {
        enableEventListenerSingleClick()
        $('#sidePanel :button').prop('disabled', false)
      }
      return this.$store.state.drawMode
    },
    isGeomMediaMode () {
      if (this.$store.state.geomMediaMode) {
        disableEventListenerSingleClick()
        $('#sidePanel button:not("#uploadFileModalCancel")').prop('disabled', true)
      }else {
        enableEventListenerSingleClick()
        $('#sidePanel :button').prop('disabled', false)
      }
      return this.$store.state.geomMediaMode
    },
    isReuseMode () {
      if (this.$store.state.reuseMode) {
        $('#sidePanel :button').prop('disabled', true)
      }else {
        $('#sidePanel :button').prop('disabled', false)
      }
      return this.$store.state.reuseMode
    },
  },
  mounted: function () {
    EventBus.$on('addGeometryElement', (geomAttr) => {
      this.story.storyBodyElements.unshift({
        element_type: 'GEOM',
        geom_attr: geomAttr
      })
      EventBus.$emit('addNewStoryGeomToMap', geomAttr)
    })

    EventBus.$on('updateGeometryElement', (geomAttr) => {
      this.story.storyBodyElements.forEach( (elem) => {
        if (elem.element_type === 'GEOM') {
          if (elem.geom_attr.id === geomAttr.id) {
            elem.geom_attr = geomAttr
          }
        }
      })
      EventBus.$emit('replaceStoryGeomToMap', geomAttr)
    })

    EventBus.$on('getStoryGeomInfo', (feature) => {
      var geomAttr
      this.story.storyBodyElements.forEach( (elem) => {
        if (elem.element_type === 'GEOM') {
          if (elem.geom_attr.id == feature.getProperties().name) {
            geomAttr = elem.geom_attr
          }
        }
      })
      EventBus.$emit('showStoryGeomInfo', geomAttr)
    })


    EventBus.$on('addMediaToGeomAttr', (geomAttr) => {
      this.mediaForGeomAttr = geomAttr
      this.uploadFileClicked(this.isGeomMedia=true)
    })


    EventBus.$on('showGeomsUsage', (geomsUsage) => {
      this.geomsUsage = geomsUsage
      $('#geomsUsageModal').modal('show')
    })

  },
  methods: {
    closePanel() {
      this.$store.commit('SET_PANEL_OPEN', false)
      EventBus.$emit('removeLayer', 'storyGeomsLayer')
      EventBus.$emit('resetDrawnFeature')
      this.$store.commit('RESTORE_ALL_USEDSTORIESGEOMETRIES')
    },
    reset () {
      this.uploadError = null
      this.uploadedFile = null
      this.tempMediaDescription = null
    },
    addEmptyVueEditor: function () {
      this.story.storyBodyElements.unshift({
        element_type: 'TEXT',
        text: null
      })
    },
    uploadFileClicked () {
      this.reset()
      $('#uploadFileModal').modal('show')
    },
    fileChange (fileList) {

      var FileSize = fileList[0].size / 1024 / 1024; // in MB
        if (FileSize > 500) {
          this.uploadError = 'The file size exceeds 500 MB. Please, upload a smaller media file.'
          fileList = ''
          return
        }

      const formData = new FormData()

      if (!fileList.length) return

      // append the files to FormData
      Array
        .from(Array(fileList.length).keys())
        .map(x => {
          formData.append('file', fileList[x], fileList[x].name)
        })

      this.$store.dispatch('addMedia', formData)
      .then((response) => {
        if (response.ok) {
          if (response.body) {
            this.uploadedFile = response.body
          }
        } else {
          if (response.body[0].indexOf('Request') == -1) {
            this.uploadError = response.body[0]
          } else {
            this.uploadError = response.body.split('Request')[0]
          }
        }
        fileList = ''

      })
      .catch((err) => {
        console.log(err)
      })
    },
    addMediaElement: function () {
      $('#uploadFileModal').modal('hide')
      this.story.storyBodyElements.unshift({
        element_type: imgFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'IMG' : videoFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'VIDEO' : audioFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'AUDIO' : null,
        mediafile_name: this.uploadedFile.name,
        mediafile: this.uploadedFile.id,
        media_description: this.tempMediaDescription
      })
      this.reset()
    },
    drawGeometry: function () {
      this.$store.commit('SET_DRAW_MODE', true)
      EventBus.$emit('addDrawingLayer')
      EventBus.$emit('resetSelectedFeatures')
    },
    reuseGeometry: function () {
      this.$store.commit('SET_REUSE_MODE', true)
      EventBus.$emit('resetSelectedFeatures')
    },
    saveStory: function () {
      EventBus.$emit('resetDrawnFeature')

      var storyform = document.getElementById(this.story.id + "_storyform")

      if (storyform.checkValidity()) {
        // Remove empty text elements from storyBodyElements array
        const elements = this.story.storyBodyElements
        some(this.story.storyBodyElements, function (el, i) {
          if (el.element_type === 'TEXT' && (el.text === undefined || el.text === null || el.text === "")) {
            elements.splice(i, 1)
            return true
          }
        })

        // Assign the order_position attribute
        each(this.story.storyBodyElements, (elem, index) => {
          elem.order_position = index
        })

        // Create or update
        if (this.story.hasOwnProperty('id')) {
          this.$store.dispatch('saveStoryContent', this.story)
        } else {
          this.$store.dispatch('addStory', this.story)
        }
        this.$store.commit('SET_STORY_VIEW_MODE', true)
        this.$store.commit('SET_GEOM_MEDIA_MODE', false)

        // Remove validated class
        storyform.classList.remove("was-validated")
      }else {
        storyform.classList.add("was-validated")
        $('#sidePanel').animate({ scrollTop: 0 }, 'fast')
      }
    },
    showCancelStorySavingModal: function () {
      if (!this.isStoryViewMode) {
        $('#editingWarningModal').modal('show')
      } else {
        this.cancelStorySaving()
      }
    },
    cancelStorySaving: function () {
      this.cleanUnusedMediaFiles()
      this.cleanUnusedGeomAttrs()

      this.$store.commit('SET_STORY_VIEW_MODE', true)
      this.$store.commit('SET_DRAW_MODE', false)
      this.$store.commit('SET_GEOM_MEDIA_MODE', false)
      this.$store.commit('SET_REUSE_MODE', false)

      if (this.story.hasOwnProperty('id')) {
        this.$store.dispatch('getStoryContent', this.story.id)
        .then((story) => {
          EventBus.$emit('addStoryGeomsToMap', story.storyBodyElements)
        })
      } else {
        this.closePanel()
      }
    },
    closeStory: function () {
      if (!this.isStoryViewMode) {
        $('#editingWarningModal').modal('show')
      } else {
        this.closePanel()
      }
    },
    editStory: function () {
      this.$store.commit('SET_STORY_VIEW_MODE', false)
      EventBus.$emit('resetDrawnFeature')
    },
    deleteElementModal: function (element) {
      if (!this.isDrawMode) {
        this.elementToDelete = element
        $('#deleteElementModal').modal('show')
      }
    },
    deleteElement: function () {
      if (this.elementToDelete.hasOwnProperty('id')) {
        this.$store.dispatch('deleteStoryBodyElement', this.elementToDelete)
        .then(() => {
          this.clean()
        })
      } else {
        var index = this.story.storyBodyElements.indexOf(this.elementToDelete)
        if (index > -1) {
            this.story.storyBodyElements.splice(index, 1)
        }
        this.clean()
      }
    },
    clean: function () {
      if (['IMG', 'VIDEO', 'AUDIO'].includes(this.elementToDelete.element_type)) {
        this.cleanUnusedMediaFiles()
      } else if (this.elementToDelete.element_type === 'GEOM') {
        this.cleanUnusedGeomAttrs()
        EventBus.$emit('removeStoryGeomFromMap', this.elementToDelete.geom_attr)
      }
    },
    cleanUnusedMediaFiles: function () {
      this.$store.dispatch('deleteUnusedMediaFiles')
    },
    cleanUnusedGeomAttrs: function () {
      this.$store.dispatch('deleteUnusedGeomAttrs')
    },
    cancelAddMediaElement: function () {
      this.reset()
      this.cleanUnusedMediaFiles()
    },
    zoomToGeometry (element) {
      EventBus.$emit('zoomToGeometry', element.geom_attr)
    },
    editGeometry (geomAttr) {
      EventBus.$emit('editGeomAttr', geomAttr)
    },
    editGeometryStyle (geomAttr) {
      EventBus.$emit('editGeometryStyle', geomAttr)
    },
    magnifyImage (element) {
      this.magnifyImageElem = element
      $('#magnifyImageModal').modal('show')
    },
    manageGeomAttrMedia (geomAttr) {
      this.$store.commit('SET_GEOM_MEDIA_MODE', true)
      this.$store.commit('SET_DRAW_MODE', false)
      EventBus.$emit('zoomToGeometry', geomAttr)
    },
    addGeomAttrMedia () {
      $('#uploadFileModal').modal('hide')
      var geomAttrMedia = {
        geom_attr: this.mediaForGeomAttr.id,
        media_type: imgFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'IMG' : videoFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'VIDEO' : audioFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'AUDIO' : null,
        mediafile_name: this.uploadedFile.name,
        mediafile: this.uploadedFile.id,
        media_description: this.tempMediaDescription
      }

      this.$store.dispatch('addGeometryAttrbMedia', geomAttrMedia)
      .then((response) => {

        this.reset()

        this.story.storyBodyElements.forEach( (elem) => {
          if (elem.element_type === 'GEOM') {
            if (elem.geom_attr.id === this.mediaForGeomAttr.id) {
              // Update this.story
              elem.geom_attr.geomAttribMedia.unshift(response.body)
              // Update drawngeom info
              EventBus.$emit('showStoryGeomInfo', elem.geom_attr)
            }
          }
        })
      })
    },
    openNarrative (story_id, geomAttr) {
      $('#geomsUsageModal').modal('hide')
      if (!this.isStoryViewMode) {
        EventBus.$emit('storyIsBeingEditedWarning')
      } else {
        this.$store.dispatch('getStoryContent', story_id)
        .then((story) => {
          this.$store.commit('SET_STORY_VIEW_MODE', true)
          this.$store.commit('SET_PANEL_OPEN', true)
          EventBus.$emit('addStoryGeomsToMap', story.storyBodyElements)
          delay(() => {
            console.log(geomAttr)
            // EventBus.$emit('zoomToGeometry', geomAttr)
          }, 10)

        })
      }

    }
  }
};
</script>
