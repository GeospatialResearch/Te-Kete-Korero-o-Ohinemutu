<template>
  <div>
    <!-- page-content  -->
    <main class="page-content">
      <div id="overlay" class="overlay" />
      <div class="container-fluid">
        <div id="navbar" class="row navbar">
          <div>
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

          <button v-if="!authenticated" class="btn btn-sm btn-success" type="button" @click="showLoginModal()">
            Login
          </button>
          <button v-else class="btn btn-sm btn-outline-danger" type="button" @click="showLogoutModal()">
            Logout
          </button>
        </div>
        <div class="row">
          <main-map v-show="contentToShow=='map'" />
          <content-info v-show="contentToShow=='themes'" />
          <side-panel v-show="contentToShow=='map'" />
        </div>
      </div>
    </main>
    <!-- page-content" -->
    <div id="loginModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content modal-margin-top">
          <div class="modal-header" />
          <div class="modal-body">
            <log-in @close="closeModal()" />
          </div>
        </div>
      </div>
    </div>
    <div id="logoutModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              Attention
            </h4>
          </div>
          <div class="modal-body">
            <p class="mb-0">
              Are you sure you want to log out?
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="$store.dispatch('logOut')">
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import 'utils/sidebar'
  import { EventBus } from 'store/event-bus'
  import MainMap from 'components/Map/MainMap'
  import ContentInfo from 'components/ContentInfo'
  import SidePanel from 'components/SidePanel'
  import LogIn from 'components/account/Login'

  export default {
    components: {
      MainMap,
      ContentInfo,
      SidePanel,
      LogIn
    },
    data () {
      return {
        selectedValue: "eng",
        showLogin: false
      }
    },
    computed: {
      contentToShow () {
        return this.$store.state.contentToShow
      },
      username () {
        return this.$store.state.user.username
      },
      authenticated () {
        return this.$store.state.authenticated
      }
    },
    beforeCreate: function () {
      // Check if the token is still valid, if yes set login, if not deauthenticate.
      this.$store.dispatch('getUser')
    },
    methods: {
      onChange (){
        // Update the store with the new language
        this.$store.commit('SET_LANG', this.selectedValue)
      },
      showLoginModal () {
        EventBus.$emit('closePanel')
        EventBus.$emit('removeWasValidated')
        $('#loginModal').modal('show')
      },
      closeModal () {
        $('#loginModal').modal('hide')
      },
      showLogoutModal () {
        $('#logoutModal').modal('show')
      }
    }
  }

</script>
