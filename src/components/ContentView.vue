<template>
  <div>
    <!-- page-content  -->
    <main class="page-content">
      <div id="overlay" class="overlay" />
      <div class="container-fluid">
        <div id="navbar" class="row p-4 navBar">
          <div class="align-self-center">
            <a id="toggle-sidebar" class="btn-sm btn-dark mr-2" href="#" title="Toggle sidebar">
              <font-awesome-icon icon="bars" />
            </a>
            <a id="pin-sidebar" class="btn-sm btn-dark" href="#" title="Pin sidebar">
              <font-awesome-icon icon="map-pin" />
            </a>
          </div>
        </div>
        <div class="row">
          <main-map v-show="contentToShow=='map'" />
          <content-info v-show="contentToShow=='themes'" />
          <side-panel v-show="contentToShow=='map'" />
        </div>
      </div>
    </main>
    <!-- page-content" -->
  </div>
</template>

<script>
  import 'utils/sidebar'
  import MainMap from 'components/Map/MainMap'
  import ContentInfo from 'components/ContentInfo'
  import SidePanel from 'components/SidePanel'

  export default {
    components: {
      MainMap,
      ContentInfo,
      SidePanel
    },
    computed: {
      contentToShow () {
        return this.$store.state.contentToShow
      }
    }
  }

</script>
