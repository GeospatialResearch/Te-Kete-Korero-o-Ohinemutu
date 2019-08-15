<template>
  <div class="col-md-4">

    <h2>Form</h2>
    <p>Form elements to be displayed here.</p>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    </p>

    <h2>Drag and Drop</h2>
    <div class="droptarget" v-on:drop="drop" v-on:dragover="allowDrop">
      <!-- html elements should have ids for the elements to be dropable -->
      <img src="static/img/test_img.gif" id="dragtarget1"  v-on:dragstart="dragStart" v-on:drag="dragging" draggable="true" width="88" height="31">
      <p  id="dragtarget2"  v-on:dragstart="dragStart" v-on:drag="dragging" draggable="true">Drag me!</p>
      <img src="static/img/favicon.png" id="dragtarget3"  v-on:dragstart="dragStart" v-on:drag="dragging" draggable="true" width="88" height="31">
      <div  id="dragtarget4"  v-on:dragstart="dragStart" v-on:drag="dragging" draggable="true">

        <iframe id="frame" width="120" height="100" src="https://www.youtube.com/embed/tgbNymZ7vqY"></iframe>

      </div>
    </div>
    <p style="clear:both;">
      <strong>Note:</strong> drag events are not supported in Internet
      Explorer 8 and earlier versions or Safari 5.1 and earlier versions.
    </p>
    <p id="demo"></p>
  </div>
</template>
<script>

export default {
    methods: {
      dragStart:function(event)  {
        event.dataTransfer.setData("Text", event.target.id);
      },
      dragging:function(event) {
        console.log(event)
        document.getElementById("demo").innerHTML =
          "The element is being dragged";
      },
      allowDrop:function(event) {
        event.preventDefault();
      },
      drop:function(event) {
        event.preventDefault();
        var data = event.dataTransfer.getData("Text");
        event.target.appendChild(document.getElementById(data));
        document.getElementById("demo").innerHTML =
          "The element was dropped";
      }
    }
}
</script>
