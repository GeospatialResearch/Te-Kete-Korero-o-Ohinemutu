<template>
  <div id="sidePanel" :class="{'col-md-6':togglePanel, 'col-md-0':!togglePanel}">
    <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closePanel()" />

    <div v-if="isStoryViewMode" class="mt-5 mb-5">
      <div v-html="story.length == 0 ? 'empty' : 'Story status : '+ story.status " />
      <h4 v-html="story.length == 0 ? '' : story.title" />
      <p v-html="story.length == 0 ? '' : story.summary" />

      <div v-for="element in story.storyBodyElements" :key="element.id">
        <div v-if="element.element_type == 'TEXT'">
          <div v-html="element.text" />
        </div>
        <img v-if="element.element_type == 'IMG'" :src="element.filesystem_path" height="320" width="240">
        <video v-if="element.element_type == 'VIDEO'" width="320" height="240" controls>
          <source :src="element.filesystem_path" type="video/mp4">
          Your browser does not support the video tag.
        </video>
        <audio v-if="element.element_type == 'AUDIO'" controls>
          <source :src="element.filesystem_path" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
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
      <div class="btn-group dropright mb-3">
        <button type="button" class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Add element to the story
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#">New Text field</a>
          <a class="dropdown-item" href="#">New Media file</a>
        </div>
      </div>

      <div class="sidebar-item sidebar-search">
        <div class="input-group">
          <button type="button" name="upload-file" class="btn btn-sm btn-warning" @click="uploadFileClicked">
            Upload media file <i aria-hidden="true"><font-awesome-icon icon="folder-open" /></i>
          </button>
        </div>
      </div>

      <div class="row col-md-12">
        <draggable :disabled="!enabled" class="list-group" ghost-class="ghost" @start="dragging = true" @end="dragging = false">
          <div v-for="element in story.storyBodyElements" :key="element.id" class="row mb-2">
            <div v-if="element.element_type == 'TEXT'" class="col-md-11">
              <vue-editor v-model="element.text" :editor-toolbar="customToolbar" class="custom-ql-editor" />
            </div>
            <img v-if="element.element_type == 'IMG'" :src="element.filesystem_path" height="320" width="240">
            <video v-if="element.element_type == 'VIDEO'" width="320" height="240" controls>
              <source :src="element.filesystem_path" type="video/mp4">
              Your browser does not support the video tag.
            </video>
            <audio v-if="element.element_type == 'AUDIO'" controls>
              <source :src="element.filesystem_path" type="audio/mpeg">
              Your browser does not support the audio element.
            </audio>
            <div class="col-md-1">
              <font-awesome-icon icon="times-circle" size="lg" color="grey" class="delete-element" @click="deleteElement()" />
            </div>
          </div>
        </draggable>
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
              <!-- <select id="fileType" v-model="fileType">
                <option v-for="option in file_options" :key="option.value">
                  {{ option.text }}
                </option>
              </select> -->
              <!-- <input id="fileDescription" v-model="fileDescription" type="text"> -->
              <form v-if="!uploadError" novalidate>
                <div class="dropbox">
                  <input type="file" :name="uploadFieldName" class="input-file" @change="fileChange($event.target.files)">
                  <p>
                    Click to browse or drop a media file (video/audio/image) here
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
              <button type="button" class="btn btn-primary" data-dismiss="modal" @click="save()">
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
          <font-awesome-icon icon="share-alt" class="mr-2" @click="deleteElement()" />
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#">Co-create story</a>
          <a class="dropdown-item" href="#">Share story</a>
          <a class="dropdown-item" href="#">Submit story</a>
          <a class="dropdown-item" href="#">Publish story</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable"
import { VueEditor } from "vue2-editor"
import api from 'store/api.js'
const apiRoot = process.env.API_HOST + '/v1'
export default {
  components: {
    draggable,
    VueEditor
  },
  data() {
    return {
      fileType: '',
      fileDescription: '',
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
        ['blockquote'],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'indent': '-1'}, { 'indent': '+1' }],
        [{ 'color': [] }, { 'background': [] }],
        ['link']
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
    reset () {
      this.uploadError = null
    },
    save(){
      console.log("SAVING ..............................")
      const formData = new FormData()

      // console.log(this.fileType)
      // formData.append("fileType",this.fileType)
      // console.log(this.fileDescription)
      // formData.append("fileDescription",this.fileDescription)
      //
      // this.$store.state.storyBodyContent.file_type = this.fileType
      // this.$store.state.storyBodyContent.name = this.fileDescription
      // console.log("storyBodyContent from STATE")
      // console.log(this.$store.state.storyBodyContent)
      const fileList = this.$store.state.storyBodyContent.file_system_path

      // append the files to FormData
      Array
        .from(Array(fileList.length).keys())
        .map(x => {
          formData.append('mediafile', fileList[x], fileList[x].name)
        })

        api.post(apiRoot + '/upload_story_body_file/', formData, {
          progress(e) {
            if (e.lengthComputable) {
              console.log(e.loaded / e.total * 100);
            }
          }
        })
          .then((response) => {
            console.log(response)
            // this.$store.state.elements.push({
            //     file_type : this.fileType,
            //     name : this.fileDescription,
            //     file_system_path : response.body.file_system_path
            // })
          })

        // let response= this.$store.dispatch('uploadStoryBodyFile', formData)


        // console.log("elements from state......")
        // console.log(this.$store.state.elements)
        // // console.log("storyBodyContent clearing......")
        // //
        // this.$store.state.storyBodyContent = {
        //   file_type : 'IMG',
        //   name : '',
        //   file_system_path : ''
        // }
      // // dispatch action to upload file
      //this.$store.dispatch('uploadStoryBodyFile', formData)
    },
    fileChange (fileList) {
      // handle file changes
      console.log("file change here............................. ")
      console.log(fileList)
      this.$store.state.storyBodyContent.file_system_path = fileList
    },
    uploadFileClicked () {
      console.log("uploadFileClicked")
      this.reset()
      $('#uploadFileModal').modal('show')
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
    }
  }
};
</script>
