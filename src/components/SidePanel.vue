<template>
  <div id="sidePanel" :class="{'col-md-6':togglePanel, 'col-md-0':!togglePanel}">
    <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closePanel()" />

    <div v-if="isStoryViewMode" class="mt-5 mb-5">
      <span class="badge badge-warning mb-2" style="vertical-align: middle;">{{ story.status }}</span>
      <h4 v-html="story.length == 0 ? '' : story.title" />
      <p class="story-summary" v-html="story.length == 0 ? '' : story.summary" />
      <hr />

      <div v-for="element in story.storyBodyElements" :key="element.id" class="col-md-12">
        <div v-if="element.element_type == 'TEXT'">
          <div v-html="element.text" class="ql-text" />
        </div>
        <div class="align-center">
          <img v-if="element.element_type == 'IMG'" :src="mediaRoot + element.mediafile_name" class="story-elem-img">
          <video v-if="element.element_type == 'VIDEO'" controls class="story-elem-video">
            <source :src="mediaRoot + element.mediafile_name" type="video/mp4">
            Your browser does not support the video tag.
          </video>
          <audio v-if="element.element_type == 'AUDIO'" controls>
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
        <button type="button" class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Add element to the story
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#" @click="addEmptyVueEditor()">New Text field</a>
          <a class="dropdown-item" href="#" @click="uploadFileClicked()">Upload Media file</a>
        </div>
      </div>

      <div class="row col-md-12">
        <draggable v-model="story.storyBodyElements" ghost-class="ghost" handle=".handle" @start="dragging = true" @end="dragging = false">
          <div v-for="element in story.storyBodyElements" id="editor" :key="element.id" class="row mb-2">
            <div class="col-md-11 mt-3">
              <div class="text-center">
                <button class="btn btn-sm btn-secondary drag-element handle">
                  Drag me
                  <i class="fas fa-arrows-alt" />
                </button>
              </div>
              <div v-if="element.element_type == 'TEXT'">
                <vue-editor v-model="element.text" :editor-toolbar="customToolbar" class="custom-ql-editor" />
              </div>
              <div class="align-center">
                <img v-if="element.element_type == 'IMG'" :src="mediaRoot + element.mediafile_name" class="story-elem-img">
                <video v-if="element.element_type == 'VIDEO'" controls class="story-elem-video">
                  <source :src="mediaRoot + element.mediafile_name" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
                <audio v-if="element.element_type == 'AUDIO'" controls class="col-md-12">
                  <source :src="mediaRoot + element.mediafile_name" type="audio/mpeg">
                  Your browser does not support the audio element.
                </audio>
              </div>
              <textarea v-if="element.element_type != 'TEXT'" v-model="element.media_description" rows="1" class="form-control form-control-sm mt-1" title="Media description" placeholder="Media description (optional)" />
            </div>
            <div class="col-md-1 delete-element">
              <font-awesome-icon icon="times-circle" size="lg" color="grey" class="handle" @click="deleteElementModal(element)" />
            </div>
          </div>
        </draggable>
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
              <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelAddMediaElement()">
                <span v-if="!uploadError">Cancel</span>
                <span v-else>Close</span>
              </button>
              <button v-if="!uploadError" type="button" class="btn btn-primary" data-dismiss="modal" @click="addMediaElement()">
                Add
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="clear" />
    <div :class="[togglePanel ? 'visible': 'invisible', 'row sidepanel-footer']">
      <button v-if="story.hasOwnProperty('id') && !isStoryViewMode" type="button" class="btn btn-success" @click="saveStory()">
        Update story
      </button>
      <button v-if="!story.hasOwnProperty('id') && !isStoryViewMode" type="button" class="btn btn-success" @click="saveStory()">
        Save story
      </button>
      <button v-if="!isStoryViewMode" type="button" class="btn btn-danger ml-2" @click="cancelStorySaving()">
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
  </div>
</template>

<script>
import draggable from "vuedraggable"
import { VueEditor } from "vue2-editor"
import { imgFormats, videoFormats, audioFormats } from 'utils/objectUtils'
import { some, each } from 'underscore'

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
      elementToDelete: null
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
    }
  },
  methods: {
    closePanel() {
      this.$store.commit('SET_PANEL_OPEN', false)
    },
    addEmptyVueEditor: function () {
      this.story.storyBodyElements.unshift({
        element_type: 'TEXT',
        text: null
      })
    },
    reset () {
      this.uploadError = null
      this.uploadedFile = null
      this.tempMediaDescription = null
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
    saveStory: function () {
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

        // Remove validated class
        storyform.classList.remove("was-validated")
      }else {
        storyform.classList.add("was-validated")
        $('#sidePanel').animate({ scrollTop: 0 }, 'fast')
      }
    },
    cancelStorySaving: function () {
      this.cleanUnusedMediaFiles()
      this.closePanel()
      this.$store.commit('SET_STORY_VIEW_MODE', true)
    },
    editStory: function () {
      this.$store.commit('SET_STORY_VIEW_MODE', false)
    },
    deleteElementModal: function (element) {
      this.elementToDelete = element
      $('#deleteElementModal').modal('show')
    },
    deleteElement: function () {
      if (this.elementToDelete.hasOwnProperty('id')) {
        this.$store.dispatch('deleteStoryBodyElement', this.elementToDelete)
        .then(() => {
          if (this.elementToDelete.element_type != 'TEXT') {
            this.cleanUnusedMediaFiles()
          }
        })
      } else {
        var index = this.story.storyBodyElements.indexOf(this.elementToDelete)
        if (index > -1) {
            this.story.storyBodyElements.splice(index, 1)
        }
        if (this.elementToDelete.element_type != 'TEXT') {
          this.cleanUnusedMediaFiles()
        }
      }
    },
    cleanUnusedMediaFiles: function () {
      this.$store.dispatch('deleteUnusedMediaFiles')
    },
    cancelAddMediaElement: function () {
      this.reset()
      this.cleanUnusedMediaFiles()
    }
  }
};
</script>
