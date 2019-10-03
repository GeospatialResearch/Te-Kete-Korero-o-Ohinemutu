<template>
  <div id="sidePanel" :class="{'col-md-6':togglePanel, 'col-md-0':!togglePanel}">
    <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closePanel()" />

    <div v-if="isStoryViewMode" class="mt-5 mb-5">
      <div v-html="story.length == 0 ? 'empty' : 'Story status : '+ story.status " />
      <h4 v-html="story.length == 0 ? '' : story.title" />
      <p v-html="story.length == 0 ? '' : story.summary" />
      <hr />

      <div v-for="element in story.storyBodyElements" :key="element.id" class="col-md-12">
        <div v-if="element.element_type == 'TEXT'">
          <div v-html="element.text" />
        </div>
        <div class="align-center">
          <img v-if="element.element_type == 'IMG'" :src="mediaRoot + element.mediafile_name" class="story-elem-img">
          <video v-if="element.element_type == 'VIDEO'" controls class="story-elem-video">
            <source :src="mediaRoot + element.mediafile_name" type="video/mp4" >
            Your browser does not support the video tag.
          </video>
          <audio v-if="element.element_type == 'AUDIO'" controls>
            <source :src="mediaRoot + element.mediafile_name" type="audio/mpeg">
            Your browser does not support the audio element.
          </audio>
          <p v-if="element.element_type != 'TEXT'">
            {{ element.media_description }}
          </p>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="row col-md-12">
        <h5 class="mb-0">
          Title
        </h5>
        <input v-model="story.title" type="text" class="form-control form-control-sm mb-3" title="Title of the story">
        <h5 class="mb-0">
          Summary
        </h5>
        <textarea v-model="story.summary" class="form-control form-control-sm" title="Story summary" />
      </div>

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
        <draggable :disabled="!enabled" class="list-group" ghost-class="ghost" @start="dragging = true" @end="dragging = false">
          <div v-for="element in story.storyBodyElements" :key="element.id" class="row mb-2">
            <div class="col-md-11 mt-3">
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
            <div class="col-md-1">
              <font-awesome-icon icon="times-circle" size="lg" color="grey" class="delete-element" @click="deleteElementModal(element)" />
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
              </form>
              <h6 class="mb-1 mt-3">
                Media description (optional)
              </h6>
              <textarea v-model="tempMediaDescription" class="form-control form-control-sm" title="Media description" />
              <div v-if="uploadError" class="alert alert-danger text-center">
                <h5>Upload failed with error:</h5>
                <code>{{ uploadError }}</code>
                <hr>
                <p>Please check that your data is valid and try again.</p>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="reset()">
                Close
              </button>
              <button type="button" class="btn btn-primary" data-dismiss="modal" @click="addMediaElement()">
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="clear" />
    <div :class="[togglePanel ? 'visible': 'invisible', 'row sidepanel-footer']">
      <button v-if="story.hasOwnProperty('id') && !isStoryViewMode" type="button" class="btn btn-success" @click="saveStoryContent()">
        Update story
      </button>
      <button v-if="!story.hasOwnProperty('id') && !isStoryViewMode" type="button" class="btn btn-success" @click="addStory()">
        Save story
      </button>
      <button v-if="!isStoryViewMode" type="button" class="btn btn-danger ml-2" @click="closePanel()">
        Cancel
      </button>
      <button v-if="story.hasOwnProperty('id') && isStoryViewMode" type="button" class="btn btn-primary" @click="editStory()">
        Edit story
      </button>
      <div v-if="isStoryViewMode" class="btn-group dropup">
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
      enabled: true,
      dragging: false,
      customToolbar: [
        // [{ 'font': [] }],
        // [{ 'header': [false, 1, 2, 3, 4, 5, 6, ] }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        ['bold', 'italic', 'underline'],
        [{'align': ''}, {'align': 'center'}, {'align': 'right'}, {'align': 'justify'}],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],
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
    storyBody(){
      return this.$store.state.storyBodyContent
    },
    isStoryViewMode (){
      return this.$store.state.storyViewMode
    },
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
        this.uploadedFile = response.body
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
    saveStoryContent: function () {
      console.log("saveStoryContent from vue",this.story)
      this.$store.dispatch('saveStoryContent', this.story)
      },
    addStory: function () {
      console.log(this.story)
      this.$store.dispatch('addStory', this.story)
    },
    editStory: function () {
      this.$store.commit('SET_STORY_VIEW_MODE', false)
    },
    deleteElementModal: function (element) {
      this.elementToDelete = element
      $('#deleteElementModal').modal('show')
    },
    deleteElement: function () {
      this.$store.dispatch('deleteStoryBodyElement', this.elementToDelete)
      .then(() => {
        if (this.elementToDelete.element_type != 'TEXT') {
          this.$store.dispatch('deleteUnusedMediaFiles')
        }
      })

    }
  }
};
</script>
