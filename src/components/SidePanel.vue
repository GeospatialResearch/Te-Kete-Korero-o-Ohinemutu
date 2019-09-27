<template>
  <div :class="{'col-md-6 scroll-div':togglePanel, 'col-md-0':!togglePanel}">
    <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closePanel()" />
    <div class="mt-5 mb-5">
      <h3>{{ story.hasOwnProperty('content') ? story.content.title : '' }}</h3>
      <p>{{ story.hasOwnProperty('content') ? story.content.summary : '' }}</p>
      <p>{{ story.length == 0 ? 'empty' : story.content.status }}</p>
    </div>

    <!-- sidepanel upload file  -->
    <div class="sidebar-item sidebar-search">
      <div class="input-group">
        <span class="input-group-text">
          <button type="button" name="upload-file" class="btn btn-warning" @click="uploadFileClicked">
            Upload (video/audio/image)   <i aria-hidden="true"><font-awesome-icon icon="folder-open" /></i>
          </button>
        </span>
      </div>
    </div>
    <div id="uploadFileModal" class="modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Upload file
            </h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <select>
              <option v-for="option in file_options" :key="option.value">
                {{ option.text }}
              </option>
            </select>
            <form v-if="!uploadError" enctype="multipart/form-data" novalidate>
              <p class="text-center">
                <strong>Upload a vector dataset (zipped shapefile or geojson file) or a raster file</strong>
              </p>
              <div class="dropbox">
                <input type="file" :name="uploadFieldName" class="input-file" @change="fileChange($event.target.files)">
                <p>
                  Click to browse or drop something here
                </p>
              </div>
            </form>
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
          </div>
        </div>
      </div>
    </div>
    <!-- <h4> Drag and drop </h4> -->
    <div class="row col-md-12">
      <!-- <h4>Draggable {{ draggingInfo }}</h4> -->
      <draggable :disabled="!enabled" class="list-group" ghost-class="ghost" @start="dragging = true" @end="dragging = false">
        <div class="list-group-item">
          <vue-editor v-model="story.content.title" :editor-toolbar="customToolbar" style="max-height: 120px; overflow-y: scroll" placeholder="Story Title" />
        </div>
        <div class="list-group-item">
          <vue-editor v-model="story.content.summary" :editor-toolbar="customToolbar" style="height: 200px; overflow-y: scroll" placeholder="Story Summary" />
        </div>
        <div class="list-group-item">
          <select v-model="story.content.status">
            <option v-for="option in status_options" :key="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>
        <!-- <div class="list-group-item">
        <iframe id="id3" dropable="false" width="188" height="100" src="https://www.youtube.com/embed/tgbNymZ7vqY" />
        </div>-->
      </draggable>
    </div>
    <button v-if="story.content.hasOwnProperty('id')" type="button" name="update-content" class="btn btn-primary" @click="saveStoryContent()">
      Update Story
    </button>
    <button v-else type="button" name="save-content" class="btn btn-primary" @click="addStory()">
      Save Story
    </button>
  </div>
</template>

<script>
import draggable from "vuedraggable"
import { VueEditor } from "vue2-editor"

export default {
  components: {
    draggable,
    VueEditor
  },
  data() {
    return {
      uploadFieldName: 'file',
      uploadError: null,
      enabled: true,
      dragging: false,
      storyContent:{},
      customToolbar: [
        [{ 'font': [] }],
        [{ 'header': [false, 1, 2, 3, 4, 5, 6, ] }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{'align': ''}, {'align': 'center'}, {'align': 'right'}, {'align': 'justify'}],
        [{ 'header': 1 }, { 'header': 2 }],
        ['blockquote', 'code-block'],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],
        [{ 'color': [] }, { 'background': [] }],
        ['link'],
        ['clean'],
      ],
      status_options: [
      { text: 'DRAFT', value: 'DRAFT' },
      { text: 'SUBMITTED', value: 'SUBMITTED' },
      { text: 'ACCEPTED', value: 'ACCEPTED' },
      { text: 'PUBLISHED', value: 'PUBLISHED' }
      ],
      file_options: [
      { text: 'IMG', value: 'IMG' },
      { text: 'AUDIO', value: 'AUDIO' },
      { text: 'VIDEO', value: 'VIDEO' }
      ]
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
    }
  },
  methods: {
    closePanel() {
      this.$store.commit('SET_PANEL_OPEN', false)
    },
    reset () {
      this.uploadError = null
    },
    fileChange (fileList) {
      // handle file changes
      console.log("file change here............................. "+fileList)
      const formData = new FormData()

      if (!fileList.length) return

      // append the files to FormData
      Array
        .from(Array(fileList.length).keys())
        .map(x => {
          formData.append('file', fileList[x], fileList[x].name)
        })

      // close the modal
      $('#uploadFileModal').modal('hide')

      // dispatch action to upload file
      this.$store.dispatch('uploadStoryBodyFile', formData)
      // .then(response => {
      //   if (response.ok) {
      //     if (response.body) {
      //       EventBus.$emit('addLayer', response.body)  // add argument false if you want to add geojson layer
      //     }
      //     this.$store.state.isUploadingData = false
      //     this.reset()
      //   } else {
      //     if (response.body.indexOf('Request') == -1) {
      //       this.uploadError = response.body[0]
      //     } else {
      //       this.uploadError = response.body.split('Request')[0]
      //     }
      //
      //     $('#uploadFiletModal').modal('show')
      //
      //   }
      //   fileList = ''
      // })
      // .catch(err => {
      //   console.error(err)
      //   // this.uploadError = err.response.body.detail
      //   // this.currentStatus = STATUS_FAILED
      //   fileList = ''
      // })
    },
    uploadFileClicked () {
      console.log("uploadFileClicked")
      this.reset()
      $('#uploadFileModal').modal('show')
    },
    saveStoryContent: function (){
      console.log("saveStoryContent from vue",this.story)
      this.$store.dispatch('saveStoryContent', this.story)
      },
    addStory: function (){
      console.log("addStory from vue")
      this.$store.dispatch('addStory', this.story)
    }

  }
};
</script>
