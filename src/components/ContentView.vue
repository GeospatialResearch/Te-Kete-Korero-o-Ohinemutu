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
          <welcome-view v-if="contentToShow=='welcome'" />
          <verify-email v-if="contentToShow=='verifyemail'" />
          <main-map v-if="contentToShow=='map'" />
          <settings-view v-if="contentToShow=='themes'" />
          <side-panel v-if="contentToShow=='map'" />
        </div>
      </div>
    </main>
    <!-- page-content" -->
    <div id="loginModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content modal-margin-top">
          <div class="modal-header" />
          <div class="modal-body">
            <register v-if="formToShow=='register'" @close="closeModal()" />
            <log-in v-if="formToShow=='login'" @close="closeModal()" />
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
  import SettingsView from 'components/SettingsView'
  import SidePanel from 'components/SidePanel'
  import LogIn from 'components/Account/Login'
  import Register from 'components/Account/Register'
  import VerifyEmail from 'components/Account/VerifyEmail'
  import WelcomeView from 'components/Home/WelcomeView'

  export default {
    components: {
      MainMap,
      SettingsView,
      SidePanel,
      LogIn,
      Register,
      VerifyEmail,
      WelcomeView
    },
    data () {
      return {
        selectedValue: "eng",
        // showLogin: false,
        formToShow: null
      }
    },
    computed: {
      contentToShow () {
        return this.$store.state.contentToShow
      },
      // username () {
      //   return this.$store.state.user.username
      // },
      authenticated () {
        return this.$store.state.authenticated
      }
    },
    mounted: function () {
      EventBus.$on('showSignupForm', () =>{
        this.formToShow = 'register'
      })
      EventBus.$on('showLoginForm', () =>{
        this.formToShow = 'login'
      })
    },
    beforeCreate: function () {
      if (this.$route.name === 'verifyemail') {
        this.$store.commit('TOGGLE_CONTENT', 'verifyemail')
      }
      // Check if the token is still valid, if yes set login, if not deauthenticate.
      this.$store.dispatch('getUser')
    },
    methods: {
      onChange (){
        // Update the store with the new language
        this.$store.commit('SET_LANG', this.selectedValue)
      },
      showLoginModal () {
        this.formToShow = 'login'
        EventBus.$emit('closePanel')
        $('#loginModal').modal('show')
        EventBus.$emit('removeWasValidated')
      },
      closeModal () {
        EventBus.$emit('removeWasValidated')
        $('#loginModal').modal('hide')
      },
      showLogoutModal () {
        $('#logoutModal').modal('show')
      }
    }
  }

</script>
