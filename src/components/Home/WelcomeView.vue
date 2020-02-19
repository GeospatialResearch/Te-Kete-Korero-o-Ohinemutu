<template>
  <div class="content-info">
    <div class="background-picture bottom-shadow text-center center-content" style="background-image: url('static/img/pictures/screenshot_marae.png')">
      <h1 class="welcome-overlay">
        <p class="welcome">
          Welcome
        </p>
        <p class="proverb">
          <i>Titiro whakamuri, kōkiri whakamua</i>
        </p>
      </h1>
    </div>
    <div class="text-center pt-5" style="background-color:#ffffff;">
      <h1>Welcome to He Kete o Pakiwaitara</h1>
      <div class="pb-4">
        <h4 class="mt-4" style="color:#777777;">
          A space where whānau can gather narratives and traditional knowledge about their whenua
        </h4>
        <br>
        <h6 v-if="!authenticated">
          Click the Login button and insert your credentials or register if you don't have an account.
        </h6>
        <h6>
          <span v-if="!authenticated">Or</span>
          <a href="#" @click="goToMap()"> Go to Map </a>
          to start exploring
          <span v-if="authenticated"> narratives. </span>
          <span v-else> public narratives. </span>
        </h6>
      </div>
    </div>
  </div>
</template>

<script>

  export default {
    computed: {
      authenticated () {
        return this.$store.state.authenticated
      }
    },
    methods: {
      goToMap () {
        $('.viewer-container').animate({ scrollTop: 0 }, 100, () => {
          this.$store.commit('TOGGLE_CONTENT', 'map')
        })
      }
    }
  }

</script>
