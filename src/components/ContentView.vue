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
        <main-map v-show="contentToShow=='map'" />
        <content-info v-show="contentToShow=='themes'" />
      </div>
    </main>
    <!-- page-content" -->
  </div>
</template>

<script>
  import 'utils/sidebar'
  import MainMap from 'components/Map/MainMap'
  import ContentInfo from 'components/ContentInfo'

  export default {
    components: {
      MainMap,
      ContentInfo
    },
    computed: {
      contentToShow () {
        return this.$store.state.contentToShow
      }
    }
  }

</script>
