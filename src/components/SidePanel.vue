<template>
  <div class="col-md-4">

    <h2>Form</h2>
    <p>Form elements to be displayed here.</p>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    </p>

    <h2>Drag and Drop</h2>
    <div class="droptarget " v-on:drop="drop" v-on:dragover="allowDrop">
      <!-- html elements should have ids for the elements to be dropable -->
      <div  id="dragtarget1"  class="dragdiv nodrop" v-on:dragstart="dragStart"  dropable="false" v-on:drag="dragging" draggable="true">
        <img id="id1" src="static/img/test_img.gif" dropable="false" draggable="false" width="88" height="31">
      </div>
      <div  id="dragtarget2"  class="dragdiv nodrop" v-on:dragstart="dragStart"  dropable="false" v-on:drag="dragging" draggable="true">
        Drag me!
      </div>
      <div  id="dragtarget3"  class="dragdiv nodrop" v-on:dragstart="dragStart"  dropable="false" v-on:drag="dragging" draggable="true">
        <img  id="id3" src="static/img/favicon.png" dropable="false" draggable="false" width="88" height="31">
      </div>
      <div  id="dragtarget4"  class="dragdiv nodrop" v-on:dragstart="dragStart"  dropable="false" v-on:drag="dragging" draggable="true">
        <iframe id="id4" dropable="false" width="88" height="100" src="https://www.youtube.com/embed/tgbNymZ7vqY"></iframe>
      </div>
      <div  id="dragtarget5" class="dragdiv nodrop" v-on:dragstart="dragStart"  dropable="false" v-on:drag="dragging" draggable="true">
        <input  id="id5" type="text" name="name" placeholder="Name" dropable="false" width="30" height="31">
      </div>
      <div  id="dragtarget6" class="dragdiv nodrop" v-on:dragstart="dragStart"  dropable="false" v-on:drag="dragging" draggable="true">
        <textarea id="id6" dropable="false" rows="4" cols="10">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        </textarea>
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
        document.getElementById("demo").innerHTML
          "The element is being dragged";
      },
      allowDrop:function(event) {
        event.preventDefault();
      },
      drop:function(event) {
        event.preventDefault();
        if (event.target.classList.contains('nodrop')) {
          alert("You can't drop inside another element")
        }
        else {
          var data = event.dataTransfer.getData("Text");
          event.target.appendChild(document.getElementById(data));
          document.getElementById("demo").innerHTML =
            "The element was dropped";
        }

      }
    }
}
</script>
