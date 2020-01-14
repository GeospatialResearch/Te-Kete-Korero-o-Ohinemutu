<template>
  <div>
    <!-- page-content  -->
    <main class="page-content">
      <div id="overlay" class="overlay" />
      <div class="container-fluid">
        <div id="navbar" class="row navbar">
          <div class="align-self-center">
            <a id="toggle-sidebar" class="btn-sm btn-dark mr-2" href="#" title="Toggle sidebar">
              <font-awesome-icon icon="bars" />
            </a>
            <a id="pin-sidebar" class="btn-sm btn-dark mr-2" href="#" title="Pin sidebar">
              <font-awesome-icon icon="map-pin" />
            </a>
            <select v-model="selectedValue" class="btn btn-sm btn-secondary dropdown-toggle" @change="onChange">
              <option value="eng">
                English
              </option>
              <option value="mao">
                Te Reo
              </option>
            </select>
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
    data () {
      return {
        selectedValue: "eng"
      }
    },
    computed: {
      contentToShow () {
        return this.$store.state.contentToShow
      }
    },
    methods: {
      onChange:function(){
        // Update the store with the new language
        this.$store.commit('SET_LANG', this.selectedValue)
       }
    }
  }

</script>
