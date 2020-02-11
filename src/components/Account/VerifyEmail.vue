<template>
  <div class="content-info">
    <div class="background-picture bottom-shadow" style="background-image: url('static/img/pictures/screenshot_ngawha.png')" />
    <div class="text-center pt-5 pb-4">
      <h1>Verify Email</h1>
      <template v-if="activationLoading">
        loading...
      </template>
      <template v-else-if="activationError">
        An error occured.
      </template>
      <template v-else-if="activationCompleted">
        <h3 class="mt-4">
          Account activation successful.
        </h3>
        <br>
        <h5>
          Click the Login button and insert your new credentials.
        </h5>
        <h5>
          Or click
          <a href="" @click="this.$store.commit('TOGGLE_CONTENT', 'map')">here</a>
          to start exploring public narratives on the map.
        </h5>
      </template>
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
      console.log(this.$route.params)
      console.log(this.$route.query.key)
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
