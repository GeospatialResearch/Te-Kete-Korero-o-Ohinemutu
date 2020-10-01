<template>
  <div class="page-wrapper default-theme sidebar-bg bg1 viewer-container toggled" :style="contentToShow=='map'?'overflow-y: hidden;':'overflow-y: auto;'">
    <!-- toggled -->
    <side-bar />
    <content-view />
  </div>
</template>

<script>

import SideBar from 'components/SideBar'
import ContentView from 'components/ContentView'

export default {
  components: {
    SideBar,
    ContentView
  },
  computed: {
    contentToShow () {
      return this.$store.state.contentToShow
    }
  },
}
</script>
