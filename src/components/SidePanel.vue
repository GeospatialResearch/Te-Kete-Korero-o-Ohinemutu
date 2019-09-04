<template>
  <div :class="{'col-md-6':togglePanel, 'col-md-0':!togglePanel}">
    <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closePanel()" />
    <div class="mt-5 mb-5">
      <h3>{{ story.hasOwnProperty('content') ? story.content.title : '' }}</h3>
      <p>{{ story.hasOwnProperty('content') ? story.content.summary : '' }}</p>
    </div>

    <button type="button" name="save-content" class="btn btn-primary" @click="saveStoryContent()">
      Save
    </button>

    <div class="row col-md-12">
      <h2>Drag and Drop</h2>
      <!-- <h4>Draggable {{ draggingInfo }}</h4> -->

      <draggable
        :disabled="!enabled"
        class="list-group"
        ghost-class="ghost"
        @start="dragging = true"
        @end="dragging = false"
      >
        <div class="list-group-item">
          <vue-editor v-if="story.hasOwnProperty('content')" v-model="story.content.summary" :editor-toolbar="customToolbar" />
        </div>
        <div class="list-group-item">
          <img id="id1" src="static/img/test_img.gif" dropable="false" width="150" height="31">
        </div>
        <div class="list-group-item">
          <img id="id2" src="static/img/favicon.png" dropable="false" width="150" height="31">
        </div>
        <div class="list-group-item">
          <iframe id="id3" dropable="false" width="188" height="100" src="https://www.youtube.com/embed/tgbNymZ7vqY" />
        </div>
        <div class="list-group-item">
          <input id="id4" type="text" name="name" placeholder="Name" dropable="false" width="130" height="31">
        </div>
        <div class="list-group-item">
          <textarea id="id5">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</textarea>
        </div>
      </draggable>
    </div>
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
      enabled: true,
      dragging: false,
      content: "",
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
        ['link', 'formula'],
        ['clean'],
      ],
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
    saveStoryContent: function (){
     this.$store.dispatch('saveStoryContent', this.story)
   }
  }
};
</script>
