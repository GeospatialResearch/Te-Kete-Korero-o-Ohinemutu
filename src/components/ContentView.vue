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
            <select v-model="selectedValue" class="btn btn-sm btn-dark dropdown-toggle" @change="onChange">
              <option value="eng">
                English
              </option>
              <option value="mao">
                Te Reo
              </option>
            </select>
          </div>
          <!-- <div v-if="authenticated" class="navbar-elem ml-3 ml-md-5 pointer" title="Website walkthrough">
            <font-awesome-icon icon="shoe-prints" />
            Walkthrough
          </div> -->
          <div class="dropdown">
            <span id="navbarDropdownAbout" class="dropdown-toggle navbar-elem ml-md-5 pointer" href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              User Manual
            </span>
            <div class="dropdown-menu ml-md-5" aria-labelledby="navbarDropdownAbout">
              <h5 class="dropdown-header pl-3" style="font-size:1.1rem;">
                Getting started
              </h5>
              <div class="dropdown-item">
                Create a user account
              </div>
              <div class="dropdown-item">
                Iwi membership verification
              </div>
              <div class="dropdown-item">
                Access to the Kete
              </div>
              <div class="dropdown-item">
                Map navigation
              </div>
              <h5 class="dropdown-header pl-3" style="font-size:1.1rem;">
                Layers
              </h5>
              <div class="dropdown-item">
                My Layers
              </div>
              <div class="dropdown-item">
                External layers
              </div>
              <div class="dropdown-item">
                Internal layers
              </div>
              <h5 class="dropdown-header pl-3" style="font-size:1.1rem;">
                Narratives
              </h5>
              <div class="dropdown-item">
                My narratives
              </div>
              <div class="dropdown-item">
                Other/Public narratives
              </div>
              <div class="dropdown-item">
                Add new narrative
              </div>
              <div class="dropdown-item">
                Date the narrative
              </div>
              <div class="dropdown-item">
                Narrative type
              </div>
              <div class="dropdown-item" @click="showAtuaModal()">
                Atua
              </div>
              <div class="dropdown-item">
                Add elements to the narrative
              </div>
              <div class="dropdown-item">
                Co-create a narrative
              </div>
              <div class="dropdown-item">
                Submit/Publish your narrative
              </div>
              <div class="dropdown-item">
                Kōhanga nests
              </div>
              <div class="dropdown-item">
                Narrative submission workflow
              </div>
            </div>
          </div>
          <div class="dropdown">
            <span id="navbarDropdownAbout" class="dropdown-toggle navbar-elem ml-md-5 pointer" href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              About
            </span>
            <div class="dropdown-menu ml-md-5" aria-labelledby="navbarDropdownAbout">
              <div class="dropdown-item text-muted">
                Te Kete o Kōrero ki te Ōhinemutu
              </div>
              <div class="dropdown-item text-muted">
                Te Tatau o Te Arawa
              </div>
              <div class="dropdown-item text-muted">
                University of Canterbury
              </div>
            </div>
          </div>
          <div class="dropdown">
            <span id="navbarDropdownAbout" class="dropdown-toggle navbar-elem ml-md-5 pointer" href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              More Info
            </span>
            <div class="dropdown-menu ml-md-5" aria-labelledby="navbarDropdownAbout">
              <div class="dropdown-item pointer" @click="showOtherDataSourcesModal()">
                Other data sources
              </div>
              <div class="dropdown-item text-muted">
                Tips and Tricks
              </div>
              <div class="dropdown-item text-muted">
                Website walkthrough
              </div>
            </div>
          </div>
          <div class="col p-0">
            <div class="float-right">
              <button class="btn btn-sm btn-dark mr-2" type="button" title="Go to Map" @click="$store.commit('TOGGLE_CONTENT', 'map')">
                <font-awesome-icon icon="map" />
                <span class="gotomap-text"> Map</span>
              </button>
              <button v-if="!authenticated" class="btn btn-sm btn-success" type="button" @click="showLoginModal()">
                Login
              </button>
              <button v-else class="btn btn-sm btn-outline-danger" type="button" @click="showLogoutModal()">
                Logout
              </button>
            </div>
          </div>
        </div>
        <div class="row">
          <welcome-view v-show="contentToShow=='welcome'" />
          <verify-email v-show="contentToShow=='verifyemail'" />
          <password-reset-confirm v-show="contentToShow=='passwordresetconfirm'" />
          <settings-view v-show="contentToShow=='themes'" />
          <main-map v-if="contentToShow=='map'" />
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
            <register v-if="formToShow=='register'" />
            <log-in v-if="formToShow=='login'" @close="closeModal()" />
            <password-reset v-if="formToShow=='resetpassword'" />
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
    <div id="atuaModal" class="modal fade">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              User Manual
            </h4>
          </div>
          <div class="modal-body">
            <atua-view />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="otherDataSourcesModal" class="modal fade">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              Other Data Sources
            </h4>
          </div>
          <div class="modal-body">
            <div class="mb-4" style="font-size:1rem;">
              <p>
                Here is a list of other places where you can find datasets or information that might be useful to you.
              </p>
              <p>
                The tool provides some default layers from these data sources but you can download other datasets through these services and upload them to the tool.
              </p>
            </div>
            <div class="pl-4 pr-4">
              <h6><a href="https://www.maorilandonline.govt.nz/gis/home.htm" target="_blank">Maori Land Online </a>&mdash; Maori Land Court</h6>
              <h6><a href="https://data.linz.govt.nz" target="_blank">LINZ Data Service </a>&mdash; Land Information New Zealand</h6>
              <h6><a href="https://data.mfe.govt.nz" target="_blank">MfE Data Service </a>&mdash; Ministry for the Environment</h6>
              <h6><a href="https://lris.scinfo.org.nz" target="_blank">LRIS Portal </a>&mdash; Land Resource Information Systems Portal</h6>
              <h6><a href="https://whenuaviz.landcareresearch.co.nz" target="_blank">Whenua Māori Visualisation Tool </a>&mdash; Manaaki Whenua Landcare Research</h6>
              <h6><a href="https://www.doc.govt.nz/our-work/maps-and-data" target="_blank">DOC Maps and Data </a>&mdash; Department of Conservation</h6>
              <h6><a href="https://datafinder.stats.govt.nz" target="_blank">Stats NZ Geographic Data Service </a>&mdash; Statistics New Zealand</h6>
              <h6><a href="https://catalogue.data.govt.nz/dataset" target="_blank">Open Data NZ </a>&mdash; Open Government Data Programme</h6>
              <h6><a href="https://www.tupu.nz" target="_blank">Tupu.nz </a>&mdash; Te Puni Kōkiri</h6>
              <h6><a href="https://maorimaps.com" target="_blank">Māori Maps </a>&mdash; Te Potiki National Trust Limited</h6>
              <br>
            </div>
            <p class="mt-3 mb-0">
              The links to other web locations are provided for your convenience. The tool is not responsible for the content or reliability of the linked websites.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Close
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
  import PasswordReset from 'components/Account/PasswordReset'
  import PasswordResetConfirm from 'components/Account/PasswordResetConfirm'
  import WelcomeView from 'components/Home/WelcomeView'
  import AtuaView from 'components/AtuaView'

  export default {
    components: {
      MainMap,
      SettingsView,
      SidePanel,
      LogIn,
      Register,
      VerifyEmail,
      PasswordReset,
      PasswordResetConfirm,
      WelcomeView,
      AtuaView
    },
    data () {
      return {
        selectedValue: "eng",
        formToShow: null
      }
    },
    computed: {
      contentToShow () {
        return this.$store.state.contentToShow
      },
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
      EventBus.$on('showResetPasswordForm', () =>{
        this.formToShow = 'resetpassword'
      })
      EventBus.$on('showAtuaModal', () =>{
        this.showAtuaModal()
      })
    },
    beforeCreate: function () {
      if (this.$route.name === 'verifyemail') {
        this.$store.commit('TOGGLE_CONTENT', 'verifyemail')
      }
      if (this.$route.name === 'passwordresetconfirm') {
        this.$store.commit('TOGGLE_CONTENT', 'passwordresetconfirm')
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
      },
      showAtuaModal () {
        $('#atuaModal').modal('show')
      },
      showOtherDataSourcesModal () {
        $('#otherDataSourcesModal').modal('show')
      }
    }
  }

</script>
