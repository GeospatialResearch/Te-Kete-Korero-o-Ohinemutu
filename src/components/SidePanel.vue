<template>
  <div class="col-md-4">

   <h2>Form</h2>
   <p>Form elements to be displayed here.</p>
   <p>
     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
   </p>

   <h2>Drag and Drop</h2>

    <div class="col-6">
      <h4>Draggable {{ draggingInfo }}</h4>

      <draggable
        :disabled="!enabled"
        class="list-group"
        ghost-class="ghost"
        @start="dragging = true"
        @end="dragging = false"
      >

        <div class="list-group-item"><img id="id1" src="static/img/test_img.gif" dropable="false" width="150" height="31"></div>
        <div class="list-group-item"><img id="id2" src="static/img/favicon.png" dropable="false" width="150" height="31"></div>
        <div class="list-group-item"><iframe id="id3" dropable="false" width="188" height="100" src="https://www.youtube.com/embed/tgbNymZ7vqY"></iframe></div>
        <div class="list-group-item"><input  id="id4" type="text" name="name" placeholder="Name" dropable="false" width="130" height="31"></div>
        <div class="list-group-item"><textarea id="id5">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</textarea></div>
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
    }
  },
  methods: {
  }
};
</script>
