<template>
  <div class="content-info">
    <div id="carouselExampleIndicators" class="carousel slide bottom-shadow" data-ride="carousel">
      <ol class="carousel-indicators">
        <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active" />
        <li data-target="#carouselExampleIndicators" data-slide-to="1" />
        <li data-target="#carouselExampleIndicators" data-slide-to="2" />
      </ol>
      <div class="carousel-inner" role="listbox">
        <!-- Slide One - Set the background image for this slide in the line below -->
        <div class="carousel-item carousel-item-welcome active" style="background-image: url('static/img/pictures/screenshot_marae.png')">
          <h1 class="welcome-overlay carousel-caption carousel-caption-welcome">
            <!-- d-none d-md-block -->
            <p class="welcome">
              Nau mai, Haere mai
            </p>
            <p class="proverb">
              <i>Titiro whakamuri, kōkiri whakamua</i>
            </p>
          </h1>
          <!-- <div class="carousel-caption d-none d-md-block">
            <h2 class="display-4">
              First Slide
            </h2>
            <p class="lead">
              This is a description for the first slide.
            </p>
          </div> -->
        </div>
        <!-- Slide Two - Set the background image for this slide in the line below -->
        <div class="carousel-item carousel-item-welcome" style="background-image: url('static/img/pictures/screenshot_ngawha.png')">
          <div class="carousel-caption">
            <h2 class="display-4">
              Second Slide
            </h2>
            <p class="lead">
              This is a description for the second slide.
            </p>
          </div>
        </div>
        <!-- Slide Three - Set the background image for this slide in the line below -->
        <div class="carousel-item carousel-item-welcome" style="background-image: url('https://source.unsplash.com/szFUQoyvrxM/1920x1080')">
          <div class="carousel-caption">
            <h2 class="display-4">
              Third Slide
            </h2>
            <p class="lead">
              This is a description for the third slide.
            </p>
          </div>
        </div>
      </div>
      <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true" />
        <span class="sr-only">Previous</span>
      </a>
      <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true" />
        <span class="sr-only">Next</span>
      </a>
    </div>
    <!-- <div class="background-picture bottom-shadow text-center center-content" style="background-image: url('static/img/pictures/screenshot_marae.png')">
      <h1 class="welcome-overlay">
        <p class="welcome">
          Nau mai, Haere mai
        </p>
        <p class="proverb">
          <i>Titiro whakamuri, kōkiri whakamua</i>
        </p>
      </h1>
    </div> -->
    <div class="text-center pt-5" style="background-color:#ffffff;">
      <h1>Welcome to Kete o Kōrero</h1>
      <div class="pb-4">
        <h4 class="mt-4" style="color:#777777;">
          A space where Ōhinemutu whānau can hold narratives and traditional knowledge about their whenua
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
