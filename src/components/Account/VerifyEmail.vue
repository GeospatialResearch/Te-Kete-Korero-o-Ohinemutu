<template>
  <div class="content-info">
    <div class="row col-md-12 m-0 background-picture bottom-shadow" style="background-image: url('static/img/pictures/screenshot_ngawha.png')" />
    <div class="row text-center">
      <div class="col-md-12" style="background-color:#ffffff;">
        <h1 class="mt-4">
          Verify Email
        </h1>
        <div v-if="activationLoading">
          loading...
        </div>
        <div v-else-if="activationError">
          An error occured.
        </div>
        <div>
          <!-- v-else-if="activationCompleted" -->
          <h3 class="pt-2">
            Account activation successful.
          </h3>
          <br>
          <h5>
            Click the Login button and insert your new credentials.
          </h5>
          <h5>
            Or click
            <a href="">here</a>
            to go Home.
          </h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  mapActions,
  mapState,
} from 'vuex'

export default {
  computed: mapState('signup', [
    'activationCompleted',
    'activationError',
    'activationLoading',
  ]),
  created() {
    if (this.$route.name === 'verifyemail') {
      var keyObj = this.$route.params
      // console.log(this.$route.params)
      // console.log(this.$route.query.key)
      this.activateAccount(keyObj.key)
    }
  },
  beforeDestroy() {
    this.clearActivationStatus()
  },
  methods: mapActions('signup', [
    'activateAccount',
    'clearActivationStatus',
  ])
}
</script>
