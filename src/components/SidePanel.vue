<template>
  <div :class="{'col-md-6':togglePanel, 'col-md-0':!togglePanel}">
    <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closePanel()" />
    <div class="mt-5 mb-5">
      <h3>{{ story.hasOwnProperty('content') ? story.content.title : '' }}</h3>
      <p>{{ story.hasOwnProperty('content') ? story.content.summary : '' }}</p>
    </div>

    <div class="row col-md-6">
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
import draggable from "vuedraggable";
export default {
  components: {
    draggable
  },
  data() {
    return {
      enabled: true,
      dragging: false
    };
  },
  computed: {
    draggingInfo() {
      return this.dragging ? "under drag" : "";
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
    }
  }
};
</script>
