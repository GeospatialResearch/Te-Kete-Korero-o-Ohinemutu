<template>
  <div class="full-width center-content">
    <img src="static/img/logo.png">
    <div class="container">
      <div class="row">
        <welcome-message name="World" />
      </div>
    </div>
    <div class="container">
      <div class="row">
        <div class="col-sm">
          <main-map />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WelcomeMessage from 'components/Home/WelcomeMessage'
import MainMap from 'components/Map/mainMap.vue'

export default {
  components: {
    WelcomeMessage,
    MainMap
  }
}
</script>
