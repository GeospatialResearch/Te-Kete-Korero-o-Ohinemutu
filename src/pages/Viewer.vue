<template>
  <div class="page-wrapper default-theme sidebar-bg bg1 toggled viewer-container">
    <div class="row">
      <side-bar />
      <content-view />
    </div>
  </div>
</template>

<script>

// import LeftSideBar from 'components/LeftSideBar'
import SideBar from 'components/SideBar'
import ContentView from 'components/ContentView'
// import MainMap from 'components/Map/MainMap.vue'

export default {
  components: {
    // MainMap,
    SideBar,
    ContentView
  }
}
</script>
