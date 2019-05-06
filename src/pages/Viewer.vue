<template>
  <div class="viewer-container">
    <div class="row">
      <left-side-bar />
      <main-map />
    </div>
  </div>
</template>

<script>

import LeftSideBar from 'components/LeftSideBar'
import MainMap from 'components/Map/MainMap.vue'

export default {
  components: {
    MainMap,
    LeftSideBar
  }
}
</script>
