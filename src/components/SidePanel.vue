<template>
  <div :class="{'col-md-6 scroll-div':togglePanel, 'col-md-0':!togglePanel}">
    <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closePanel()" />
    <div v-if="isStoryViewMode" class="mt-5 mb-5">
      <h4 v-html="story.length == 0 ? 'empty' : 'Story status : '+story.content.status " />
      <h3 v-html="story.hasOwnProperty('content') ? story.content.title : '' " />
      <p v-html="story.hasOwnProperty('content') ? story.content.summary : '' " />
    </div>
    <div v-else>
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
              <select id="fileType" v-model="fileType">
                <option v-for="option in file_options" :key="option.value">
                  {{ option.text }}
                </option>
              </select>
              <input id="fileDescription" v-model="fileDescription" type="text">
              <form v-if="!uploadError" novalidate>
                <p class="text-center">
                  <strong>Upload a file</strong>
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
              <button type="button" class="btn btn-primary" data-dismiss="modal" @click="save()">
                Save
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
          <li v-for="element in this.$store.state.elements" :key="element.id">
            <span class="ml-2"> {{ element.file_system_path }}</span>
          </li>
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
      storyContent:{},
      storyBodyContent:{},
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
          formData.append('file', fileList[x], fileList[x].name)
        })

        api.post(apiRoot + '/upload_story_body_file/', formData)
          .then((response) => {
            console.log(response)
            this.$store.state.elements.push({
                file_type : this.fileType,
                name : this.fileDescription,
                file_system_path : response.body.file_system_path
            })
          })

        // let response= this.$store.dispatch('uploadStoryBodyFile', formData)


        console.log("elements from state......")
        console.log(this.$store.state.elements)
        // console.log("storyBodyContent clearing......")
        //
        this.$store.state.storyBodyContent = {
          file_type : 'IMG',
          name : '',
          file_system_path : ''
        }
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
